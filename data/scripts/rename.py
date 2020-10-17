# Pythono3 code to rename multiple  
# files in a directory or folder 
  
import os 

path =  "downloads/bag chair/"

# Function to rename multiple files 
def main(): 
  
    for count, filename in enumerate(os.listdir(path)): 
        dst ="image" + str(count) + ".jpg"
        src = path + filename 
        dst = path+ dst 
        os.rename(src, dst) 
  
if __name__ == '__main__': 
    main() 