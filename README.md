# TimeKeeper
stable version for timeKeeper face in hdmi 7 in with pyqt5 

ngồi chờ tín hiệu gửi về từ mqtt (IDCardReader):
MqttPathSubcribe = "MainApp"
nếu có dữ liệu gửi đến từ KeyBoard:
_dataWriteMainApp = {"source":"KeyBoard","func":"capture","data":""}

data là ID của card sau đó chụp hình và publish lên MqttPathPublish = "APIGetPost"
_dataWriteAPIGetPost = {"source":"MainApp","func":"capture","data":{"ID":"","base64image":""}}
*trong đó "ID" là IDCard nhận được (_dataWriteMainApp["data"]), "base64image" là link chuẩn bức ảnh (vd: /home/pi/maychamcong/MainApp/image/image.jpg")
 => hiển thị bức hình lên màn hình

sau đó nếu nhận được dữ liệu từ APIGetPost:
_dataWriteMainApp = {"source":"APIGetPost","func":"screen","data":{"company":"","name":"","ID":"","mess":""}}

dùng các dữ liệu trong _dataWriteMainApp["data"] để hiển thị: 
CÔNG TY: _dataWriteMainApp["data"]["company"]
TÊN: _dataWriteMainApp["data"]["name"]
ID: _dataWriteMainApp["data"]["ID"]
THÔNG BÁO: _dataWriteMainApp["data"]["mess"]
