# _*_ coding:utf-8 _*_

__author__ = 'yanghao'
__date__ = '2018/1/28 10:42'

def get_auth_url():

    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_uri = 'http://127.0.0.1:8000/complete/weibo/'

    access_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=3788328495,redirect_uri=redirect_uri)

    print(access_url)


def get_access_token(code='67efcb2e5d941f9a4e55dec62ad3ad72'):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    import requests
    re_dict = requests.post(access_token_url,data={
        "client_id":3788328495,
        "client_secret":"0ae11600deb4dba3c434c57f002f0ce1",
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:8000/complete/weibo/"
    })
    pass

def get_user_inof(access_token='',uid=""):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}".format(access_token=access_token,uid=uid)

    print(user_url)

if __name__ == '__main__':
    get_auth_url()

##b'{"access_token":"2.00bVXgDDVS84IE83bffc6668ydxY1E","remind_in":"157679999","expires_in":157679999,"uid":"2802866091","isRealName":"true"}'
    get_access_token(code='67efcb2e5d941f9a4e55dec62ad3ad72')

    get_user_inof(access_token="2.00bVXgDDVS84IE83bffc6668ydxY1E",uid="2802866091")