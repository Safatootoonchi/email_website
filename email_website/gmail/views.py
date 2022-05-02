from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from .form import EmailModelForm, LabelForm, FilterForm, ContactForm, SearchContactForm, SignatureForm, ReplyForm, \
    ForwardForm
from .models import Email, Label, Filter, Contact, Signature, BackGround, Reply, Forward
from user.models import User
from django.views.generic import FormView, DetailView, ListView, DeleteView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpRequest
from django.db.models import Q
import csv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactSerializer, EmailSerializer

from django.urls import reverse
import datetime
import logging

logger = logging.getLogger("gmail")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name="next")
def home(request):
    return render(request, "gmail/base.html", {})


def compose(request):
    return render(request, "gmail/compose.html", {})


def test(request):
    return render(request, "gmail/twst.html", {})


class NewEmail(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = "next"

    def get(self, request):
        email_form = EmailModelForm()
        return render(request, "gmail/compose.html", {"email_form": email_form})

    def post(self, request):
        if 'send' in request.POST:
            email_form = EmailModelForm(request.POST, request.FILES)
            if email_form.is_valid():
                user_login = request.user
                sing = Signature.objects.filter(user=user_login)
                content = email_form.cleaned_data["content"]
                cc = email_form.cleaned_data["cc"]
                bcc = email_form.cleaned_data["bcc"]
                if cc:
                    cc_s = cc.split(',')
                else:
                    cc_s = []
                if bcc:
                    bcc_s = bcc.split(',')
                else:
                    bcc_s = []
                s = cc_s + bcc_s
                for i in sing:
                    content = f"{content}\n\n{i.text}"
                email = Email(title=email_form.cleaned_data["title"],
                              to=email_form.cleaned_data["to"],
                              content=content,
                              cc=email_form.cleaned_data["cc"],
                              bcc=bcc,
                              file=email_form.cleaned_data["file"],
                              user=user_login
                              )
                for w in s:
                    email2 = Email(title=email_form.cleaned_data["title"],
                                   to=w,
                                   content=content,
                                   cc=cc,
                                   file=email_form.cleaned_data["file"],
                                   user=user_login,
                                   show="N",
                                   )
                    email2.save()

                email.save()

                return render(request, "gmail/base.html", {"message": "email was sent successfully. "})

            else:
                logger.error(f"There is problem: {email_form.errors}")
                return HttpResponse(f"There is problem: {email_form.errors}")
        elif 'draft' in request.POST:
            email_form = EmailModelForm(request.POST, request.FILES)
            if email_form.is_valid():
                user_login = request.user
                sing = Signature.objects.filter(user=user_login)
                content = email_form.cleaned_data["content"]
                cc = email_form.cleaned_data["cc"]
                bcc = email_form.cleaned_data["bcc"]
                if cc:
                    cc_s = cc.split(',')
                else:
                    cc_s = []
                if bcc:
                    bcc_s = bcc.split(',')
                else:
                    bcc_s = []
                s = cc_s + bcc_s
                for i in sing:
                    content = f"{content}\n\n{i.text}"
                email = Email(title=email_form.cleaned_data["title"],
                              to=email_form.cleaned_data["to"],
                              content=content,
                              cc=cc,
                              bcc=bcc,
                              file=email_form.cleaned_data["file"],
                              user=user_login,
                              draft="Y"
                              )
                for w in s:
                    email2 = Email(title=email_form.cleaned_data["title"],
                                   to=w,
                                   content=content,
                                   cc=cc,
                                   file=email_form.cleaned_data["file"],
                                   user=user_login,
                                   show="N",
                                   draft="Y"
                                   )
                    email2.save()
                email.save()
                return render(request, "gmail/base.html", {"message": "email was draft successfully. "})
            else:
                logger.error(f"There is problem: {email_form.errors}")
                return HttpResponse(f"There is problem: {email_form.errors}")


def inbox(request):
    user_login = request.user
    email_g = Email.objects.filter(to=user_login.name, draft="N", archive="N", deleted="N")
    return render(request, "gmail/inbox.html", {"email": email_g})


def sent(request):
    user_login = request.user
    email_f = Email.objects.filter(user=user_login.id, draft="N", archive="N", show="Y", deleted="N")
    return render(request, "gmail/sent.html", {"email": email_f})


def draft(request):
    user_login = request.user
    email_d = Email.objects.filter(user=user_login.id, draft="Y", show="Y", deleted="N")
    return render(request, "gmail/draft.html", {"email": email_d})


def draft_detail(request, id):
    if request.method == "GET":
        try:
            email = Email.objects.get(id=id)
            return render(request, "gmail/draft_detail.html", {"object": email})

        except:
            logger.error(f"Email with id {id} does not exist. ")
            return HttpResponse("This email does not exist. ")
    elif request.method == "POST":
        email = Email.objects.filter(id=id).update(draft="N")
        return render(request, "gmail/base.html", {"message": "Email was sent successfully. "})


def archive(request):
    user_login = request.user
    email_d = Email.objects.filter(Q(user=user_login.id, archive="Y") | Q(to=user_login.name, archive="Y"))
    return render(request, "gmail/archive.html", {"email": email_d})


def archive_detail(request, id):
    if request.method == "GET":
        try:
            email = Email.objects.get(id=id)
            return render(request, "gmail/archive_detail.html", {"object": email})

        except:
            logger.error(f"Email with id {id} does not exist. ")
            return HttpResponse("This email does not exist. ")
    elif request.method == "POST":
        email = Email.objects.filter(id=id).update(archive="N")
        return render(request, "gmail/base.html", {"message": "No archive. "})


def trash(request):
    user_login = request.user
    email_d = Email.objects.filter(user=user_login.id, deleted="Y")
    for e in email_d:
        day = datetime.datetime.now().replace(tzinfo=None) - e.trash.replace(tzinfo=None)
        if day.days > 30:
            e.delete()
            logger.warning(f"Email with id {e.id} was deleted. ")

    return render(request, "gmail/trash.html", {"email": email_d})


def trash_detail(request, id):
    if request.method == "GET":
        try:
            email = Email.objects.get(id=id)
            day = (datetime.datetime.now().replace(tzinfo=None) - email.trash.replace(tzinfo=None))
            d = 30 - day.days
            return render(request, "gmail/trash_detail.html", {"object": email, "day": d})

        except:
            logger.error(f"Email with id {id} does not exist. ")
            return HttpResponse("This email does not exist. ")
    elif request.method == "POST":
        email = Email.objects.filter(id=id).update(deleted="N", trash=None)
        return render(request, "gmail/base.html", {"message": "No trash. "})


a = ''


def email_detail_send(request, id):
    if request.method == "GET":
        try:
            email = Email.objects.get(id=id)
            form_l = LabelForm()
            form_r = ReplyForm()
            form_f = ForwardForm()
            return render(request, "gmail/email_detail_send.html",
                          {"object": email, "form_l": form_l, "form_r": form_r, "form_f": form_f})

        except:
            logger.error(f"Email with id {id} does not exist. ")
            return HttpResponse("This email does not exist. ")
    elif request.method == "POST":
        if 'save' in request.POST:
            form = LabelForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data["title"])
                new_label = Label(title=form.cleaned_data["title"],
                                  user=request.user.name,
                                  email=id,
                                  due_date=timezone.now()
                                  )
                new_label.save()
                return render(request, "gmail/base.html", {"message": "Label was created successfully. "})

            else:
                logger.error(f"There is problem: {form.errors}")
                return HttpResponse(f"There is problem: {form.errors}")
        elif 'archive' in request.POST:
            email = Email.objects.filter(id=id).update(archive="Y")
            return render(request, "gmail/base.html", {"message": "Email was archived. "})
        elif 'trash' in request.POST:
            email = Email.objects.filter(id=id).update(trash=datetime.datetime.now())
            email2 = Email.objects.filter(id=id).update(deleted="Y")
            return render(request, "gmail/base.html", {"message": "Email was trashed. "})

        elif 'reply' in request.POST:
            form = ReplyForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                file = form.cleaned_data["file"]
                user = request.user
                email = Email.objects.get(id=id)
                content_f = f"{content}\n\n-----------reply message---------\n\n{email.content}"
                email = Email(title=title,
                              to=email.user.name,
                              content=content_f,
                              file=file,
                              user=user,
                              draft="N"
                              )
                email.save()
                return render(request, "gmail/base.html", {"message": "Was replayed successfully. "})
            else:
                logger.error(f"There is problem: {form.errors}")
                return HttpResponse(f"There is problem: {form.errors}")
        elif 'forward' in request.POST:
            form = ForwardForm(request.POST, request.FILES)
            if form.is_valid():
                to = form.cleaned_data["to"]
                user = request.user
                email = Email.objects.get(id=id)
                content_f = f"\n\n-----------Forward message---------\n\n{email.content}"
                email = Email(title=email.title,
                              to=to,
                              content=content_f,
                              file=email.file,
                              user=user,
                              draft="N"
                              )
                email.save()
                return render(request, "gmail/base.html", {"message": "Forwarded successfully. "})
            else:
                logger.error(f"There is problem: {form.errors}")
                return HttpResponse(f"There is problem: {form.errors}")


