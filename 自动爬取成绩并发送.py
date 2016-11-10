#-*_coding:utf-8-*-
import requests
import re
import sys
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import os
import time

import smtplib
reload(sys)
sys.setdefaultencoding("utf-8")






def xuehao(zjh,mm):#爬取信息
    session = requests.Session()
    url='http://newjw.cduestc.cn/loginAction.do'
    date={
        'zjh':zjh,
        'mm':mm
    }
    html_post=session.post(url,date)
    url='http://newjw.cduestc.cn/bxqcjcxAction.do'
    html=session.get(url)

    text_fied = re.findall(u";\">(.*?)</tr>",html.text,re.S)
    haha=[]
    for a in text_fied:
        a=a.strip()
        the_end=re.findall(u"center\">(.*?)</td>",a,re.S)
        haha.append(the_end)
    f=[]
    count=0
    for name in haha[1:13]:
        if name[6].strip()=="":
            q='%s:成绩未出'%(name[2].strip())
            f.append(q)
            count+=1
        else:
            q='%s:%s'%(name[2].strip(),name[6].strip())
            f.append(q)
    return '\n'.join(f)

chengji=xuehao(1341310220,'BYPQQI')
def send():#发送邮件
    def _format_addr(s):#转换编码
        name, addr = parseaddr(s)
        return formataddr((
            Header(name, 'utf-8').encode(),
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    from_addr = '845437607@qq.com'
    password = 'bcjtnbzlhfalbbhf'
    to_addr = ['459551804@qq.com']
    smtp_server = 'smtp.qq.com'
    smtp_port = 587

    msg = MIMEText('这是你的成绩\n%s'%chengji, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'你最亲爱的爸爸 <%s>' % from_addr)
    msg['To'] = _format_addr(u'小分队成员<%s>' % to_addr)
    msg['Subject'] = Header(u'来自爸爸的问候……', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


def update():
    while True:
        if not os.path.exists('weibo.txt'):
            f = open('weibo.txt', 'a')
            f.write(chengji)
            f.close()
            send()
        else:
            f = open('weibo.txt', 'r')
            existweibo = f.read()
            if chengji in existweibo:
                pass
                print "查询"
            else:
                send()
                f = open('weibo.txt', 'w')
                f.write(chengji)
                f.close()
        time.sleep(30)
update()





