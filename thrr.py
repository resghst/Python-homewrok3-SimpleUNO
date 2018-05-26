import socket, threading, time    

def  doWaiting():    
    print('\t[Info] start waiting...{0}' , time.strftime( '%H:%M:%S' ))    
    time.sleep( 5 )    
    print('\t[Info] stop waiting...{0}' , time.strftime( '%H:%M:%S' ))    

def  doWaiting1():    
    print('cscs' )    
    inst = raw_input('input The command:')   
    print(inst)    
thread1 = threading.Thread(target = doWaiting)    
thread1.start()  
thread2 = threading.Thread(target = doWaiting1)    
thread2.start() 
print('end join')  