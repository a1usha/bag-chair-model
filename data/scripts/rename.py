# Pythono3 code to rename multiple  
# files in a directory or folder 
  
import os 
from PIL import Image

path =  "data/imagess/"
pathth =  "data/imagesss/"

# Function to rename multiple files 
def main(): 
  
    for count, filename in enumerate(os.listdir(path)): 

        name = filename.split('.')[0] + '.png'

        im = Image.open(path + filename)
        im.save(pathth + name)

if __name__ == '__main__': 
    main() 