def label_list(request):
    l = []
    d = []
    label = Label.objects.filter(Q(user=request.user.name) | Q(user=None))
    for i in label:
        if i.title not in l:
            l.append(i.title)
            d.append(i.id)
    l.reverse()
    d.reverse()
    s = []
    for i in range(len(d)):
        s.append([l[i], d[i]])
    return render(request, "gmail/label_list.html", {"index": s})


def label_detail(request, id):
    if request.method == "GET":
        emaill = []
        l = Label.objects.get(id=id)
        s = l.title
        n = Label.objects.filter(title=s)

        for i in n:
            if i.email:
                e = i.email
                emaill.append(Email.objects.get(id=e))
        return render(request, "gmail/label_detail.html", {"label": l, "object": emaill})

    elif request.method == "POST":

        l = Label.objects.get(id=id)
        s = l.title
        if l.user:
            Label.objects.filter(title=s).delete()
            return render(request, "gmail/base.html", {"message": "Label was deleted successfully. "})
        else:
            logger.warning("This label is the default, it is not possible to delete. ")
            return render(request, "gmail/base.html",
                          {"message": "This label is the default, it is not possible to delete. "})


class FilterView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = "next"

    def get(self, request):
        form = FilterForm()
        form2 = FilterForm()
        return render(request, "gmail/filter.html", {"form": form, "form2": form2})

    def post(self, request):
        if 'filter' in request.POST:
            form = FilterForm(request.POST)
            if form.is_valid():
                filter_by = form.cleaned_data["filter_by"]
                text = form.cleaned_data["text"]
                label = form.cleaned_data["label"]
                if filter_by == "F":
                    user_f = User.objects.get(name=text)
                    id_f = user_f.id
                    if request.user.id != id_f:
                        email_f = Email.objects.filter(user=id_f)
                        for i in email_f:
                            new_label = Label(title=label,
                                              user=request.user.name,
                                              email=i.id,
                                              due_date=timezone.now()
                                              )
                            new_label.save()
                        return render(request, "gmail/base.html", {"message": "Filter was sent successfully. "})
                    else:
                        logger.warning(f"user whit id {id_f} is already registered. ")

                elif filter_by == "W":
                    email_w = Email.objects.filter(content__contains=text)
                    for i in email_w:
                        new_label = Label(title=label,
                                          user=request.user.name,
                                          email=i.id,
                                          due_date=timezone.now()
                                          )
                        new_label.save()
                    return render(request, "gmail/base.html", {"message": "Filter was sent successfully. "})

            else:
                logger.error(f"There is problem: {form.errors}")
                return HttpResponse(f"There is problem: {form.errors}")
        elif 'f_archive' in request.POST:
            form = FilterForm(request.POST)
            if form.is_valid():
                user_login = request.user
                email_filter = Filter(filter_by=form.cleaned_data["filter_by"],
                                      text=form.cleaned_data["text"],
                                      user=user_login,
                                      archive="Y"
                                      )
                email_filter.save()
                filter_by = form.cleaned_data["filter_by"]
                text = form.cleaned_data["text"]
                if filter_by == "F":
                    user_f = User.objects.get(name=text)
                    id_f = user_f.id
                    if request.user.id != id_f:
                        email_f = Email.objects.filter(user=id_f).update(archive="Y")
                        return render(request, "gmail/base.html",
                                      {"message": "Emails in this filter (FROM) was archived. "})
                    else:
                        logger.warning(f"user whit id {id_f} is already registered. ")

                elif filter_by == "W":
                    email_w = Email.objects.filter(content__contains=text).update(archive="Y")
                    return render(request, "gmail/base.html",
                                  {"message": "Emails in this filter (HAS WORD) was archived. "})

            else:
                logger.error(f"There is problem: {form.errors}")
                return HttpResponse(f"There is problem: {form.errors}")
        elif 'f_trash' in request.POST:
            form = FilterForm(request.POST)
            if form.is_valid():
                filter_by = form.cleaned_data["filter_by"]
                text = form.cleaned_data["text"]
                if filter_by == "F":
                    user_f = User.objects.get(name=text)
                    id_f = user_f.id

                    if request.user.id != id_f:
                        email_f = Email.objects.filter(user=id_f).update(trash=datetime.datetime.now())
                        email2 = Email.objects.filter(user=id_f).update(deleted="Y")
                        return render(request, "gmail/base.html",
                                      {"message": "Emails in this filter (FROM) was trashed. "})
                    else:
                        logger.warning(f"user whit id {id_f} is already registered. ")
                    # return render(request, "gmail/base.html",
                    #               {"message": "Nooooooo. "})

                elif filter_by == "W":
                    email_w = Email.objects.filter(content__contains=text).update(trash=datetime.datetime.now())
                    email2 = Email.objects.filter(content__contains=text).update(deleted="Y")
                    return render(request, "gmail/base.html",
                                  {"message": "Emails in this filter (HAS WORD) was trashed. "})

            else:
                logger.error(f"There is problem: {form.errors}")
                return HttpResponse(f"There is problem: {form.errors}")


