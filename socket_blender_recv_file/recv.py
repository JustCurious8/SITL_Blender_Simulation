#dependency library
from decimal import Decimal
import os,sys,time,math,json,logging
import bpy,functools


# first of all import the socket library 
import socket			 
# next create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		 
print("Socket successfully created")

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 	
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12345
port=12345		

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))		 
print("socket binded to %s" %(port))
start=time.time()

#class library
#from blender_recv_file.mqtt_protocol import mqtt

#class decoder
from socket_blender_recv_file.packet_generator import decoder_packet

#class blender_instance
from socket_blender_recv_file.blender_api import *


def update(decoder):
        data, addr = s.recvfrom(3072)
        #print(len(data))
        data2=json.loads(data)
        #print(data)
        decoder.decoder_data(data2,addr)
        return 0.01
 
'''
def update2(decoder):
        data, addr = s2.recvfrom(3072)
        #print(len(data))
        data2=json.loads(data)
        print(data)
        decoder.decoder_data(data2,addr)
        return 0.01
'''

if __name__ == "__main__":
   #drone parameter
   ID=256
   Drone_no=49
   
   #clearing  object 
   blender_clearing_instance()
   
   #creating drone_instance
   instance=blender_instance(Drone_no)

   #decoder_packet
   decoder=decoder_packet(instance,Drone_no)  
  
   
   #listening the drone prameter by intialising blender timer    
   recv_thread = functools.partial(update,decoder)
   #recv_thread2 = functools.partial(update2,decoder)
   bpy.app.timers.register(recv_thread)
   #bpy.app.timers.register(recv_thread2)

