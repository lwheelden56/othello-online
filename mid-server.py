# Server File

# Notes
# When checking transmissions from clients, make sure to note client id
# THIS WILL BE MERGED INTO SERVER REWRITE

# Init
import socket, sys, pygame
global host, port, s
client1Connected=False
client2Connected=False

host = '' # Should refer to all available interfaces
port = 8002 

# Game Functions
def getCount(self,type):
	cnt=0
	for row in self.cells:	
		for col in row:
			if col.ret_type()==type:
				cnt=cnt+1
	return cnt	

def moves_possible(self,color):	
	count=0
	for row in range(8):
		for col in range(8):
			count =count+len(self.evaluate_move(col,row,color))
	return not count==0

def game_over(self): # needs to return game_over and color 
	# Returns black, white, or tie if game is over
	if self.getCount("black")==0:
		return "white"
	if self.getCount("white")==0:
		return "black"
	if self.getCount("blank")==0 and self.getCount("black")>self.getCount("white"):
		return "black"
	if self.getCount("blank")==0 and self.getCount("black")<self.getCount("white"):
		return "white"
	if self.getCount("blank")==0 and self.getCount("black")==self.getCount("white"):
		return "nobody"
	return "game on"
	
def flip_pieces(self,plist,color):
	for b in plist:
		self.cells[b[0]][b[1]].move(color)
	
def evaluate_move(self,col,row,color):
	#return list of flippable coordinates
	fliplist=[]
	if color=="white":
		opponent="black"
	else:
		opponent="white"
		
	if not self.cells[row][col].ret_type()=="blank":
		return []
	delc=0
	delr=-1
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	delc=1
	delr=-1
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	delc=1
	delr=0
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	delc=1
	delr=1
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	delc=0
	delr=1
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	delc=-1
	delr=1
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	delc=-1
	delr=0
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	delc=-1
	delr=-1
	ccol=col+delc
	crow=row+delr
	plist=[]
	while crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==opponent:
		plist.append((crow,ccol))
		ccol=ccol+delc
		crow=crow+delr
	if crow>=0 and ccol >=0 and crow<=7 and ccol<=7 and self.cells[crow][ccol].ret_type()==color:
		for c in plist:
			fliplist.append(c)
	conn.sendall(fliplist)
	return fliplist

# Init Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(host,port)
s.listen(2)

clients[''] # may not work

# Main Loop
with conn:
	while True:
		conn, addr = s.accept() # needed in loop to keep accepting connections
		rxdata = conn.recv(1024)
#		Claim ID system
		if rxdata == "claim":
			if not clients: # better way to do this?
				clients.append(1)
				client1Connected=True
			elif len(clients)==1:
				clients.append(2)
				client2Connected=True
			elif len(clients)==2:
				conn.sendall("Server Full")
#		Soft Disconnects
