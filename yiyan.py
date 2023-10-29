import requests
import json
import os
from config import Config

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    API_Key = Config.API_Key
    Secret_Key = Config.Secret_Key
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}".format(API_Key=API_Key,Secret_Key=Secret_Key)

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def yiyan_api(message,access_token,use4=False):
    if use4:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
    else:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + access_token
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        result = json.loads(response.text)["result"]
    except:
        print(response.text)
    # print(result)
    return result

def yiyan_embedding(input_text):
    if input_text=="":
        input_text="  "
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token=" + get_access_token()

    payload = json.dumps({
        "input": [input_text]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    result = json.loads(response.text)["data"][0]["embedding"]
    return result

def main():
    embed = yiyan_embedding()
    print(embed)
if __name__ == '__main__':
    main()