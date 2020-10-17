"""



"""

from xml.etree import ElementTree
import os 

folder = 'images'
path_to_set = 'download_data/downloads/images/'
path =  "downloads/labels/"

def main(): 
  
    for count, filename in enumerate(os.listdir(path)): 
        
        tree = ElementTree.parse(path + filename)
        root = tree.getroot()

        name = root.find("filename").text

        root.find("folder").text = folder
        root.find("path").text = path_to_set + name

        tree.write(path + filename)
  
if __name__ == '__main__': 
    main() 