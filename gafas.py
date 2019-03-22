import os.path
import sys
import json
import cv2
# from picamera import PiCamera
from time import sleep
import requests
# camera = PiCamera()

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
CLIENT_ACCESS_TOKEN = '4e7b40ad03e846f2b408a372e1fd1588'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    const = 1
    while(const == 1):
        request = ai.text_request()
        request.lang = 'es'  # optional, default value equal 'en'

        # request.session_id = "<SESSION ID, UBIQUE FOR EACH USER>"
        print("\nYour Input : ", end=" ")
        request.query = input()

        print("\nHeimdall\'s response :", end=" ")
        response = request.getresponse()
        responsestr = response.read().decode('utf-8')
        response_obj = json.loads(responsestr)

        print(response_obj["result"]["fulfillment"]["speech"])
        if (response_obj["result"]["action"] == "read-book"):
          capture_image('/home/pi/heimdall/reconocimiento/image1.jpg')
          with open('imagen1.jpg', 'rb') as f: 
            r = requests.post('http://10.240.39.151:5000/', files={'file': f})
            r = r.json()
        if (response_obj["result"]["action"] == "face-detection"):
            capture_image('/home/pi/heimdall/reconocimiento/image1.jpg')
            with open('imagen1.jpg', 'rb') as f: 
              r = requests.post('http://10.240.39.151:5000/', files={'file': f})
              r = r.json()

              #enviar el dato por bluetooth a android

def capture_image(destination):
    ret, frame = cap.read()
    cv2.imwrite(destination, frame)
    # camera.start_preview()
    # sleep(3)
    # camera.capture(destination)
    # camera.stop_preview()

main()
