import os.path
import sys
import json
from picamera import PiCamera
from time import sleep
camera = PiCamera()

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
    const=1
    while(const==1):
        request = ai.text_request()
        request.lang = 'es'  # optional, default value equal 'en'

        # request.session_id = "<SESSION ID, UBIQUE FOR EACH USER>"
        print("\nYour Input : ",end=" ")
        request.query = input()        

        print("\nHeimdall\'s response :",end=" ")
        response = request.getresponse()
        responsestr = response.read().decode('utf-8')
        response_obj = json.loads(responsestr)

        print(response_obj["result"]["fulfillment"]["speech"])
        if (response_obj["result"]["action"]=="read-book"):
            camera.start_preview()
            sleep(3)
            camera.capture('/home/pi/heimdall/leer/image1.jpg')
            camera.stop_preview()
            const=1
        if (response_obj["result"]["action"]=="face-detection"):
            camera.start_preview()
            sleep(3)
            camera.capture('/home/pi/heimdall/reconocimiento/image1.jpg')
            camera.stop_preview()
            const=1

if __name__ == '__main__':
    main()
