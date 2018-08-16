import GetNewFilePath
import paramiko
import datetime
date=datetime.datetime.today().strftime('%Y%m%d_%H%M')
path = r'F:\data_resource\test1\result_filename.txt'
severse_path = '/home/appSys/RIOpenApi4UMC'
new_path=(GetNewFilePath.new_filenamepath(path,severse_path))
def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport(GetNewFilePath.conf['host_ip'], GetNewFilePath.conf['port'])
        t.connect(username=GetNewFilePath.conf['username'], password=GetNewFilePath.conf['password'])
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print (e)
if new_path==None:
    print('服务器还没有上传新文件，数据没有提取完！')
else:
    sftp_down_file(new_path, r"F:\data_resource\test\%s.txt"%(date))
