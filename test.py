import pip._vendor.requests as req,socket
BASE = 'http://127.0.0.1:5000/'
response = req.get(BASE+'ack')
print(response.json())

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(''.join(s.getsockname()[0].rpartition('.')[:2]))
