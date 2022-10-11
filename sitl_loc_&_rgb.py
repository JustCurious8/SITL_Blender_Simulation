import pymavlink.mavutil as mavutil
import sys
import time
import threading
import json
import time
import asyncio
import numpy as np

# -*- coding: utf-8 -*-

# GUI implementation generated from reading ui file 'GUI.ui'
from PyQt4 import QtCore, QtGui
from functools import partial
from PyQt4 import QtTest
#from mqtt_protocol import mqtt
import os
import socket
import threading
			 
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



no_of_inst=72
#z={"R_ID":[0]*no_of_inst, "G_ID":[0]*no_of_inst, "B_ID":[0]*no_of_inst, "X_ID":[0]*no_of_inst, "Y_ID":[0]*no_of_inst, "Z_ID":[0]*no_of_inst}
z={"R_ID":[0]*no_of_inst, "G_ID":[0]*no_of_inst, "B_ID":[0]*no_of_inst, "X_ID":[0]*no_of_inst, "Y_ID":[0]*no_of_inst, "Z_ID":[0]*no_of_inst}

def findxy(lat1,lon1,lat2,lon2):
        return (lat2-lat1)*111*1000, (lon2-lon1)*(2*(np.pi)/360)*6371*(np.cos(lat1*np.pi/180))*1000

async def showing_messages(mav,num):
    while True:
      try:
        await asyncio.sleep(0.001)
        #await asyncio.sleep(0.1)


        '''
        msg=mav.recv_match(blocking=True)
        msg=msg.to_dict()
        if(msg['mavpackettype']=="GLOBAL_POSITION_INT"):
           x,y=findxy(28.5432059,77.1901801,round(msg["lat"]*1e-7,7),round(msg["lon"]*1e-7,7))
           z["X_ID"][num-1]=x
           z["Y_ID"][num-1]=y
           z["Z_ID"][num-1]=round(msg["relative_alt"]*1e-3,2)
    

     
        elif(msg['mavpackettype']=="RC_CHANNELS"):
           z["R_ID"][num-1]=msg["chan11_raw"]
           z["G_ID"][num-1]=msg["chan12_raw"]
           z["B_ID"][num-1]=msg["chan13_raw"]


        elif(msg['mavpackettype']=="COMMAND_ACK"):
             print(msg)
             print("\n\n")


        #print(msg["chan11_raw"])
        #print(msg.to_dict())
        #msg=msg.to_dict()
        #print(msg["chan11_raw"])
        '''

        msg1=mav.recv_match(type = 'RC_CHANNELS',blocking=True,timeout=0.1)
        msg2=mav.recv_match(type = 'GLOBAL_POSITION_INT',blocking=True,timeout=0.1)
        #msg3=mav.recv_match(type = 'COMMAND_ACK',blocking=True,timeout=0.2)
        #msg1=mav.recv_match(type = 'RC_CHANNELS',blocking=True)
        #msg2=mav.recv_match(type = 'GLOBAL_POSITION_INT',blocking=True)
        #msg3=mav.recv_match(type = 'COMMAND_ACK',blocking=True)
        #print(msg1,msg2)
        #if(msg3):
        #  print(msg3)

        z["R_ID"][num-1]=msg1.chan11_raw
        z["G_ID"][num-1]=msg1.chan12_raw
        z["B_ID"][num-1]=msg1.chan13_raw
 
        x,y=findxy(28.5442646,77.1886164,round(msg2.lat*1e-7,7),round(msg2.lon*1e-7,7))
        #x,y=findxy(28.5432059,77.1901801,28.5432059,77.1901801)
        z["X_ID"][num-1]=x
        z["Y_ID"][num-1]=y
        #z["X_ID"][num-1]=round(msg2.lat*1e-7,7)
        #z["Y_ID"][num-1]=round(msg2.lon*1e-7,7)
        z["Z_ID"][num-1]=round(msg2.relative_alt*1e-3,2)

      except KeyboardInterrupt:
        print('User you have pressed ctrl-c button.')
        sys.exit()  

      except: 
        pass


