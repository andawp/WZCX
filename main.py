# -*- coding: utf-8 -*-
import query, sys, time, random
from xml.etree import ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf8')
tree = ET.parse('config.xml').getroot().find('carInfo')
carinfo = tree.findall('car')
for car in carinfo:
    query.ReqCarIllegalInfo(car.get('zl'), car.get('fdj'), car.get('cpd'), car.get('hm'), car.get('to_mail'))
    time.sleep(random.randint(10,30))
