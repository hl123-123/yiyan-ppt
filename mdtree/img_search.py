import requests
import re
import uuid
import os
headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69",  # 随机生成一个代理请求
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
           "Connection": "keep-alive"}

img_re = re.compile('"thumbURL":"(.*?)"')
img_format = re.compile("f=(.*).*?w")


def file_op(img):
    if not os.path.exists("./save_img"):
        os.makedirs("./save_img")
    uuid_str = uuid.uuid4().hex
    tmp_file_name = './save_img/%s.jpeg' % uuid_str
    with open(file=tmp_file_name, mode="wb") as file:
        try:
            file.write(img)
        except:
            pass


def xhr_url(url_xhr, start_num=0, page=5):
    end_num = page*30
    for page_num in range(start_num, end_num, 30):
        resp = requests.get(url=url_xhr+str(page_num), headers=headers)
        if resp.status_code == 200:
            img_url_list = img_re.findall(resp.text)  # 这是个列表形式
            for img_url in img_url_list:
                img_rsp = requests.get(url=img_url, headers=headers)
                file_op(img=img_rsp.content)
        else:
            break
    print("内容已经全部爬取")

def get_img(search_content,start_num=0,page=1):
    url_xhr = "https://image.baidu.com/search/acjson?tn=resultjson_com&word={text}&pn=".format(text=search_content)
    end_num = page*30
    img_list = []
    for page_num in range(start_num, end_num, 30):
        resp = requests.get(url=url_xhr+str(page_num), headers=headers)
        if resp.status_code == 200:
            img_url_list = img_re.findall(resp.text)  # 这是个列表形式
            for img_url in img_url_list:
                save_dict={"thumbnail":img_url}
                img_list.append(save_dict)
                # img_rsp = requests.get(url=img_url, headers=headers)
                # file_op(img=img_rsp.content)
        else:
            break

    print("内容已经全部爬取")
    return img_list
if __name__ == "__main__":
    a = get_img("'温馨梦境，安然入睡。'")
    print(a)
    # org_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&word={text}&pn=".format(text=input("输入你想检索内容:"))
    # xhr_url(url_xhr=org_url, start_num=int(input("开始页:")), page=int(input("所需爬取页数:")))