#port=14550
port=5770
mav=[None]*no_of_inst
for i in range(no_of_inst):
   #mav.append(mavutil.mavlink_connection('tcp:127.0.0.1:'+str(port+(i*10)), baud=115200))
   try:
      mav[i]=mavutil.mavlink_connection('tcp:127.0.0.1:'+str(port+(i*10)), baud=115200, retries=1)
      #mav[i]=mavutil.mavlink_connection('udp:0.0.0.0:'+str(port+i*10), baud=115200)
   
   except:
      pass

   #mav[i]=mavutil.mavlink_connection('udp:0.0.0.0:'+str(port+i*10), baud=115200)
   #print(port+i*10)

#print("past")
for i in range(no_of_inst):
  try:
     mav[i].wait_heartbeat()

  except:
     pass


for i in range(no_of_inst):
  try:
    mav[i].mav.command_long_send(mav[i].target_system,mav[i].target_component,mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,0,65,50000,0,0,0,0,0)
    mav[i].mav.command_long_send(mav[i].target_system,mav[i].target_component,mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,0,33,50000,0,0,0,0,0)
  
  except:
    pass
   
   #mav[i].mav.command_long_send(mav[i].target_system,mav[i].target_component,mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,0,77,50000,0,0,0,0,0)
   #mav[i].mav.command_long_send(mav[i].target_system,mav[i].target_component,mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,0,0,50000,0,0,0,0,0)

'''
for i in range(len(mav)):
   print(mav[i])
'''
async def try1():
  while True:
    await asyncio.sleep(0.1)
    print(z["Z_ID"])
    s.sendto(json.dumps(z).encode(),(UDP_IP_ADDRESS, UDP_PORT_NO))


loop = asyncio.get_event_loop()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)



