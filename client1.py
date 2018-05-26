import socket, threading, time, json
endgame = False
d1_card, d2_card, d3_card = [], [], []
nowcard = ''

def reflashnow(action):
	global nowcard
	if(action == 'r'):
		d = open( 'now.txt' , 'r+')
		nowcard = d.read()
		d.close()
	elif(action == "w"):
		d = open( 'now.txt' , 'w+')
		d.write(nowcard)
		d.close()

def send_card(message):
	print "send card..."
	send = socket.socket()
	host = socket.gethostname()
	send.connect((host, 12344))
	data = str(message) + '\n'
	send.send(data)
	send.close()

def recvcontrol():
	global endgame, d1_card, d2_card, nowcard
	reciver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()
	port = 12346
	reciver.bind((host, port)) 
	reciver.listen(5)
	while not endgame:
		c, addr = reciver.accept()
		data = c.recv(1024)
		data = data.split("|")
		if(data[0] == 'send_card'):
			data = data[1]
			data = data.split("\n")
			d = open( 'c1.txt' , 'w+')
			d.write(data[0])
			d.close()
			d1_card = json.loads(data[0])
			d2_card = json.loads(data[1])
			print str(d1_card) + "\n" +str(d2_card)
		elif(data[0] == 'rec_card'):
			data = data[1]
		elif(data[0] == 'read_current'):
			data = data[1]
			data = data.split("\n")
			if(data[0]=='c2'):
				nowcard = data[1]
				d = open( 'now.txt' , 'w+')
				d.write(nowcard)
				d.close()
				if(nowcard[0]=='P'):
					card = ['B', 'G', 'R', 'Y']
					for i in range(4):
						if( nowcard[6] == card[i] ):
							d1_card.extend([ card[i]+'1', card[i]+'2' ])
							d = open( 'c1.txt' , 'w+')
							d.write(json.dumps(d1_card))
							d.close()

	c.close()


def useraction():
	global endgame, d1_card, d2_card, d3_card, nowcard
	while not endgame:
		inst = raw_input('input The command:')
		if inst == 'see': #see_mycard
			print d1_card
			d = open( 'c1.txt' , 'w+')
			print d.read()
			d.close()
		elif inst == 'read': #read_current
			print nowcard
		elif inst == 'please': #recommend_card
			if(nowcard[0]=='P'): tcolor = nowcard[6]
			else: tcolor = nowcard[0]
			for i in d1_card:
				if(i[0]=='P'): mycolor = i[6]
				else: mycolor = i[0]
				if(mycolor == tcolor): 
					print i
					continue
			d = open( 'd3.txt' , 'r+')
			d3_card = d.read()
			d.close()
			pick_card =  d3_card[0]
			d3_card.remove(pick_card)
			d1_card.append(pick_card)
			d = open( 'c1.txt' , 'w+')
			d.write(json.dumps(d1_card))
			d.close()
			d = open( 'd3.txt' , 'w+')
			d.write(json.dumps(d3_card))
			d.close()
		elif inst == 'send': #send_card
			card = raw_input('input The send card:')
			send_card(card)
			d1_card.remove(card)
			d = open( 'c1.txt' , 'w+')
			d.write(d1_card)
			d.close()

if __name__ == "__main__":
	thread1 = threading.Thread(target = recvcontrol)
	thread2 = threading.Thread(target = useraction)
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()
	print('end join')  
