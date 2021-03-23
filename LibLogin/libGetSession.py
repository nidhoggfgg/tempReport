import requests
from bs4 import BeautifulSoup


def getInfo():
    indexUrl = 'https://ehall.hainanu.edu.cn/amp-auth-adapter/login?service=https://ehall.hainanu.edu.cn:443/qljfwapp/sys/lwHainanuStuTempReport/*default/index.do'
    
    # loginUrl 内含有动态的部分，得先访问 indexUrl 才行
    response = requests.get(indexUrl, allow_redirects=False)
    loginUrl = response.headers["Location"]
    response = requests.get(loginUrl)
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    
    # 根据我抓包来看，应该只有这两个是有用的，提交密码时要用
    token = {}
    token["JSESSIONID"] = cookies["JSESSIONID"]
    token["route"] = cookies["route"]
    
    html = response.text
    soup = BeautifulSoup(html, "html.parser")   
    def getValue(a, b): return soup.find(attrs={a: b}).get("value")
    
    # 页面内有用的内容，提交密码时要用
    pageInfo = {}
    pageInfo["lt"] = getValue("name", "lt")
    pageInfo["dllt"] = getValue("name", "dllt")
    pageInfo["execution"] = getValue("name", "execution")
    pageInfo["_eventId"] = getValue("name", "_eventId")
    pageInfo["rmShown"] = getValue("name", "rmShown")
    pageInfo["pwdSalt"] = getValue("id", "pwdDefaultEncryptSalt")
    
    session = {}
    session["token"] = token
    session["pageInfo"] = pageInfo
    session["loginUrl"] = loginUrl
    
    return session

getInfo()