import os
import exifread
import shutil
import random


def getExif(filename):
    FIELD = 'EXIF DateTimeOriginal'
    fd = open(filename, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    if FIELD in tags:
        newname = str(tags[FIELD]).replace(':', '').replace(' ', '_')
        return newname+os.path.splitext(filename)[1]
    else:
        print('No {} found'.format(FIELD))

def renamefile(path,file,newname):
    while os.path.exists(os.path.join(path, newname)):
        newname=os.path.splitext(newname)[0]+str(random.randint(0,9))+os.path.splitext(newname)[1]
    os.rename(os.path.join(path, file), os.path.join(path, newname))

def removefile(file,path,dir):
    shutil.copyfile(path + '\\' + file, dir + '\\' + file)

if __name__ == '__main__':
    #path='D:\\Projects\\python\\lyy\\pic'
    path='C:\\Users\\lyy\\Desktop\\picture\\dir'

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path,file)):
            newname=getExif(os.path.join(path,file))
            dir=os.path.join(path,newname[0:6])
            if not os.path.isdir(dir):
                os.makedirs(dir)
            removefile(file,path,dir)
            renamefile(dir,file,newname)