import socket
import re

HTTPRESPONSE = 'HTTP/1.1 200 OK\r\n\r\n'

DATARESPONSE = 'HTTP/1.1 200 OK\r\nContent-Type: "application/json"\r\nContent-length: 86\r\n\r\n{"cnt":"4457,005","pwr":453,"lvl":0,"dev":"","det":"","con":"OK","sts":"(52)","raw":0}'

INFORESPONSE = 'HTTP/1.1 200 OK\r\nContent-Type: "application/json"\r\nContent-length: 43\r\n\r\n{"model":"LS120","mac":"72:b8:ad:14:00:04"}'

GASRESPONSE = 'HTTP/1.1 200 OK\r\nContent-Type: "application/json"\r\nContent-length: 134\r\n\r\n[{"tm":1692912986,"net": 13622.201,"pwr": 207,"p1": 6277.846,"p2": 7344.375,"n1": 0.020,"n2": 0.000,"gas": 3544.785,"gts":2308242335}]'

PORT = 6666

def get_body_len(buf):

  contentlength=re.compile("Content-Length: (.*?)\n")
  bodylen_array = contentlength.findall(buf)
  if len(bodylen_array) > 0:
    bodylen = bodylen_array[0]

    if bodylen:
      return int(bodylen)

  return 0


def server_program():

  server_socket = socket.socket()  # get instance
  # look closely. The bind() function takes tuple as argument
  try:
    server_socket.bind(('', PORT))  # bind host address and port together
  except:
    print("Could not bind to port; try again in 30 seconds")
    exit(1)

  # configure how many clients the server can listen simultaneously
  server_socket.listen(1)

  while True:
    print("\n\t>>> Listening on port " + str(PORT) + "...")
    conn, address = server_socket.accept()  # accept new connection
    print("\n-----------------------------------------")
    print("Connection from: " + str(address))
    print("-----------------------------------------\n")
    allreceived = False
    receivebuf = ''
    try:
      while not allreceived:
        received = str(conn.recv(1024).decode())
        received_len = len(received)
        if received_len == 0:
          break

        print (f'-- Received {received_len} bytes:\n')
        print(received)

        receivebuf = receivebuf + received
        receivebuf_len = len(receivebuf)
        
        endheader_idx = receivebuf.find('\r\n\r\n')
        if endheader_idx >= 0:
          len_sans_body = endheader_idx + 4

          bodylen = get_body_len(receivebuf)
          if bodylen > 0:
            if receivebuf_len == (len_sans_body + bodylen):
              allreceived = True
          elif bodylen == 0:
            allreceived = True

      if "/a?f=j" in receivebuf:
        conn.send(DATARESPONSE.encode())  # send response to the client

      elif "/d" in receivebuf:
        conn.send(INFORESPONSE.encode())  # send response to the client
        
      elif "/e" in receivebuf:
        conn.send(GASRESPONSE.encode())

      conn.close()
    except Exception as e:
      print (f'Error during receive: {e}')
      conn.close()


if __name__ == '__main__':

  try:
    server_program()
  except KeyboardInterrupt:
    print ('\nINFO: Action interrupted by user...\n')
