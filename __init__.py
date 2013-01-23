#coding=utf-8
import time
from lxml import etree
from models import Keyword, Chat

def produce_text_resp(from_, to_, resp, funcflag='0', pretty_print=False):
    r = etree.Element('xml')
    tousername = etree.SubElement(r, 'ToUserName')
    tousername.text = etree.CDATA(to_)
    fromusername = etree.SubElement(r, 'FromUserName')
    fromusername.text = etree.CDATA(from_)
    createtime = etree.SubElement(r, 'CreateTime')
    createtime.text = etree.CDATA(str(int(time.time())))

    msgtype = etree.SubElement(r, 'MsgType')
    msgtype.text = etree.CDATA('text')
    content = etree.SubElement(r, 'Content')
    content.text = etree.CDATA(resp)
    funcflag_ = etree.SubElement(r, 'FuncFlag')
    funcflag_.text = etree.CDATA(funcflag)
    xml = etree.tostring(r, encoding='utf-8', pretty_print=pretty_print)
    return xml

def produce_news_resp(from_, to_, resp, funcflag='0', pretty_print=False):
    r = etree.Element('xml')
    tousername = etree.SubElement(r, 'ToUserName')
    tousername.text = etree.CDATA(to_)
    fromusername = etree.SubElement(r, 'FromUserName')
    fromusername.text = etree.CDATA(from_)
    createtime = etree.SubElement(r, 'CreateTime')
    createtime.text = etree.CDATA(str(int(time.time())))

    msgtype.text = etree.CDATA('news')
    content = etree.SubElement(r, 'Content')
    content.text = etree.CDATA('')
    articlecount = etree.SubElement(r, 'ArticleCount')
    articlecount.text = etree.CDATA(str(resp.article_set.count()))
    articles = etree.SubElement(r, 'Articles')
    for a in resp.article_set.all():
        item = etree.SubElement(articles, 'item')
        title = etree.SubElement(item, 'Title')
        title.text = etree.CDATA(a.title)
        desp =  etree.SubElement(item, 'Discription')
        desp.text = etree.CDATA(a.desp)
        picurl = etree.SubElement(item, 'PicUrl')
        picurl.text = etree.CDATA(a.imgurl())
        url = etree.SubElement(item, 'Url')
        url.text = etree.CDATA(a.url)

    funcflag_ = etree.SubElement(r, 'FuncFlag')
    funcflag_.text = etree.CDATA(funcflag)
    xml = etree.tostring(r, encoding='utf-8', pretty_print=pretty_print)
    return xml

def get_rule_by_keyword(msg):
    content = msg.content.lower().strip()
    keywords = Keyword.objects.filter(is_enabled=True).filter(is_strict=True).filter(content=content).\
                order_by('-priority').all()
    if keywords:
        k = keywords[0]
        rule = k.rule.order_by('?')[0]
        return rule

    keywords = Keyword.objects.filter(is_enabled=True).filter(is_strict=False).order_by('-priority').all()
    for k in keywords:
        if content.find(k.content) != -1:
            rule = k.rule.order_by('?')[0]
            return rule
    return None

def get_default_rule(msg):
    keyword = Keyword.objects.get(content='default')
    rule = keyword.rule.order_by('?')[0]
    return rule


