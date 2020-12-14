function server_init(port)
port = 8080;
t = tcpip('0.0.0.0', port, 'NetworkRole', 'server');
disp("Connecting ... ")
fopen(t);
disp(" >> Connected")