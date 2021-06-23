
%%%
%
% byte img [1920][1080]
% >> 0-255
%
%
% clear all;
add_heds_path;

% Detect SLMs and open a window on the selected SLM:
heds_init_slm;

% Open the SLM preview window (might have an impact on performance):
heds_utils_slm_preview_show;

% Calculate e.g. a vertical blazed grating:
blazePeriod = 5;
% Reserve memory for the data:
x = heds_slm_width_px;

y = heds_slm_height_px;

%%%%��� 532 ��
x= [-x/2:1:x/2-1]-10;
y=[-y/2:1:y/2-1]-10;


% %��� 850 ��
% x= [-x/2:1:x/2-1]+370;
% y=[-y/2:1:y/2-1]+120;


[X Y]=meshgrid(x,y); % create matrices for grids of X and Y 1920 x 1080
[phi,ro] = cart2pol(X,Y); %transform Cartesian coordinates to polar
p=0;



L11=2;
L12=-2;
L13=3;
L14=4;
L15=0;
L16=0;


w0=100; % gaussian waist beam ��� ������� ��� 13333333333333333
LG11=LG(ro,phi,w0,L11,p);
LG12=LG(ro,phi,w0,L12,p);
LG13=LG(ro,phi,w0,L13,p);
LG14=LG(ro,phi,w0,L14,p);
LG15=LG(ro,phi,w0,L15,p);
% LG16=LG(ro,phi,w0,L16,p);

% 
% a=sqrt(4/20); for 1 and 2

a=sqrt(5/80);
b=sqrt(5/80)*exp(0i*pi/6);

c=sqrt(0/80);
d=sqrt(0/80);

e=sqrt(0/105);

% a=sqrt(3.5/20);
% b=sqrt(3.5/20);
% c=sqrt(6.5/20);
% d=sqrt(6.5/20);
% a=sqrt(1/2);
% b=sqrt(0/2);
% c=sqrt(0/20);
% d=sqrt(0/20);
e=sqrt(0/50);
f=sqrt(0/50);

Result_1=(a)*LG11+b*LG12+c*LG13+d*LG14+e*LG15;
% Result_1=LG11*exp(12*1i*pi);
Result_1=Result_1/max(max(abs(Result_1)));
Amplitude=abs(Result_1);
Phase=angle(Result_1)-pi*Amplitude;

PHASE_1=mod(Phase-2*pi*X/blazePeriod,2*pi).*Amplitude/2/pi*256;
data=uint8(PHASE_1);

heds_show_data(data);


