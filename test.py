import  socket
import dns

import dns.query

#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('80.77.12.178', 10000)
# sock.connect(server_address)
# sock.send("h")
# h=sock.recv((222));sssd
#
IP_ADDRESS='60.6.75.31'
queryCheck = dns.message.make_query('www.google.com', 2)
dns.query.tcp(queryCheck,IP_ADDRESS)

# def checkIfTcp(serverAddress):
#   #  try:sdf
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_address=(serverAddress,10000);
#         sock.connect(server_address)
#     #except:
#         print("h")
#
# #checkIfTcp('www.google.co.il')
#
#
#
#
# s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# result = s.connect_ex(('113.165.88.235 ', 10000))
# s.close()
# if result > 0:
#     print("problem with socket!")
# else:
#     print("everything it's ok!")