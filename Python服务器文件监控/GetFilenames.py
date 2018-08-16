import os
def getfilename(path):
    for (path,path_,filename) in os.walk(path):
        return filename