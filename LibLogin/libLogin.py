import requests


class Login:
    def __init__(self, userName, encryptedPwd, session):
        self.userName     = userName
        self.encryptedPwd = encryptedPwd
        self.token = session["token"]
        self.pageInfo = session["pageInfo"]
        self.loginUrl = session["loginUrl"] + "#/stuTempReport"


    def getCookies(self):
        headers = {
            "Host": "authserver.hainanu.edu.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "500"
        }
        cookies = {
            "route": self.token["route"],
            "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE": "zh_CN",
            "JSESSIONID": self.token["JSESSIONID"]
        }
        data = "" + \
            "username="  + self.userName         + "&" + \
            "password="  + self.encryptedPwd     + "&" + \
            "lt="        + self.pageInfo["lt"]        + "&" + \
            "dllt="      + self.pageInfo["dllt"]      + "&" + \
            "execution=" + self.pageInfo["execution"] + "&" + \
            "_eventId="  + self.pageInfo["_eventId"]  + "&" + \
            "rmShown="   + self.pageInfo["rmShown"]

        response = requests.post(self.loginUrl, cookies=cookies, headers=headers, data=data, allow_redirects=False)
        try:
            cookies["CASTGC"] = requests.utils.dict_from_cookiejar(response.cookies)["CASTGC"]
        except BaseException:
            return None

        # 第一步为了找到下一步链接
        nextUrl = response.headers["Location"]
        response = requests.get(nextUrl, cookies=cookies, allow_redirects=False)

        # 继续寻找下一步的链接
        result = requests.Session()
        nextNextUrl = response.headers["Location"]
        response = result.get(nextNextUrl, allow_redirects=False)

        # 最后获取到新的真正可用的 cookie
        cookies["CASTGC"] = requests.utils.dict_from_cookiejar(response.cookies)["CASTGC"]
        nextNextNextUrl = response.headers["Location"]
        response = requests.get(nextNextNextUrl, allow_redirects=False)

        # 拿到最后一个必须的 cookie
        cookies["MOD_AMP_AUTH"] = requests.utils.dict_from_cookiejar(response.cookies)["MOD_AMP_AUTH"]
        tempCookie = {
            "CASTGC": cookies["CASTGC"],
            "MOD_AMP_AUTH": cookies["MOD_AMP_AUTH"]
        }
        finalUrl = 'https://ehall.hainanu.edu.cn:443/qljfwapp/sys/lwHainanuStuTempReport/*default/index.do'
        response = requests.get(finalUrl, cookies=tempCookie)
        cookies["_WEU"] = requests.utils.dict_from_cookiejar(response.cookies)["_WEU"]

        return cookies
