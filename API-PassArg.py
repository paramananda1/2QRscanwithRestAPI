#-to run the app execute the command python API-PassArg.py
#-go to http://localhost:5000/getQRdata/or.png/30 
import subprocess
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class getQRdata(Resource):
    def get(self, image, angle):
        #return {'data': subprocess.check_output(["./QR_reader_webCam",image, angle])}
        data = subprocess.check_output(["./QR_reader_webCam",image, angle])
        return {'data': str(data)}

api.add_resource(getQRdata, '/getQRdata/<image>/<angle>')

if __name__ == '__main__':
     app.run()