class ContactView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = "next"

    def get(self, request):
        form = ContactForm()
        return render(request, "gmail/contact.html", {"form": form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            user_login = request.user
            email = form.cleaned_data["email"]
            name = form.cleaned_data["name"]
            print(name)
            try:
                user_c = User.objects.get(name=name)
                email_c = user_c.email
                if email == email_c:
                    email = Contact(email=email,
                                    name=name,
                                    phone=form.cleaned_data["phone"],
                                    other_email=form.cleaned_data["other_email"],
                                    birthday=form.cleaned_data["birthday"],
                                    user=user_login
                                    )
                    email.save()
                    return render(request, "gmail/base.html", {"message": "Contact was added successfully. "})
                else:
                    return render(request, "gmail/base.html", {"message": "email of this user is not correct. "})

            except:
                logger.error("This username does not exist. ")
                return render(request, "gmail/base.html", {"message": "This username does not exist. "})

        else:
            logger.error(f"There is problem: {form.errors}")
            return HttpResponse(f"There is problem: {form.errors}")


class ContactList(LoginRequiredMixin, ListView):
    model = Contact
    login_url = settings.LOGIN_URL
    redirect_field_name = "next"


def search_email(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        artists = Email.objects.filter(content__icontains=url_parameter)
    else:
        artists = Email.objects.all()

    ctx["artists"] = artists
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            template_name="artists-results-partial.html", context={"artists": artists}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "artists.html", context=ctx)


def search_contact(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        artists = Contact.objects.filter(
            Q(email__icontains=url_parameter) | Q(name__icontains=url_parameter) | Q(
                phone__icontains=url_parameter) | Q(
                other_email__icontains=url_parameter) | Q(birthday__icontains=url_parameter))
    else:
        artists = Contact.objects.all()

    ctx["artists"] = artists
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            template_name="artists-results-partial2.html", context={"artists": artists}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "artists2.html", context=ctx)


def exportcsv(request):
    contacts = Contact.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=contacts.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Email', 'Name', 'Phone', 'Other Email', 'Birthday'])
    studs = contacts.values_list('id', 'email', 'name', 'phone', 'other_email', 'birthday')
    for std in studs:
        writer.writerow(std)
    return response


class SignatureView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = "next"

    def get(self, request):
        form = SignatureForm()
        return render(request, "gmail/sign.html", {"form": form})

    def post(self, request):
        form = SignatureForm(request.POST)
        if form.is_valid():
            user_login = request.user
            sign = Signature(text=form.cleaned_data["text"],
                             user=user_login
                             )
            sign.save()
            return render(request, "gmail/base.html", {"message": "Signature was added successfully. "})

        else:
            logger.error(f"There is problem: {form.errors}")
            return HttpResponse(f"There is problem: {form.errors}")


class SignatureList(LoginRequiredMixin, ListView):
    model = Signature
    login_url = settings.LOGIN_URL
    redirect_field_name = "next"


class SignatureDetail(LoginRequiredMixin, DetailView):
    model = Signature
    login_url = settings.LOGIN_URL
    redirect_field_name = "next"


@api_view()
def email_sent_api(request):
    user_login = request.user
    email_f = Email.objects.filter(user=user_login.id)
    ser_data = EmailSerializer(email_f, many=True)
    return Response(ser_data.data, status=status.HTTP_200_OK)


@api_view()
def email_received_api(request):
    user_login = request.user
    email_g = Email.objects.filter(to=user_login.name)
    ser_data = EmailSerializer(email_g, many=True)
    return Response(ser_data.data, status=status.HTTP_200_OK)


@api_view()
def contact_api(request):
    user_login = request.user
    contact_e = Contact.objects.filter(user=user_login)
    ser_data = ContactSerializer(contact_e, many=True)
    return Response(ser_data.data, status=status.HTTP_200_OK)


class BackColor(View):
    def get(self, request):
        back = BackGround.objects.all()

        return render(request, "gmail/base.html", {"back": back})

    def post(self, request):
        back = BackGround.objects.all()
        return render(request, "gmail/base.html")


def signature_detail(request, id):
    if request.method == "GET":
        l = Signature.objects.get(id=id)
        return render(request, "gmail/signature.html", {"object": l})

    elif request.method == "POST":
        return render(request, "gmail/base.html", {"message": "Signature was deleted successfully."})


class SignatureDeleteView(DeleteView):
    template_name = 'gmail/delete_view.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Signature, id=id_)

    def get_success_url(self):
        return reverse('signature_list')
