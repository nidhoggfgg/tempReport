from LibLogin.libEncrypt import Encrypt
from LibLogin.libGetSession import GetSession
from LibLogin.libLogin import Login

userName = input("请输入你的用户名/学号：")
passwd   = input("请输入你的密码：")

print("正在获取session...")
session = GetSession().getInfo()

print("正在加密密码...")
encryptPwd = Encrypt(passwd, session["pageInfo"]["pwdSalt"]).encrypt()

print("正在获取cookie...")
cookie = Login(userName, encryptPwd, session).getCookies()

if cookie is None:
    print("fuck，出错了，请确认你的用户名或者密码")
else:
    print("整个登录模块正常")
