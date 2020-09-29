# 2QRscanwithRestAPI
Scan 2 qrs and find angle 
Pre Requrments:
json,Opencv, numpy, pyzbar,Flask( for rest api)

Steps:
Create Executble , copy and Run in current dir:
pyinstaller --onefile  QR_reader_webCam.py
cp dist/QR_reader_webCam . 

Rn API :  
export FLASK_APP=RESTapi.py
flask run
To see data navigat to http://127.0.0.1:5000/ or issu curl http://127.0.0.1:5000/ 

TODO:
Current this code is using a static image, we need to read from webcam.
