import requests as requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.views.generic import CreateView
from kavenegar import *
import logging

logger = logging.getLogger("user")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'user/user_register.html'
    success_url = 'user_login'

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect("user_login")
        else:
            logger.error(f"{form.errors}")
            return render(request, 'user/user_register.html', {"form": form})


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        next = request.GET.get("next", "")
        if user:
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect("/user/")
            # return redirect("/email_website/")

        else:
            logger.warning("username or password was wrong")
            return render(request, 'user/login.html', {'message': 'username or password was wrong'})


def validation_form(request):
    if request.method == "GET":
        form = ValidationForm()
        import requests
        url = "https://api.kavenegar.com/v1/622B496B4734464C646D6B3275473861506D63393470386D4A5333664F627056456C4758344C6B744A49733D/sms/send.json"
        payload = {"receptor": "09177276144", "message": "کد تایید 5556"}
        payam = requests.post(url, data=payload)
        return render(request, "user/validation_code.html", {"form": form})

    elif request.method == "POST":
        # form is object of class
        form = ValidationForm(request.POST)
        if form.is_valid():
            # clean data is a dict
            validate_number = form.cleaned_data["validate_number"]
            if validate_number == '5556':
                return HttpResponse("Login successfully")
            else:
                logger.warning("validate_number isn't correct")
                return HttpResponse('validate_number isnt correct')


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/user/")
    elif request.method == "GET":
        return render(request, "user/logout.html", {})
