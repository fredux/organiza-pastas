import os
import sys
from pathlib import Path
import argparse
import yaml
 
#get thu user 
usuario =os.getlogin()

if sys.platform == "linux" :
    # linux
    downloads_path =  r'/home/{}/Downloads'.format(usuario)
elif sys.platform == "darwin":
    # OS X
    print("OS X")
elif sys.platform == "win32":
    # Windows...
    downloads_path =  r'c:\Users\{}\Downloads'.format(usuario)

#Get the file types
folder_names = {
    'Audio':['aif','cda','mid','midi','mp3','mpa','ogg','wav','wma'],
    'Compressed':['7z','deb','pkg','rar','rpm', 'tar.gz','z', 'zip', 'tgz'],
    'Code':['js','jsp','html','ipynb','py','java','css', 'go'],
    'Documents':['ppt','pptx','pdf','xls', 'xlsx','doc','docx','txt', 'tex', 'epub', 'csv', 'odt'],
    'Images':['bmp','gif','ico','jpeg','jpg','png', 'JPG','jfif','svg','tif','tiff', 'PNG', 'png'] ,
    'Softwares':['apk','bat','bin', 'exe','jar','msi'],
    'Videos':['3gp','avi','flv','h264','mkv','mov','mp4','mpg','mpeg','wmv', 'mkv'],
    'Others': ['NONE']
    }

def createYaml(file, folder_names):
    yaml_config = yaml.load(yaml.dump(folder_names), Loader=yaml.FullLoader)
    with open(file, "w") as outfile:  
        yaml.dump(yaml_config, outfile)
    

#if the yaml file exists open it and set the folder_names variable
if os.path.isfile('config.yaml'):
    with open('config.yaml', 'r') as f:
      folder_names = yaml.safe_load(f)
    
class DeclutterFolder:
    '''
    folders_path = Deve ser informado o path da pasta que será organizada
    folder_names deve ser no padrão: {'name': {'ext1', 'ext2'... '}, 'Others: ['NONE'}}

    Ex: 
    folder_names = {
        'Audio':['aif','cda','mid','midi','mp3','mpa','ogg','wav','wma'],
        'Compressed':['7z','deb','pkg','rar','rpm', 'tar.gz','z', 'zip', 'tgz'],
        'Code':['js','jsp','html','ipynb','py','java','css', 'go'],
        'Documents':{'ppt','pptx','pdf','xls', 'xlsx','doc','docx','txt', 'tex', 'epub', 'csv', 'odt'],
        'Images':['bmp','gif .ico','jpeg','jpg','png', 'JPG','jfif','svg','tif','tiff', 'PNG', 'png'] ,
        'Softwares':['apk','bat','bin', 'exe','jar','msi'],
        'Videos':['3gp','avi','flv','h264','mkv','mov','mp4','mpg','mpeg','wmv', 'mkv'],
        'Others': ['NONE']
     }
    '''
    
    def __init__(self, folders_path, folder_names):
        self.__folders_path = folders_path
        self.__folder_names = folder_names
        self.__onlyfiles = [os.path.join(self.__folders_path, file)  for file in os.listdir(self.__folders_path)  if os.path.isfile(os.path.join(self.__folders_path, file))]
        self.__onlyfolders = [os.path.join(self.__folders_path, file)  for file in os.listdir(self.__folders_path)  if not os.path.isfile(os.path.join(self.__folders_path, file))]
        self.__extension_filetype_map = {extension: fileType  for fileType, extensions in self.__folder_names.items() for extension in extensions }
        
    def makeFolders(self):
        folders = [os.path.join(self.__folders_path, folder_name)  for folder_name in self.__folder_names.keys()]
        [os.mkdir(folderPath) for folderPath in folders if not os.path.exists(folderPath)]
        
    def __new_path(self,old_path):
        extension = str(old_path).split('.')[-1]
        amplified_folder = self.__extension_filetype_map[extension] if extension in self.__extension_filetype_map.keys() else 'Others'
        final_path = os.path.join(self.__folders_path,amplified_folder, str(old_path).split(os.path.sep)[-1])
        return final_path
        
    def moveFiles(self):
        #move files to predefinied folders
        try: 
            [Path(eachfile).rename(self.__new_path(eachfile)) for eachfile in self.__onlyfiles]

        #Move other folders
            [Path(onlyfolder).rename(Path(os.path.join(self.__folders_path,'Others', str(onlyfolder).split(os.path.sep)[-1])))
                for onlyfolder in self.__onlyfolders if str(onlyfolder).split(os.path.sep)[-1] not in self.__folder_names.keys()]
        except FileExistsError as err:
            print(err)
            return
        print("Pastas {} organizadas! ".format(self.__folders_path)) 

    def moveFilesReplace(self):
        #Move  files/folders. does not work for renaming folders that already exist in the predefinied folders
        try: 
            [Path(eachfile).replace(self.__new_path(eachfile)) for eachfile in self.__onlyfiles]
    
            [Path(onlyfolder).replace(Path(os.path.join(self.__folders_path,'Others', str(onlyfolder).split(os.path.sep)[-1])))
                for onlyfolder in self.__onlyfolders if str(onlyfolder).split(os.path.sep)[-1] not in self.__folder_names.keys()]
        except  Exception as err:
            print(err)
            return

        print("Pastas {} organizadas! ".format(self.__folders_path)) 
    

parser = argparse.ArgumentParser(description='Declutter folder.',  epilog='Enjoy the program! :)')
parser.add_argument('-p', '--path', type=str,  help='Enter folder to declutter', required=False)

args = parser.parse_args()

if (not os.path.isdir(str(args.path)) and args.path != None):
    print('The path specified does not exist')
    sys.exit()

if (args.path !=None):
    downloads_path = args.path

organiza = DeclutterFolder(downloads_path, folder_names)
organiza.makeFolders()
organiza.moveFilesReplace()




