# _*_ coding:utf-8 _*_

__author__ = 'yanghao'
__date__ = '2018/1/7 14:15'
import json
import requests

class YunPian(object):
    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【印刻学术期刊】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict

if __name__ == "__main__":
    yun_pian = YunPian("5a8169e9dafd137fc527e6e34fd9b54c")
    yun_pian.send_sms("二郎是个笨蛋", "15120092564")