function y = client_receive()
ip = '192.168.1.51';
port = 8080;
t = tcpip(ip, port, 'NetworkRole', 'client');
disp("Connecting ... ")
fopen(t);
disp(" >> Connected")
y = fread(t, t.BytesAvailable);
disp(' >> Received')
