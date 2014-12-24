#coding:utf-8
#ÓÊ¼þ·¢ËÍº¯Êý
import smtplib, logging
from email.mime.text import MIMEText
from xml.etree import ElementTree

def send(to_list,sub,content):
    logging.basicConfig(filename='log.txt', format='%(levelname)s | %(asctime)s | %(message)s', level=logging.DEBUG)
    root = ElementTree.parse("config.xml").getroot()
    mail_host = root.find("mail/mail_host").text
    mail_pass = root.find("mail/mail_pass").text
    mail_postfix = root.find("mail/mail_postfix").text
    mail_user = root.find("mail/mail_user").text + "@" + mail_postfix
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg['To'] = to_list
    try:
        server = smtplib.SMTP_SSL(mail_host,465)
        server.login(mail_user,mail_pass)
        server.sendmail(msg['From'],to_list,msg.as_string())
        server.close()
        return True
    except Exception,e:
        logging.error(e.message)
        return False