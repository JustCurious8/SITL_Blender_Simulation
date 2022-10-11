from decimal import Decimal
import time,json
import bpy


class  blender_instance:
    def __init__(self,object_no):
         self.verts =[(0,0,0),(0,1.5,0),(1.5,1.5,0),(1.5,0,0),(0,0,1.5),(0,1.5,1.5),(1.5,1.5,1.5),(1.5,0,1.5)]
         self.faces =[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
         self.mat = [None]*object_no         
         self.cube=[None]*object_no
         self.cube_object=[None]*object_no

         for i in range(object_no):
          self.mat[i] = bpy.data.materials.new(name="MaterialName") #set new material to variable
 
         
         for i in range(object_no):             
          self.cube[i] = bpy.data.meshes.new('Cube')
          self.cube_object[i] = bpy.data.objects.new("Cube",self.cube[i])
          self.cube_object[i].location = 0,0,0
          bpy.context.collection.objects.link(self.cube_object[i])
          self.cube[i].from_pydata(self.verts,[],self.faces)
          self.cube[i].update(calc_edges=True)


         for i in  range(object_no):    
           self.cube_object[i].data.materials.append(self.mat[i]) #add the material to the object 
           self.cube_object[i].active_material.diffuse_color = (1,0,0,1) #change color
  

def blender_clearing_instance():
    try:  
  
       # Deleting all 
       bpy.ops.object.select_all(action='SELECT') 
       bpy.ops.object.delete()  

       for material in bpy.data.materials:
          bpy.data.materials.remove(material)


    except:
       loop_error()



def loop_error():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("thread is closed")
        print("Error is occurred")
        print("line no :"+str(exc_traceback.tb_lineno))
        print("error message :"+str(exc_value))
        print(os.getpid())
        myCmd = 'kill '+str(os.getpid())
        os.system(myCmd)

   
   
                         

