#coding=utf8
import datetime
from lxml import etree
from models import Msg

class WeixinMiddleware(object):
    def process_request(self, request):
        if request.method == 'GET':
            return None
        signature = request.GET.get('signature', None)
        if not signature:
            return None
        received = request.raw_post_data
        xml = etree.fromstring(received)
        tousername = xml.find('./ToUserName').text
        fromusername = xml.find('./FromUserName').text
        createtime = int(xml.find('./CreateTime').text)
        createtime = datetime.datetime.fromtimestamp(createtime)
        msgtype = xml.find('./MsgType').text
        if msgtype == 'text':
            content = xml.find('./Content').text
            msg = Msg.objects.create(msg_type=msgtype, to_user=tousername, from_user=fromusername,
                                created_at_from_wx=createtime, content=content)
            request.msg = msg

        elif msgtype == 'location':
            x = xml.find('./Location_X').text
            y = xml.find('./Location_y').text
            scale = xml.find('./Scale').text
            label = xml.find('./Label').text
            msg = Msg.objects.create(msg_type=msgtype, to_user=tousername, from_user=fromusername,
                                created_at_from_wx=createtime,
                                latitude=x, longitude=y, scale=scale, label=label)
            request.msg = msg