class Ui_GUI(object):
    
    def __init__(self,mav):  	
        self.arming_signal=0
        self.guided_signal=0
        self.instance=0
        #self.mqtt=mqtt
        self.Mav=mav
        self.data_packet={"messageid": 0, "payload": { } }


        app = QtGui.QApplication(sys.argv)
        self.GUI = QtGui.QWidget() 
        self.setupUi(self.GUI)
        self.GUI.show()
        sys.exit(app.exec_())


        

    def setupUi(self, GUI):
        #FRAME
        GUI.setObjectName(_fromUtf8("GUI"))
        GUI.resize(250, 280)
        GUI.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);"))
        self.label_Title = QtGui.QLabel(GUI)
        self.label_Title.setGeometry(QtCore.QRect(180, 180, 541, 51))

        self.label = QtGui.QLabel(GUI)
        self.label.setGeometry(QtCore.QRect(40, 30, 71, 31))
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 170, 0);\n"
"color: rgb(0, 0, 0);"))
        self.label.setObjectName(_fromUtf8("label"))


        '''
        #ARMING
        self.pushButton_ARMING_1 = QtGui.QPushButton(GUI)
        self.pushButton_ARMING_1.setGeometry(QtCore.QRect(40, 30, 71, 31))
        self.pushButton_ARMING_1.setStyleSheet(_fromUtf8("background-color: rgb(255, 170, 0);\n"
"color: rgb(0, 0, 0);"))
        self.pushButton_ARMING_1.setObjectName(_fromUtf8("pushButton_ARMING_1"))
        self.pushButton_ARMING_1.clicked.connect(partial(self.ARMING))
        '''

        self.take_input = QtGui.QLineEdit(GUI)
        self.take_input.setGeometry(QtCore.QRect(140, 30, 71, 31))
        self.take_input.setObjectName(_fromUtf8("get_input"))
        self.take_input.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);"))
        self.take_input.setText("")


        #ARMING
        self.pushButton_ARMING_1 = QtGui.QPushButton(GUI)
        self.pushButton_ARMING_1.setGeometry(QtCore.QRect(40, 80, 71, 31))
        self.pushButton_ARMING_1.setStyleSheet(_fromUtf8("background-color: rgb(255, 170, 0);\n"
"color: rgb(0, 0, 0);"))
        self.pushButton_ARMING_1.setObjectName(_fromUtf8("pushButton_ARMING_1"))
        self.pushButton_ARMING_1.clicked.connect(partial(self.ARMING))

        #GUIDED
        self.pushButton_GUIDED_1 = QtGui.QPushButton(GUI)
        self.pushButton_GUIDED_1.setGeometry(QtCore.QRect(40, 130, 71, 31))
        self.pushButton_GUIDED_1.setStyleSheet(_fromUtf8("background-color: rgb(255, 170, 0);\n"
"color: rgb(0, 0, 0);"))
        self.pushButton_GUIDED_1.setObjectName(_fromUtf8("pushButton_GUIDED_1"))
        self.pushButton_GUIDED_1.clicked.connect(partial(self.GUIDED))


        #LAND
        self.pushButton_LAND_1 = QtGui.QPushButton(GUI)
        self.pushButton_LAND_1.setGeometry(QtCore.QRect(40, 180, 71, 31))
        self.pushButton_LAND_1.setStyleSheet(_fromUtf8("background-color: rgb(255, 170, 0);\n"
"color: rgb(0, 0, 0);"))
        self.pushButton_LAND_1.setObjectName(_fromUtf8("pushButton_LAND_1"))
        self.pushButton_LAND_1.clicked.connect(partial(self.LAND))


        self.retranslateUi(GUI)
        QtCore.QMetaObject.connectSlotsByName(GUI)

    def retranslateUi(self, GUI):
        GUI.setWindowTitle(_translate("GUI", "GUI", None))
        self.label.setText(_translate("GUI", "Instance:", None))
        self.pushButton_ARMING_1.setText(_translate("GUI", "ARMING", None))
        self.pushButton_GUIDED_1.setText(_translate("GUI", "GUIDED", None))
        self.pushButton_LAND_1.setText(_translate("GUI", "LAND", None))

    def user_input(self):
           self.instance = int(self.take_input.text())

    def ARMING(self):
           self.user_input()

           if(self.instance == 255):
             for i in range(len(self.Mav)):
               try:
                 self.Mav[i].mav.command_long_send(self.Mav[i].target_system,self.Mav[i].target_component,mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0,1, 0, 0, 0, 0, 0, 0)  
               except: 
                 pass

           elif(self.instance>0 and self.instance<255):
                 self.Mav[self.instance-1].mav.command_long_send(self.Mav[self.instance-1].target_system,self.Mav[self.instance-1].target_component,mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0,1, 0, 0, 0, 0, 0, 0) 

           print(self.instance) 
           #return 1

    def GUIDED(self):
          self.user_input()

          if(self.instance == 255):
             for i in range(len(self.Mav)):
               try:
                 self.Mav[i].mav.set_mode_send(self.Mav[i].target_system,mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,4)
                 #self.Mav[i].mav.command_long_send(self.Mav[i].target_system,self.Mav[i].target_component,mavutil.mavlink.MAV_CMD_DO_FLIGHTTERMINATION ,0,1,0,0,0,0,0,0)
               except: 
                 pass

          elif(self.instance>0 and self.instance<255):
               self.Mav[self.instance-1].mav.set_mode_send(self.Mav[self.instance-1].target_system,mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,4)
               #self.Mav[self.instance-1].mav.command_long_send(self.Mav[self.instance-1].target_system,self.Mav[self.instance-1].target_component,mavutil.mavlink.MAV_CMD_DO_FLIGHTTERMINATION ,0,1,0,0,0,0,0,0)
  
          print(self.instance) 
          #return 1



    def LAND(self):
          self.user_input()

          if(self.instance == 255):
             for i in range(len(self.Mav)):
               try:
                 self.Mav[i].mav.set_mode_send(self.Mav[i].target_system,mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,9)
               except: 
                 pass

          elif(self.instance>0 and self.instance<255):
               self.Mav[self.instance-1].mav.set_mode_send(self.Mav[self.instance-1].target_system,mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,9)

          print(self.instance)
          #return 1

def start_gui(mav):
        ui=Ui_GUI(mav)  
                        

def start_gui_thread(mqtt):
         message = threading.Thread(target=start_gui,args=(mav,))
         message.start()
         return(message)


def stop_message(message):
         message.do_run = False
         message.join()

'''
async def start_gui(mav):
     ui=Ui_GUI(mav)
'''

try:
    for i in range(no_of_inst):
      asyncio.ensure_future(showing_messages(mav[i],i+1))

    asyncio.ensure_future(try1())
    #asyncio.ensure_future(start_gui(mav))

    message=start_gui_thread(mav)
    #asyncio.ensure_future(try2())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    stop_message(message)
    myCmd = 'kill '+str(os.getpid())
    print("exit")
    os.system(myCmd)
    loop.close()
