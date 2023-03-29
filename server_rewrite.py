# Server File

# Other notes
# Send fliplist, let clients flip
# game over cut due to scope issues

# Init
import pygame, socket, threading, time
global background, screen, swidth, sheight, BoardWidth, BoardHeight, BoardColor, Boardx, Boardy, BoardColor, CellWidth, CellHeight, BoarderWidth, BoarderColor, green, black, white
global s, host, port, player, clients, display, clientS1, clientS2, encoder
pygame.init()
clients=[]

# Config
display=False
encoder='utf-8'

# Display Init and Board Setup
inf=pygame.display.Info()
swidth=inf.current_w
sheight=inf.current_h
if display:
	screen=pygame.display.set_mode((swidth,sheight),flags=pygame.RESIZABLE)
BoardWidth=BoardHeight=int(sheight*0.885)
Boardx=int(sheight*.03)
Boardy=int(sheight*.1)
CellWidth=int(sheight*.1)
CellHeight=int(sheight*.1)
BoarderWidth=int(sheight*.01)
BoardColor=(30,240,100)
green=BoardColor
background=(0,0,0)
black=(0,0,0)
BoarderColor=(205,155,30)
white=(255,255,255)

# Text Function
def puttext(surf,pos,text,size,color,flag):
	fontrend=pygame.font.Font(pygame.font.get_default_font(),size)
	textrend=fontrend.render(text,1,color)
	if flag=="center":
		textpos=(surf.get_rect().centerx-int(textrend.get_rect().width/2.0),pos[1])
	elif flag == "left":
		textpos=(surf.get_rect().left+2,surf.get_rect().top)
	elif flag=="right":
		textpos=(surf.get_rect().right-2,surf.get_rect().top)
	else:
		textpos=pos
	surf.blit(textrend,textpos) 

# Accept client connection requests
def accept_clients():
	global s, clients
	print("Open to clients")
	while len(clients)<=1:
		clientsocket, addr = s.accept()
		print('Connected to: ' + addr[0] + ':' + str(addr[1]))
		clientsocket.sendall(bytes("Connected", encoder))
		threading.Thread(target=client_acc_thread, args=(clientsocket,)).start()
	return

# Identify Clients and Separate Sockets
def client_acc_thread(client):
	global s, clients, clientS1, clientS2
	if len(clients)==1:
		clientS2=client
		clients.append(clientS2)
		clientS2.sendall(bytes("black", encoder))
#		print(clientS2)
	if len(clients)==0:
		clientS1=client
		clients.append(clientS1)
		clientS1.sendall(bytes("white", encoder))
#		print(clientS1)
	return

# Scoreboard (Needs to send those results to clients)
def drawScoreBoard(b,w,turn):
	width=int(swidth*.4)
	height=int(sheight*.4)
	scoreboard=pygame.Surface((width,height))
	scoreboard.fill((0,0,100))
	if turn=="white":
		puttext(scoreboard,(width,3),"White Player Turn",40,white,"center")
	if turn=="black":
		puttext(scoreboard,(width,3),"Black Player Turn",40,white,"center")
	puttext(scoreboard,(10,70),"White Player Tiles Owned: "+str(w),30,white,"")
	puttext(scoreboard,(10,120),"Black Player Tiles Owned: "+str(b),30,white,"")
	return scoreboard	

# Board Class (Still needs modification)
class board:
#	Board Init (Leave as is)
	def __init__(self):
		self.rows=8
		self.columns=8
		self.cells=[]
		x=0
		y=0
		for r in range(8):
			row=[]
			x=0
			for c in range(8):
				row.append(cell("blank",x,y,x*CellWidth+Boardx+BoarderWidth*(x+1),y*CellHeight+Boardy+BoarderWidth*(y+1)))
				x=x+1
			self.cells.append(row)
			y=y+1
		self.turn="white"

#	Draw Board (Leave as is)
	def draw(self,player):
		screen.fill((0,0,0))
		pygame.draw.rect(screen,BoarderColor,pygame.Rect(Boardx,Boardy,BoardWidth,BoardHeight))
		for row in self.cells:
			for col in row:
				col.draw()
		screen.blit(drawScoreBoard(self.getCount("black"),self.getCount("white"),self.turn),(int(sheight*.93),100))	

#	Get Count of Claimed Cells (Should be okay, send result on calling end)
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

#	Game Over Detection (Should be okay, return may need fixed)
	def game_over(self):
		#returns black white or tie if game is over
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

#	Also done on client side
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
		return fliplist

# Cell class (Still needs modification)
class cell:
	def __init__(self,type,x,y,xpos,ypos):
		self.x=x
		self.y=y
		self.xpos=xpos
		self.ypos=ypos
		if type=="white":
			self.type="white"
		elif type=="black":
			self.type="black"
		else:
			self.type="blank"
		self.radius=int(CellHeight/2.0)
		self.centerx=self.xpos+int(CellWidth/2.0)		
		self.centery=self.ypos+int(CellHeight/2.0)		

	def move(self,type):
		if type=="white":
			self.type="white"
		elif type=="black":
			self.type="black"
		else:
			self.type="blank"
	def ret_type(self):
		return self.type

	def draw(self):
		pygame.draw.rect(screen,green,pygame.Rect(self.xpos,self.ypos,CellWidth,CellHeight))
		if self.type=="white":
			pygame.draw.circle(screen,white,(self.centerx,self.centery),self.radius)
		if self.type=="black":
			pygame.draw.circle(screen,black,(self.centerx,self.centery),self.radius)

# Board Setup
#while True:
game=board()
game.cells[3][3].move("white")
game.cells[4][4].move("white")
game.cells[3][4].move("black")
game.cells[4][3].move("black")
#	wait=False
player="white"
#	puttext(screen,(200,500),"WELCOME TO OTHELLO. LET'S PLAY!",80,(0,255,0),"Center")
#	wait=True

# Init Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',8002))
s.listen(2)
idle=True

# Main Loop (Heavy modification needed)
while True:
	if idle==True:
		accept_clients()
		if len(clients)==2:
			clientS1.sendall(bytes("gameon", encoder))
			time.sleep(1)
#			print(clientS2)
			clientS2.sendall(bytes("gameon", encoder))
			idle=False
	ev=pygame.event.get()
	for event in ev:
		if event.type==pygame.KEYUP:
			if event.key==pygame.K_ESCAPE: # add another key later
				exit()

	if idle==False and player=="white":
		time.sleep(5)
		clientS1.sendall(bytes("white turn", encoder))
		clientS2.sendall(bytes("white turn", encoder))
		coords=clientS1.recv(1024) # Wait for coordinates from white
		coords.split()
		print(coords) # debug
		if coords[0]<8 and coords[1]<8 and coords[0]>-1 and coords[1]>-1:
				p=game.evaluate_move(x,y,player)
				if len(p)>0: # what is this
					clientS1.sendall(bytes(player+ "Valid Move", encoder))
					p.append((y,x)) # why is this here
					game.flip_pieces(p,player)
					clientS1.sendall(bytes(p, encoder)) # May not work
					if player=="white":
						player="black"
					else:
						player="white"
					if not game.moves_possible(player):
						if player=="white":
							player="black"
						else:
							player="white"
					game.turn=player
				game.draw(player)
				if len(p) == 0:
					puttext(screen,(200,500),"INVALID MOVE!!!",80,(255,0,0),"Center")
					clientS1.sendall(bytes("Invalid Move", encoder))
					wait=True
		game.turn=player
	# Test white first, then black
	pygame.display.flip()