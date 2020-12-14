function server_broadcast(data)
port = 8080;
t = tcpip('0.0.0.0', port, 'NetworkRole', 'server');
disp("Connecting ... ")
fopen(t);
disp(" >> Connected")
fwrite(t, data);
disp(data)
disp(' >> Sent')
