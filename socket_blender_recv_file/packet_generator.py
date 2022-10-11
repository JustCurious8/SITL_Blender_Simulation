from decimal import Decimal
import time,json
import bpy
import sys


class decoder_packet:
    def __init__(self,instance,total_drone):
         self.instance=instance
         self.total_drone=total_drone
         self.check=0

                                
     
    def decoder_data(self,RecieveData,addr):
        '''
        if(RecieveData["R_ID"][0]>0 and self.check==0):
            self.check=1
        '''

        for i in range(self.total_drone):
            X=RecieveData["X_ID"][i]
            Y=RecieveData["Y_ID"][i]
            Z=RecieveData["Z_ID"][i]
            R=RecieveData["R_ID"][i]/255.0
            G=RecieveData["G_ID"][i]/255.0
            B=RecieveData["B_ID"][i]/255.0
            #T=RecieveData["time_RAW"][i]

            self.instance.cube_object[i].location = X,Y,Z
            self.instance.cube_object[i].active_material.diffuse_color = (R,G,B,1) #change color
        print(Z)     

    '''
    def decoder_data2(self,RecieveData,addr):

        for i in range(self.total_drone):
            #X=RecieveData["X_ID"][i]
            #Y=RecieveData["Y_ID"][i]
            #Z=RecieveData["Z_ID"][i]
            R=RecieveData["R_ID"][i]/255.0
            B=RecieveData["B_ID"][i]/255.0
            G=RecieveData["G_ID"][i]/255.0
            #T=RecieveData["time_RAW"][i]

            #self.instance.cube_object[i].location = X,Y,Z
            self.instance.cube_object[i].active_material.diffuse_color = (R,B,G,1) #change color
        print(R)
    '''
    
    def update_drone(self):
        self.instance.cube_object[self.ID-1].location = self.X,self.Y,self.Z
        self.instance.cube_object[self.ID-1].active_material.diffuse_color = (self.R,self.B,self.G,1) #change color
       	      		       

