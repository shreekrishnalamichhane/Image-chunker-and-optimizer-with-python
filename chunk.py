# import OS module
import os
import sys
import shutil
from compress import compress_img, get_size_format

def progress(count, total, prefix=''):
    bar_len = 60

    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('%s  [%s] %s%s \r' % (prefix,bar, percents, '%'))
    sys.stdout.flush()  # As suggested by Rom Ruben

# Get the list of all files and directories
path = "./"

files = os.listdir(path+"src/")
# print(files)

chunkIndex = 0
chunkCount = 1
totalItems = len(files)
currentItems = 0
totalSave = 0
chunkSize = int(input("Enter the number of files in one chunk : "))
quality = float(input("Enter the quality [0-100]: "))
ratio = float(input("Enter the ratio [0.0-1.0] : "))

for x in files:
    currentItems += 1
    if os.path.isfile(os.path.join(path+"src/", x)):
        if chunkIndex >= chunkSize:
            chunkIndex = 0
            chunkCount += 1
        if x != os.path.basename(sys.argv[0]):
            chunkIndex += 1
        try:
            os.mkdir(os.path.join(path , "dst/Chunk "+str(chunkCount)),0o666)
            pass
        except:
            pass
        totalSave+= compress_img(path+"src/" , path+"dst/Chunk " + str(chunkCount) , x , ratio , quality)
            # shutil.copyfile(os.path.join(path, x), os.path.join(path+"Chunk " + str(chunkCount),x))
        progress(currentItems,totalItems,"Progress : " + x)

if currentItems == totalItems:
    print('Transaction Complete!')
    if(totalSave <0):
        print(f"Total Storage Freed : -{ get_size_format(-totalSave)}")
    else:
        print(f"Total Storage Freed : { get_size_format(totalSave)}")
