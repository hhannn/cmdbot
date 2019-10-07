from websocket import create_connection
ws = create_connection("ws://api.warframestat.us/pc/cetusCycle")
ws.send('"ShortString"')

while True:
  result =  ws.recv()
  print ("Received '%s'" % result)

ws.close()