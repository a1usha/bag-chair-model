# Pythono3 code to rename multiple  
# files in a directory or folder 
  
# importing os module 
import os 

path =  "downloads/bag chair/"

# Function to rename multiple files 
def main(): 
  
    for count, filename in enumerate(os.listdir(path)): 
        dst ="image" + str(count) + ".jpg"
        src = path + filename 
        dst = path+ dst 
          
        # rename() function will 
        # rename all the files 
        os.rename(src, dst) 
  
# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 