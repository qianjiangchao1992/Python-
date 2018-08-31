import GetNewFilePath
import paramiko
import os
import time
path = r'F:\data_resource\file_xzt\filenames\basic_filename.txt'
severse_path = '/home/appSys/RIOpenApi4UMC/xzt1/basic'
new_path=(GetNewFilePath.new_filenamepath(path, severse_path))
def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport(GetNewFilePath.conf['host_ip'], GetNewFilePath.conf['port'])
        t.connect(username=GetNewFilePath.conf['username'], password=GetNewFilePath.conf['password'])
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print (e)
def getfilename(path):
    for (path, path_, filename) in os.walk(path):
        return filename
data_path=[]
if len(new_path)==0:
    print('服务器还没有上传basic新文件！')
else:
    print("发现新basic文件")
    start_time = time.time()
    for name in new_path:
        paths=name
        localfilename=name.split('/')[-1]
        sftp_down_file(paths, r"F:\data_resource\file_xzt\basic\%s"%(localfilename))
        data_path.append(r"F:\data_resource\file_xzt\basic\%s" % (localfilename))
    end_time = time.time()
    print('下载新basic文件所花时间为%f' % (end_time - start_time))





