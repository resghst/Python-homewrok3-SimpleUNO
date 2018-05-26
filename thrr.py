import socket, threading, time, json    

def  doWaiting():    
    print('\t[Info] start waiting...{0}' , time.strftime( '%H:%M:%S' ))    
    time.sleep( 5 )    
    print('\t[Info] stop waiting...{0}' , time.strftime( '%H:%M:%S' ))    

def  doWaiting1():   
    d = open( 'd3.txt' , 'r+')
    a=d.read()
    print str(a)
    d3_card = json.loads(a)
    print str(d3_card)
    d.close()
thread1 = threading.Thread(target = doWaiting)    
thread1.start()  
thread2 = threading.Thread(target = doWaiting1)    
thread2.start() 
print('end join')  