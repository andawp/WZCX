# coding:utf-8

import requests, logging, re, mail
from bs4 import BeautifulSoup

def ReqCarIllegalInfo(zl,fdj,cpd,hm,toemail):
    logging.basicConfig(filename='log.txt', format='%(levelname)s | %(asctime)s | %(message)s', level=logging.WARNING)
    
    geturl = "http://www.hncsjj.gov.cn/cstv2/weixin/oauth.action?code=00106ce9715f0ff135ef5f5ff6dcb0dY&state=ajcstweixin"
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)"}
    s = requests.session()
    try:
        g = s.get(geturl,headers=headers, timeout=10)
    except Exception,ex:
        logging.error(ex.message)
        return

    posturl = "http://www.hncsjj.gov.cn/cstv2/weixinclwfcx/wxclwfcx.action"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko", "Referer": "http://www.hncsjj.gov.cn/cstv2/weixin/oauth.action?code=00106ce9715f0ff135ef5f5ff6dcb0dY&state=ajcstweixin"}
    carnumber = str(cpd) + str(hm)
    data = {"carwfcxbean.carType": zl, "carwfcxbean.carNumber": carnumber, "carwfcxbean.fdjh": fdj}
    try:
        p = s.post(posturl, data=data, headers=headers, timeout=10)
    except Exception,ex:
        logging.error(ex.message)
        return
    content = p.content
    result = re.search(r"\bform0\b", content)
    if result:
        soup = BeautifulSoup(content)
        plist = soup.find_all("p")
        body = ""
        for p in plist:
            body += str(p)
        body = "".join(body.split(" "))
        body = body.replace(r'<p style="width: 100%;height: 20px;"></p>', '')
        body = body.replace(r'</p><p align="right">', '，')
        body = body.replace(r'累计扣分', '，累计扣分')
        body = body.replace(r'<span style="color:#4299C7;font-size: 20px">', '，<span style="color:red">')
        body = body.replace(r'</span>20', '</span>，20')
        print body.encode('gbk')
        mail.send(toemail, str(cpd) + str(hm) + '违章查询结果', body)
    else:
        return
