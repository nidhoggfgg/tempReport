import requests
from bs4 import BeautifulSoup


class GetSession:
        def __init__(self):
                self.indexUrl =  'https://ehall.hainanu.edu.cn/amp-auth-adapter/login?service=https://ehall.hainanu.edu.cn:443/qljfwapp/sys/lwHainanuStuTempReport/*default/index.do'


        def getInfo(self):
                response = requests.get(self.indexUrl, allow_redirects=False)
                loginUrl = response.headers["Location"]

                token    = {}
                pageInfo = {}

                response            = requests.get(loginUrl)
                cookie              = requests.utils.dict_from_cookiejar(response.cookies)
                token["JSESSIONID"] = cookie["JSESSIONID"]
                token["route"]      = cookie["route"]

                html = response.text
                soup = BeautifulSoup(html, "html.parser")

                getValue = lambda a, b: soup.find(attrs={a: b}).get("value")

                pageInfo["lt"]        = getValue("name", "lt")
                pageInfo["dllt"]      = getValue("name", "dllt")
                pageInfo["execution"] = getValue("name", "execution")
                pageInfo["_eventId"]  = getValue("name", "_eventId")
                pageInfo["rmShown"]   = getValue("name", "rmShown")
                pageInfo["pwdSalt"]   = getValue("id", "pwdDefaultEncryptSalt")

                session = {}
                session["token"] = token
                session["pageInfo"] = pageInfo
                session["loginUrl"] = loginUrl

                return session