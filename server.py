import socket, random, json, threading, time
inaction = ''
beforecard = ''
ready=0

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
	a = random.sample(xrange(28), 28)
	for i in range(28):
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
	print "send card..."
	send = socket.socket()
	host = socket.gethostname()   
	print str(host) + "  " + str(port)
	send.connect((host, port))
	data = 'send_card|' + str(message) + '\n' + str(message1)
	send.send(data)
	send.close()

def send_finish(port, message):
	time.sleep(1)
	# print "send finish..."
	send = socket.socket()
	host = socket.gethostname()   
	# print str(host) + "  " + str(port)
	send.connect((host, port))
	data = 'rec_card|' + str(message)
	send.send(data)
	send.close()

def send_current(port, message):
	time.sleep(1)
	# print "send current..."
	send = socket.socket()
	host = socket.gethostname()   
	# print str(host) + "  " + str(port)
	send.connect((host, port))
	data = 'read_current|' + str(message)
	send.send(data)
	send.close()

def serveraction():
	global ready
	jspile1, jspile2, jspile3 = [], [], []
	pile = ["" for i in range(28)]
	pile1 = ["" for i in range(5)]
	pile2 = ["" for i in range(5)]
	pile3 = ["" for i in range(18)]
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
			print str(pile1)+ "\n" + str(pile2) + "\n" + str(pile3)
			ready+=1
		elif(inst=='s'): #send_card
			send_card(12345, jspile1, jspile2)
			send_card(12346, jspile1, jspile2)
			ready+=1
		elif(inst=='r'): #rec_card
			global inaction, beforecard
			data = inaction.split(",")
			member = data[0]
			card = data[1]
			beforecard = card
			d = open( 's_now.txt' , 'a+')
			d.write(inaction)
			d.close()
			if( member == 'c1' ): send_finish(12345,card)
			elif(member == 'c2'): send_finish(12346,card)


def getdata():
	global inaction, ready
	reciver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()
	port = 12344
	reciver.bind((host, port)) 
	reciver.listen(5)
	while True:
		if(ready == 3):
			c, addr = reciver.accept()
			data = c.recv(1024)
			inaction = data
	c.close()


def corrent():
	global inaction
	while True:
		if(ready == 3):
			send_current(12345,inaction)
			send_current(12346,inaction)
	c.close()

if __name__ == '__main__':


	thread1 = threading.Thread(target = serveraction)
	thread2 = threading.Thread(target = getdata)
	thread3 = threading.Thread(target = corrent)
	thread1.start()
	thread2.start()
	thread3.start()
	thread2.join()
	thread1.join()
	thread3.join()
	print('end join')  
