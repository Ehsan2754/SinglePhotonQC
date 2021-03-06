function [outputArg1] = LG(ro,phi,w,l,p)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
outputArg1 = ((-1)^p)*
sqrt(2*factorial(p)/pi/w/w/factorial(p+abs(l)))*
((sqrt(2).*ro/w).^abs(l));
c=1.5;
x=(ro/(w/c)).^2;
outputArg1=outputArg1.*exp(1i*l*phi).*L_pl(2*x,l,p).*exp(-(ro/w).^2);
end

