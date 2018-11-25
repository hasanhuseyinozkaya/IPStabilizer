from json import load
import json
from urllib2 import urlopen#this line represents with python 3.7 , in python 2.7 this line should be "from urllib2 import urlopen"
import socket
import time
import datetime
import pymongo
import os
def GetMachineFreeSpace():
	stat = os.statvfs('/') #this is for linux
	return str(((stat.f_bsize * stat.f_bavail)/1024)/1024)
def InsertIPsToMongo(publicIp):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		client = pymongo.MongoClient("mongodb+srv://<UserName>:<Password>@ipclusters-7xwxg.mongodb.net/test?retryWrites=true")
		db = client.ipdb
		ipcollection = db.ipcollection
		data ={}
		data['IP']=str(publicIp)
		data['MachineIP']=str(s.getsockname()[0])
		data['IPType']=1
		data['IPCreateDateTime'] = str(datetime.datetime.now())
		data['SystemFreeSpace'] = GetMachineFreeSpace()
		currentPublicIP = json.dumps(data)
		ipcollection.insert_one(data)
		s.close()

def SetAndStabilizePublicIP():
	try:
		my_ip = load(urlopen('http://jsonip.com'))['ip']
		InsertIPsToMongo(my_ip)
		print(my_ip)
	except Exception as e:
		print(e)

if __name__ == '__main__':
	while True:
		SetAndStabilizePublicIP()
		time.sleep(600) 
	