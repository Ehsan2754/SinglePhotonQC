function client_init(ip,port)
t = tcpip(ip, port, 'NetworkRole', 'client');
disp("Connecting ... ")
fopen(t);
disp(" >> Connected")