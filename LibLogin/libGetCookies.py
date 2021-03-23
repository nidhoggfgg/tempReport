import requests


def getCookies(userName, encryptedPwd, session):
    """
    提交密码到服务器来获取cookies
    userName 为用户名
    encryptedPwd 为加密之后的密码
    session 是在网页中获取的会话信息
    """
    token    = session["token"]
    pageInfo = session["pageInfo"]
    loginUrl = session["loginUrl"] + "#/stuTempReport"

    # 发包所需的头部和 cookie 以及内容
    headers = {
        "Host": "authserver.hainanu.edu.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "500"
    }
    cookies = {
        "route": token["route"],
        "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE": "zh_CN",
        "JSESSIONID": token["JSESSIONID"]
    }
    data = "" + \
        "username="  + userName              + "&" + \
        "password="  + encryptedPwd          + "&" + \
        "lt="        + pageInfo["lt"]        + "&" + \
        "dllt="      + pageInfo["dllt"]      + "&" + \
        "execution=" + pageInfo["execution"] + "&" + \
        "_eventId="  + pageInfo["_eventId"]  + "&" + \
        "rmShown="   + pageInfo["rmShown"]

    # 确认帐号密码的正确性
    response = requests.post(loginUrl, cookies=cookies, headers=headers, data=data, allow_redirects=False)
    try:
        cookies["CASTGC"] = requests.utils.dict_from_cookiejar(response.cookies)["CASTGC"]
    except BaseException:
        return None

    # 第一步为了找到下一步链接
    nextUrl = response.headers["Location"]
    response = requests.get(nextUrl, cookies=cookies, allow_redirects=False)

    # 继续寻找下一步的链接
    # result = requests.Session()
    nextNextUrl = response.headers["Location"]
    response = requests.get(nextNextUrl, allow_redirects=False)

    # 最后获取到新的真正可用的 CASTGC
    cookies["CASTGC"] = requests.utils.dict_from_cookiejar(response.cookies)["CASTGC"]
    nextNextNextUrl = response.headers["Location"]
    response = requests.get(nextNextNextUrl, allow_redirects=False)

    # 拿到可持久使用的 cookie
    cookies["MOD_AMP_AUTH"] = requests.utils.dict_from_cookiejar(response.cookies)["MOD_AMP_AUTH"]
    tempCookie = {
        "CASTGC": cookies["CASTGC"],
        "MOD_AMP_AUTH": cookies["MOD_AMP_AUTH"]
    }

    finalUrl = 'https://ehall.hainanu.edu.cn:443/qljfwapp/sys/lwHainanuStuTempReport/*default/index.do'
    response = requests.get(finalUrl, cookies=tempCookie)

    cookies["_WEU"] = requests.utils.dict_from_cookiejar(response.cookies)["_WEU"]
    return cookies

