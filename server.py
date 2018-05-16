import socket 
import random
import json

def generate_card(pile):
	card = ['B', 'G', 'R', 'Y']
	j, p, pc, pos = 0, 0, 0, -1
	for j in range(0,8):
		pc=0
		for i in range(1,6):
			pos+=1
			if(j<=3): pile[pos] = card[j] + str(i)
			elif(p<4):
				pc+=1
				pile[pos] = 'Plus2_' + card[p]
				if(pc==2): 
					p+=1
					break
	return pile
	
def div_card(pile, pile1, pile2, pile3):
	pile1_i, pile2_i, pile3_i = 0, 0, 0
	a = random.sample(xrange(30), 30)
	for i in range(30):
		if(i<5): 
			pile1[pile1_i] = pile[a[i]]
			pile1_i+=1
		elif(i<10):
			pile2[pile2_i] = pile[a[i]]
			pile2_i+=1
		else:
			pile3[pile3_i] = pile[a[i]]
			pile3_i+=1
	return pile1, pile2, pile3

def send_card(port, message, message1):
	s = socket.socket()         
	host = socket.gethostname()   
	s.connect((host, port))
	s.send(message)
	s.send(message1)
	print s.recv(1024)
	s.close()  


if __name__ == '__main__':

	s = socket.socket()
	host = socket.gethostname()
	port = 12345
	s.bind((host, port)) 
	s.listen(5)

	ready=0
	jspile1, jspile2, jspile3 = [], [], []
	pile = ["" for i in range(30)]
	pile1 = ["" for i in range(5)]
	pile2 = ["" for i in range(5)]
	pile3 = ["" for i in range(20)]
	while True:
		inst = raw_input('input The command:')
		if(inst=="g"):#generate_card
			pile = generate_card(pile)
			print pile
			ready+=1
		elif(inst=="d"):#div_card
			divpile=[[]for i in range(3)]
			divpile[0], divpile[1], divpile[2] = div_card(pile, pile1, pile2, pile3)
			for i in range(1,4):
				d = open( 'd' + str(i) + '.txt' , 'w+')
				d.write(str(divpile[i-1]))
				d.close()
			jspile1 = json.dumps(pile1)
			jspile2 = json.dumps(pile2)
			print pile1
			print pile2
			print pile3
		elif(inst=='s'): #send_card
			send_card(12345, jspile1, jspile2)
			send_card(12346, jspile1, jspile2)


		# while True:
		# 	if( ready==1 ):
		# 		c, addr = s.accept()
		# 		print  addr
		# 		c.send('helllo')
		# 		c.close()