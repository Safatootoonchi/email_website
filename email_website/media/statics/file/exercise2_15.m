clear, clc
%exercise2_14
%find the power that is dissipated through a wire with fallowing dementions
d=000.1; %diameter in meter
l=2.00; %length in meter
i=120; %current of the wire in amps
A=pi*(d/2)^2;
Resistivity=[1.59*10^(-8) 1.68*10^(-8) 2.44*10^(-8) 2.82*10^(-8) 1.0*10^(-7)];
...*[Silver Copper Gold Aluminum Iron];
%claculate the power
p=(i^2*Resistivity*l)/A; %power in order of left to right for silver toiron
str = ["M","G","A","F"];

disp(p)
