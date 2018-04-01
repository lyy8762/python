import os
import exifread


def getExif(path,filename):
    FIELD = 'EXIF DateTimeOriginal'
    fd = open(filename, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    if FIELD in tags:
        new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + os.path.splitext(filename)[1]
        tot = 1
        while os.path.exists(new_name):
            new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + '_' + str(tot) + \
                       os.path.splitext(filename)[1]
            tot += 1

        new_name2 = path+'\\'+new_name
        print(new_name2)
        os.rename(filename, new_name2)
    else:
        print('No {} found'.format(FIELD))



if __name__ == '__main__':
    path='D:\\Projects\\python\\lyy\\pic'
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path,file)):
            getExif(path,os.path.join(path,file))
