#!/usr/bin/python
# -*- coding: utf8 -*-

########################################################################
#API face detect setup
########################################################################
import json
import requests
import base64
from datetime import datetime
from ftplib import FTP
import time

import threading
from MqttClient import MQTTClient

Mqtt = MQTTClient()
Mqtt.MqttPathPublish = "your path to publish"
Mqtt.MqttPathSubcribe = "APIGetPost"


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        Mqtt.mqttSubcribe()

queueLock = threading.Lock()
thread = myThread(1, "thread1")
thread.start()

#login infomation
# urlLogin = "http://new-thd.ddns.net:4000/v1/auth"
urlLogin = "https://api.deepkafe.com/faceid/v1/auth"
typeHeaderLogin = {'Content-Type': 'application/json'}
userData = {"username": "deepkafe1",  "password": "deepkafedemo1"}

#API Upload
# urlDac = "http://new-thd.ddns.net:4000/v1/dac"
urlDac = "https://api.deepkafe.com/faceid/v1/dac"

#Get access data
# urlGetAccess = "http://new-thd.ddns.net:4000/v1/fetch"
urlGetAccess = "https://api.deepkafe.com/faceid/v1/fetch"
dataGetAccess = {"start_time": "01/01/1992 1:1:1", "end_time": "06/03/2019 1:1:1"}

#Verification API
# urlVerify = "http://new-thd.ddns.net:4000/v1/verify"
urlVerify = "https://api.deepkafe.com/faceid/v1/verify"
dataVerify = {'image': '',  'verify_id' : ''}
urlVerifyFtp = "https://api.deepkafe.com/faceid/v1/ftp-verify-notice"
dataVerifyFtp = {"ftp_host": "", "ftp_user": "", "ftp_pass": "", "verify_data": [1]}

#Get all user API
# urlGetUsers = "http://new-thd.ddns.net:4000/v1/get_users"
urlGetUsers = "https://api.deepkafe.com/faceid/v1/get_users"

#Register User API
# urlRegister = "http://new-thd.ddns.net:4000/v1/register"
urlRegister = "https://api.deepkafe.com/faceid/v1/register"
dataRegister = {"user_name": "",  "user_id" : "",  "face_images" : "", "overwrite": True}

#Retrain API
# urlRetrain = "http://new-thd.ddns.net:4000/v1/retrain"
urlRetrain = "https://api.deepkafe.com/faceid/v1/retrain"

#Delete User API
# urlDeleteUser = "http://new-thd.ddns.net:4000/v1/delete_user"
urlDeleteUser = "https://api.deepkafe.com/faceid/v1/delete_user"
dataDeleteUser = {"user_id" : ""}

#Recognize by FTP API
urlRecognize = "https://api.deepkafe.com/faceid/v1/ftp-recognize-notice"
dataRecognize = {"ftp_host": "", "ftp_user": "", "ftp_pass": "", "recognize_data": [""]}

typeHeaderApi = {'Content-Type': 'application/json', 'Authorization':''}


def getToken():
    responseDecodedJson = requests.post(urlLogin, data=json.dumps(userData), headers=typeHeaderLogin)
    responseJson = responseDecodedJson.json()
    if responseJson["message"] == "SUCCESS":
        return responseJson["data"]["authToken"].encode("ascii","replace")
    else:
        return "False"
