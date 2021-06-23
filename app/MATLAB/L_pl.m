function [value] = L_pl(x,l,p)
value=0;
for i=0:p
    value=value+(-1).^i*factorial(p+abs(l))./factorial(p-i)./factorial(abs(l)+i)./factorial(i).*x.^i;

end

