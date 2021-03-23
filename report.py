from LibLogin.libEncrypt import Encrypt
from LibPostTemp.libPostTemp import TempReport
from LibLogin.libGetSession import getInfo
from LibLogin.libGetCookies import getCookies

userName = input("请输入你的用户名/学号：")
passwd   = input("请输入你的密码：")

session = getInfo()
encryptedPwd = Encrypt(passwd, session["pageInfo"]["pwdSalt"]).encrypt()
cookies = getCookies(userName, encryptedPwd, session)
reporter = TempReport(cookies)
reporter.reportAll("ALL", userName)