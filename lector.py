########### Python 3.6 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json



def read(url):
    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '11bb51916aee456f85cae4d6e9e8a8a7'

    # Replace or verify the region.
    #
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace 
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'southcentralus.api.cognitive.microsoft.com'

    headers = {
        # Request headers.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters. The language setting "unk" means automatically detect the language.
        'language': 'unk',
        'detectOrientation ': 'true',
    })

    # The URL of a JPEG image containing text.
    body = "{'url':'"+url+"'}"
    print(body)
    try:
        # Execute the REST API call and get the response.
        print("sending image")
        conn = http.client.HTTPSConnection(uri_base)
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        print("response!!!")
        #data = response.read()
        str_response = response.read().decode('utf-8')
        # 'data' contains the JSON data. The following formats the JSON data for display.
        #parsed = json.loads(data)
        parsed = json.loads(str_response)
        print ("Response:")
        texto = json.dumps(parsed, sort_keys=True, indent=2)
        with open("Output.txt", "w") as text_file:
            print(f"{texto}", file=text_file)
        conn.close()
        return texto

    except Exception as e:
        print('Error:')
        print(e)
    return "failed to read"

    ####################################