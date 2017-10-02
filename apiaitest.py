import os.path
import sys
import json
import pyttsx
engine = pyttsx.init()
import apiai
CLIENT_ACCESS_TOKEN = '4e7b40ad03e846f2b408a372e1fd1588⁠⁠⁠⁠'
def main():
    while(1):
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        request = ai.text_request()
        request.lang = 'en'  # optional, default value equal 'en'

        # request.session_id = "<SESSION ID, UBIQUE FOR EACH USER>"
        print("\n\nYour Input : ",end=" ")
        request.query = input()

        print("\n\nBot\'s response :",end=" ")
        response = request.getresponse()
        responsestr = response.read().decode('utf-8')
        response_obj = json.loads(responsestr)

        print(response_obj["result"]["fulfillment"]["speech"])
        engine.say(response_obj["result"]["fulfillment"]["speech"])
        engine.runAndWait()
if __name__ == '__main__':
  main()