def getAccess(_startTime, _endTime):
    dataGetAccess["start_time"] = _startTime
    dataGetAccess["end_time"] = _endTime

    typeHeaderApi['Authorization'] = 'Bearer ' + getToken()
    responseDecodedJson = requests.post(urlGetAccess, data=json.dumps(dataGetAccess), headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

def verifyFace(_base64Image, _id):
    dataVerify['image'] = _base64Image
    dataVerify['verify_id'] = _id
    _token = getToken()
    if _token == "False":
        return "False"
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    responseDecodedJson = requests.post(urlVerify, data=json.dumps(dataVerify), headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

def verifyFaceFtp(_ftpHost, _ftpUser, _ftpPass, _imageFtp, _ID):
    dataVerifyFtp['ftp_host'] = _ftpHost
    dataVerifyFtp['ftp_user'] = _ftpUser
    dataVerifyFtp['ftp_pass'] =_ftpPass
    dataVerifyFtp['verify_data'][0] = [_imageFtp,_ID]
    _token = getToken()
    if _token == "False":
        return "False"
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    responseDecodedJson = requests.post(urlVerifyFtp, data=json.dumps(dataVerifyFtp), headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

def getAllUsers():
    typeHeaderApi['Authorization'] = 'Bearer ' + getToken()
    responseDecodedJson = requests.get(urlGetUsers, headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

def registerUser(_username, _userId, _faceImage, _overwrite):
    typeHeaderApi['Authorization'] = 'Bearer ' + getToken()
    dataRegister["user_name"] = _username
    dataRegister["user_id"] = _userId
    dataRegister["face_images"] = _faceImage
    dataRegister["overwrite"] = _overwrite
    responseDecodedJson = requests.post(urlRegister, data=json.dumps(dataRegister), headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

def deleteUser(_userId):
    typeHeaderApi['Authorization'] = 'Bearer ' + getToken()
    dataDeleteUser["user_id"] = _userId
    responseDecodedJson = requests.post(urlDeleteUser, data=json.dumps(dataDeleteUser), headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

def recognizeFaceFtp(_ftpHost, _ftpUser, _ftpPass, _imageFtp):
    dataRecognize["ftp_host"] = _ftpHost
    dataRecognize["ftp_user"] = _ftpUser
    dataRecognize["ftp_pass"] =_ftpPass
    dataRecognize["recognize_data"][0] = _imageFtp
    _token = getToken()
    if _token == "False":
        return "False"
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    print dataRecognize
    responseDecodedJson = requests.post(urlRecognize, data=json.dumps(dataRecognize), headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

def reTrain():
    typeHeaderApi['Authorization'] = 'Bearer ' + getToken()
    responseDecodedJson = requests.get(urlRetrain, headers=typeHeaderApi)
    responseJson = responseDecodedJson.json()
    return responseJson

########################################################################
flag_1 = False
flag_2 = False
_dataWriteMainApp = {"source":"APIGetPost","func":"screen","data":{"company":"","name":"","ID":"","mess":""}}
_dataWriteAudioPlay = {"source":"APIGetPost","func":"play","data":""}
_dataWriteGPIO = {"source":"APIGetPost","func":"blinkLed","data":0}


print "APIGetPost"
ImageBase64 = ""
IDCardNumber = ""
ftp = FTP()
ftp.set_debuglevel(2)
ftpHost = "new-thd.ddns.net"
ftpUser = "ltkftp"
ftpPass = "aNdIcKerbanDeNUmBEtIcYoFUraTHe"
ftpPath = "/files/save/in"

while True:
    _waitData = Mqtt.getData()
    if _waitData != None:
        waitData = json.loads(_waitData)
        #if waitData["source"] == "KeyBoard":
        #    IDCardNumber = waitData["data"]
        #    #print "KeyBoard: ", IDCardNumber
	#    flag_1 = True
#	if (waitData["source"] == "MainApp") & (waitData["data"]["ID"] == "0250879771"):
#            _ImageBase64 = waitData["data"]["base64image"]
#            IDCardNumber = waitData["data"]["ID"]
#            FtpImage = "Image_" + datetime.now().strftime("%b-%d-%Y_%H_%M_%S")+".jpg"
#            fp = open(_ImageBase64, 'rb')
#            # ftp.connect('192.168.0.220', 21) 
#            # ftp.login('creta','a123456')
#            # ftp.cwd('/Raymond_killer/image_save')
#            ftp.connect(ftpHost)
#            ftp.login(ftpUser,ftpPass)
#            ftp.cwd(ftpPath)
#            ftp.storbinary('STOR %s' % FtpImage, fp)
#            fp.close()
#            ftp.quit()
#            FtpImage = ftpPath + "/" + FtpImage
#            #print "start"
#	    _timeStart = time.time()
#            _respont = recognizeFaceFtp(ftpHost,ftpUser,ftpPass,FtpImage)
#            _timeStop = time.time()
#	    data = open('/home/pi/maychamcong/log.txt', 'a')
#            print _timeStop-_timeStart
#            now = datetime.now()
#            data.write("RecognizeFace " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
#            data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
#            data.close()
#	    #print "stop"
#            print _respont
#        if (waitData["source"] == "MainApp") & (waitData["data"]["ID"] != "0250879771"):
        if waitData["source"] == "MainApp":
            _ImageBase64 = waitData["data"]["base64image"]
            IDCardNumber = waitData["data"]["ID"]
#            with open(_ImageBase64) as image_file:
#		ImageBase64 = base64.b64encode(image_file.read())
	    #print "MainApp: ", ImageBase64
	    #flag_2 = True
	    #flag_1 = True

        #if (flag_1 == True) & (flag_2 == True):
            #flag_1 = False
            #flag_2 = False
	    #print "start"
	    if IDCardNumber == "0250879771":
		FlagType = "recognize"
		_ImageBase64 = waitData["data"]["base64image"]
                IDCardNumber = waitData["data"]["ID"]
		FtpImage = "Image_" + datetime.now().strftime("%b-%d-%Y_%H_%M_%S")+".jpg"
                fp = open(_ImageBase64, 'rb')
                ftp.connect(ftpHost)
                ftp.login(ftpUser,ftpPass)
                ftp.cwd(ftpPath)
            	ftp.storbinary('STOR %s' % FtpImage, fp)
            	fp.close()
            	ftp.quit()
            	FtpImage = ftpPath + "/" + FtpImage
            	#print "start"
           	_timeStart = time.time()
            	_respont = recognizeFaceFtp(ftpHost,ftpUser,ftpPass,FtpImage)
            	_timeStop = time.time()
           	data = open('/home/pi/maychamcong/log.txt', 'a')
           	print _timeStop-_timeStart
            	now = datetime.now()
            	data.write("RecognizeFace " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
            	data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
            	data.close()
            	print _respont
		if (_respont["message"] == "SUCCESS") & (len( _respont["data"]["result"][0]["recognition"]) != 0):
		    #print _respont["data"]["result"][0]["recognition"][0]["score"]
		    _score = _respont["data"]["result"][0]["recognition"][0]["score"]
		    if _score == -1:
			_dataWriteMainApp["data"]["mess"] = u"chào bạn! mời bạn đến quầy đăng ký thông tin"
			_dataWriteAudioPlay["data"] = u"chào bạn mời bạn đến quầy đăng ký thông tin"
		    else:
    		        _dataWriteMainApp["data"]["mess"] = _respont["data"]["result"][0]["message"] + "score = " + str("%.2f" % (_score*100)) + "%"
			_dataWriteAudioPlay["data"] = u"xin chào " + _respont["data"]["result"][0]["recognition"][0]["name"] + u" mời bạn vào"
                    _dataWriteMainApp["data"]["name"] = _respont["data"]["result"][0]["recognition"][0]["name"]
                    _dataWriteMainApp["data"]["company"] = userData["username"]
                    _dataWriteMainApp["data"]["ID"] = _respont["data"]["result"][0]["recognition"][0]["user_id"]
		    Mqtt.MqttPathPublish = "MainApp"
                    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
		    #_dataWriteAudioPlay["data"] = "moibanvao"
		    Mqtt.MqttPathPublish = "AudioPlay"
                    Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))
		elif (_respont["message"] == "SUCCESS") & (len( _respont["data"]["result"][0]["recognition"]) == 0):
                    #print _respont["data"]["result"][0]["recognition"][0]["score"]
                    #_score = _respont["data"]["result"][0]["recognition"][0]["score"]
                    #if _score == -1:
                    #    _dataWriteMainApp["data"]["mess"] = "moi ban den quay dien thong tin"
                    #    _dataWriteAudioPlay["data"] = "moibandenquaydienthongtin"
                    #else:
                    _dataWriteMainApp["data"]["mess"] = _respont["data"]["result"][0]["message"] + u"camera chưa thấy mặt bạn"
                    #_dataWriteAudioPlay["data"] = "moibanvao"
                    _dataWriteMainApp["data"]["name"] = ""
                    _dataWriteMainApp["data"]["company"] = userData["username"]
                    _dataWriteMainApp["data"]["ID"] = ""
                    Mqtt.MqttPathPublish = "MainApp"
                    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    _dataWriteAudioPlay["data"] = u"camera chưa thấy mặt bạn"
                    Mqtt.MqttPathPublish = "AudioPlay"
                    Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))
		else:
                    _dataWriteMainApp["data"]["mess"] = u"server đang gặp lỗi"
                    _dataWriteMainApp["data"]["name"] = ""
                    _dataWriteMainApp["data"]["company"] = ""
	            _dataWriteMainApp["data"]["ID"] = IDCardNumber
                    Mqtt.MqttPathPublish = "MainApp"
                    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    _dataWriteAudioPlay["data"] = u"server đang gặp lỗi rồi"
                    Mqtt.MqttPathPublish = "AudioPlay"
                    Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))

	    else:
		FlagType = "verify"
            	#with open(_ImageBase64) as image_file:
               	#    ImageBase64 = base64.b64encode(image_file.read())
	    	_ImageBase64 = waitData["data"]["base64image"]
                IDCardNumber = waitData["data"]["ID"]
                FtpImage = "Image_" + datetime.now().strftime("%b-%d-%Y_%H_%M_%S")+".jpg"
                fp = open(_ImageBase64, 'rb')
                ftp.connect(ftpHost)
                ftp.login(ftpUser,ftpPass)
                ftp.cwd(ftpPath)
                ftp.storbinary('STOR %s' % FtpImage, fp)
                fp.close()
                ftp.quit()
                FtpImage = ftpPath + "/" + FtpImage
		_timeStart = time.time()
            	#print "start request"
	    	#__respont =  verifyFace(ImageBase64,IDCardNumber)
            	__respont = verifyFaceFtp(ftpHost,ftpUser,ftpPass,FtpImage,IDCardNumber)
		_timeStop = time.time()
            	data = open('/home/pi/maychamcong/log.txt', 'a')
            	print _timeStop-_timeStart
            	now = datetime.now()
            	data.write("VerifyFace " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
	    	data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
	    	data.close()
	    	#print "stop"

            	if __respont["message"] == "SUCCESS":
		    print __respont
                    if __respont["data"]["result"][0]["message"] == "Matched":
		    #if __respont["data"]["message"] == "Matched":
#		    	print IDCardNumber
                    	_dataWriteGPIO["data"] = 5
                    	#_dataWriteMainApp["data"]["mess"] = "Moi Ban Vao!"
                    	#_dataWriteMainApp["data"]["name"] = __respont["data"]["user_data"]["user_name"]
			_dataWriteMainApp["data"]["mess"] = "score: " + str("%.2f" % (__respont["data"]["result"][0]["score"]*100)) + u"% => mời bạn vào!"
                        _dataWriteMainApp["data"]["name"] = __respont["data"]["result"][0]["user_data"]["user_name"]
			_dataWriteMainApp["data"]["company"] = userData["username"]
		    	_dataWriteMainApp["data"]["ID"] = IDCardNumber
                    	_dataWriteAudioPlay["data"] = u"xin chào " + __respont["data"]["result"][0]["user_data"]["user_name"] + u" mời bạn vào" 
                    elif __respont["data"]["result"][0]["message"] == "Not matched":
		    #if __respont["data"]["message"] == "Not matched":
                    	_dataWriteGPIO["data"] = 2
                    	_dataWriteMainApp["data"]["mess"] = "score: " + str("%.2f" % (__respont["data"]["result"][0]["score"]*100)) + u"% => Bạn cầm nhầm thẻ rồi!"
                    	_dataWriteMainApp["data"]["name"] = ""
                    	_dataWriteMainApp["data"]["company"] = ""
		    	_dataWriteMainApp["data"]["ID"] = IDCardNumber
                    	_dataWriteAudioPlay["data"] = u"bạn cầm nhầm thẻ rồi"
                    elif __respont["data"]["result"][0]["message"] == "there is no user presented verify id":
		    #if __respont["data"]["message"] == "there is no user presented verify id":
                    	_dataWriteGPIO["data"] = 3
                    	_dataWriteMainApp["data"]["mess"] = u"Thẻ không hợp lệ!"
                    	_dataWriteMainApp["data"]["name"] = ""
                    	_dataWriteMainApp["data"]["company"] = ""
		    	_dataWriteMainApp["data"]["ID"] = IDCardNumber
                    	_dataWriteAudioPlay["data"] = u"Thẻ không hợp lệ"
		    elif __respont["data"]["result"][0]["message"] == "There is not any face in the image":
                    #if __respont["data"]["message"] == "There is not any face in the image":
                    	_dataWriteGPIO["data"] = 1
                    	_dataWriteMainApp["data"]["mess"] = u"Camera chưa thấy mặt bạn!"
                    	_dataWriteMainApp["data"]["name"] = ""
                    	_dataWriteMainApp["data"]["company"] = ""
		    	_dataWriteMainApp["data"]["ID"] = IDCardNumber
                    	_dataWriteAudioPlay["data"] = u"camera chưa thấy mặt bạn"
		    else:
			_dataWriteMainApp["data"]["mess"] = u"server đang gặp lỗi!"
                    	_dataWriteMainApp["data"]["name"] = ""
                    	_dataWriteMainApp["data"]["company"] = ""
                    	_dataWriteMainApp["data"]["ID"] = IDCardNumber
                    	Mqtt.MqttPathPublish = "MainApp"
                    	Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    	_dataWriteAudioPlay["data"] = u"server đang gặp lỗi rồi"
                    	Mqtt.MqttPathPublish = "AudioPlay"
                    	Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))

                    Mqtt.MqttPathPublish = "MainApp"
                    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    Mqtt.MqttPathPublish = "GPIO"
                    Mqtt.mqttPublish(json.dumps(_dataWriteGPIO))
                    Mqtt.MqttPathPublish = "AudioPlay"
                    Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))
                else:
                    _dataWriteMainApp["data"]["mess"] = u"server đang gặp lỗi!"
                    _dataWriteMainApp["data"]["name"] = ""
                    _dataWriteMainApp["data"]["company"] = ""
                    _dataWriteMainApp["data"]["ID"] = IDCardNumber
                    Mqtt.MqttPathPublish = "MainApp"
                    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    _dataWriteAudioPlay["data"] = u"server đang gặp lỗi rồi"
                    Mqtt.MqttPathPublish = "AudioPlay"
                    Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))

	print "done"

