# Othello LAN Multiplayer Client
# Liam Wheelden

# Init
import pygame, time, socket
global background, screen, swidth, sheight, BoardWidth, BoardHeight, BoardColor, Boardx, Boardy, BoardColor, CellWidth, CellHeight, BoarderWidth, BoarderColor,green, black, white
global host, port, s, color, send

# Connection Init
print("Connect to server:")

host = str(input())
port = 8002

# Connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to server...")
s.connect((host, port))

while True:
	rxdata=s.recv(1024)
	if rxdata.decode()=="Connected":
		print("Connected to server, getting color...")
	if rxdata.decode()=="white" or rxdata.decode()=="black":
		color = rxdata.decode()
		print("Your color is: "+ color)
	if rxdata.decode() == "gameon":
		print("Game is starting...")
		break

while True: # Temporary
	time.sleep(5)
	print("idle")

pygame.init()
# Display & Board Init
inf=pygame.display.Info()
swidth=inf.current_w
sheight=inf.current_h
screen=pygame.display.set_mode((swidth,sheight),flags=pygame.FULLSCREEN)
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

# Tx data to server
def send(call):
	global s
	s.sendall(bytes(str(call),'utf-8'))
	
# Scoreboard Drawing Function	
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

# Board Class
class board:
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
		self.turn="white" # move turns to server side

	def draw(self,player):
		screen.fill((0,0,0))
		pygame.draw.rect(screen,BoarderColor,pygame.Rect(Boardx,Boardy,BoardWidth,BoardHeight))
		for row in self.cells:
			for col in row:
				col.draw()
		screen.blit(drawScoreBoard(self.getCount("black"),self.getCount("white"),self.turn),(int(sheight*.93),100))	

# Cell Class
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

	def move(self,type): # may be confusing
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

# Intro and Setup
while True:
	game=board()

	game.cells[3][3].move("white")
	game.cells[4][4].move("white")
	game.cells[3][4].move("black")
	game.cells[4][3].move("black")
	wait=False
	#player="white" # needs to be done server side
	puttext(screen,(200,500),"WELCOME TO OTHELLO. LET'S PLAY!",80,(0,255,0),"Center")
	wait=True
	ex=False
#	send("ready") shouldn't be necessary

# Game Loop Rewrite
while True:
	rxdata = s.recv(1024) # Blocks thread from continuing

#	if rxdata.decode() == "game_over white" or rxdata.decode() == "game_over black" or rxdata.decode() == "game_over nobody":
#		result=rxdata.decode()
		# needs parsed here
#		puttext(screen,(200,500),"GAME OVER. "+result+" wins!",80,(255,0,0),"Center")
#		puttext(screen,(200,800),"Play Again?(Y/N)",80,(255,0,0),"Center")
#		gameover=True
#		wait=True
#	else:
#		pass # fix?
#	possibly check turn and then continue if this turn?

	ev=pygame.event.get()
	space=False
	mpos=0
	for event in ev:
		if event.type==pygame.KEYUP:
			if event.key==pygame.K_ESCAPE: # This is good
				s.close()
				exit()
		if event.type==pygame.MOUSEBUTTONUP and rxdata.decode()==color:
			mpos=pygame.mouse.get_pos()
			x=int((mpos[0]-Boardx-BoarderWidth)/(CellWidth+BoarderWidth))
			y=int((mpos[1]-Boardy-BoarderWidth)/(CellHeight+BoarderWidth))
			send(x+ y)
			while True:
				rxdata=s.recv(1024) # Blocks thread from continuing
				if rxdata.decode()=="Invalid Move":
					puttext(screen,(200,500),"INVALID MOVE!!!",80,(255,0,0),"Center")
					wait=True
					break
				if rxdata.decode()=="Valid Move":
					rxdata = s.recv(1024)
					game.flip_pieces(rxdata.decode(),color)

	if ex:
		ex=False
		break

	pygame.display.flip() # this stays
	if wait:
		time.sleep(2)
		wait=False	
		game.draw()
		pygame.display.flip()