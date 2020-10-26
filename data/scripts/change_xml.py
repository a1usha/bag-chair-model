from xml.etree import ElementTree
import os 

folder = 'imagesss'
path_to_set = 'data/imagesss/'
path =  "data/annotations/"

def main(): 
  
    for count, filename in enumerate(os.listdir(path)): 
        
        tree = ElementTree.parse(path + filename)
        root = tree.getroot()

        name = root.find("filename").text
        name = name.split('.')[0] + '.png'
        root.find("filename").text = name

        root.find("folder").text = folder
        root.find("path").text = path_to_set + name

        tree.write(path + filename)
  
if __name__ == '__main__': 
    main() 