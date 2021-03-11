from bs4 import BeautifulSoup
import requests
import urllib3
from datetime import datetime
import json


class TempReport:
    def __init__(self, studentCookies, userId, fromDate, toDate=datetime.today()):
        self.studentCookies = studentCookies
        self.userId         = userId
        self.fromDate       = fromDate
        self.toDate         = toDate
        self.days           = (toDate - datetime.strptime(fromDate, "%Y-%m-%d")).days
        self.allTempUrl     = 'https://ehall.hainanu.edu.cn/qljfwapp/sys/lwHainanuStuTempReport/mobile/stuTempReport/getStuTempReportData.do'
        self.postTempUrl    = 'https://ehall.hainanu.edu.cn/qljfwapp/sys/lwHainanuStuTempReport/mobile/stuTempReport/T_STU_TEMP_REPORT_MODIFY.do?'
        self.headers        = {
            "Host": "ehall.hainanu.edu.cn",
            "Content-Length": "77",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.data = ""    + \
            "USER_ID="    + self.userId                      + "&" + \
            "pageNumber=" + "1"                              + "&" + \
            "pageSize="   + str(self.days)                   + "&" + \
            "KSRQ="       + self.fromDate                    + "&" + \
            "JSRQ="       + self.toDate.strftime("%Y-%m-%d") + "&"


    def getTempInfo(self, state):
        allDays = json.loads(
            requests.post(self.allTempUrl, headers=self.headers, data=self.data, cookies=self.studentCookies).text)
        tempInfo = []
        for rows in allDays["datas"]["getStuTempReportData"]["rows"]:
            if rows["STATE"] == state:
                tempInfo.append(rows)
        return tempInfo


    def postTemp(self, notReportInfo, location="海南省海口市美兰区云翮南路", hms="22:00:00", state="YES", temp="37.3°C以下", display="是"):
        postUrl = str(self.postTempUrl) + \
            "WID="                      + str(notReportInfo["WID"])                         + "&" + \
            "LOCATION_DETAIL="          + str(location)                                     + "&" + \
            "USER_ID="                  + str(notReportInfo["USER_ID"])                     + "&" + \
            "USER_NAME="                + str(notReportInfo["USER_NAME"])                   + "&" + \
            "SEX="                      + str(notReportInfo["SEX"])                         + "&" + \
            "USER_PHONE="               + str(notReportInfo["USER_PHONE"])                  + "&" + \
            "STU_TYPE="                 + str(notReportInfo["STU_TYPE"])                    + "&" + \
            "DEPT_CODE="                + str(notReportInfo["DEPT_CODE"])                   + "&" + \
            "MAJOR_CODE="               + str(notReportInfo["MAJOR_CODE"])                  + "&" + \
            "CLASS_CODE="               + str(notReportInfo["CLASS_CODE"])                  + "&" + \
            "CAMPUS="                   + str(notReportInfo["CAMPUS"])                      + "&" + \
            "CHECK_START_TIME="         + str(notReportInfo["CHECK_START_TIME"])            + "&" + \
            "CHECK_END_TIME="           + str(notReportInfo["CHECK_END_TIME"])              + "&" + \
            "SYNC_TIME="                + str(notReportInfo["SYNC_TIME"])                   + "&" + \
            "REPORT_TIME="              + str(notReportInfo["CHECK_DATE"]) + " " + str(hms) + "&" + \
            "REPORT_TYPE="              + str(notReportInfo["REPORT_TYPE"])                 + "&" + \
            "BODY_TEMPERATURE="         + str("1")                                          + "&" + \
            "STATE="                    + state                                             + "&" + \
            "CHECK_DATE="               + str(notReportInfo["CHECK_DATE"])                  + "&" + \
            "SEX_DISPLAY="              + str(notReportInfo["SEX_DISPLAY"])                 + "&" + \
            "DEPT_CODE_DISPLAY="        + str(notReportInfo["DEPT_CODE_DISPLAY"])           + "&" + \
            "MAJOR_CODE_DISPLAY="       + str(notReportInfo["MAJOR_CODE_DISPLAY"])          + "&" + \
            "CLASS_CODE_DISPLAY="       + str(notReportInfo["CLASS_CODE_DISPLAY"])          + "&" + \
            "CAMPUS_DISPLAY="           + str(notReportInfo["CAMPUS_DISPLAY"])              + "&" + \
            "REPORT_TYPE_DISPLAY="      + str(notReportInfo["REPORT_TYPE_DISPLAY"])         + "&" + \
            "BODY_TEMPERATURE_DISPLAY=" + temp                                              + "&" + \
            "STATE_DISPLAY="            + display
        rsp = requests.post(postUrl, cookies=self.studentCookies)
        return rsp


    def reportAll(self, state):
        notReportTempInfo = self.getTempInfo(state)
        fail = []
        for oneDayTempInfo in notReportTempInfo:
            tempRespond = self.postTemp(oneDayTempInfo)
            if tempRespond.text != '{"datas":{"T_STU_TEMP_REPORT_MODIFY":1},"code":"0"}':
                fail += oneDayTempInfo["CHECK_DATE"]
        return fail
