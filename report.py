from LibLogin.libEncrypt import Encrypt
from LibLogin.libGetSession import GetSession
from LibLogin.libLogin import Login
from LibPostTemp.libPostTemp import TempReport

userName = input("请输入你的用户名/学号：")
passwd   = input("请输入你的密码：")
fromDate = input("请输入开始填报的日期(类似于2020-11-20)：")

print("正在获取session...")
session = GetSession().getInfo()

print("正在加密密码...")
encryptPwd = Encrypt(passwd, session["pageInfo"]["pwdSalt"]).encrypt()

print("正在获取cookie...")
cookie = Login(userName, encryptPwd, session).getCookies()

fails = TempReport(cookie, userName, fromDate).reportAll("NO")

for i in fails:
    print("失败日期：" + i)