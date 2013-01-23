#coding=utf-8
import time
from django.db import models

IMAGE_DIR = 'upload/image'
def upload_to(instance, filename):
    filename = filename.encode('u8')
    fn = '.'.join([str(time.time()), filename.split('.')[-1]])
    return '%s/%s'%(IMAGE_DIR, fn)

rule_type_choices = (
    ('text', u'文本'),
    ('news', u'图文news'),
)
funcflag_choices = (
    ('0', u'default'),
    ('1', u'星标'),
)
class Rule(models.Model):
    class Meta:
        verbose_name = u'回复规则'
        verbose_name_plural = verbose_name
        app_label = 'weixin'

    rule_type = models.CharField(max_length=20, choices=rule_type_choices, default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    funcflag = models.CharField(max_length=5, choices=funcflag_choices, default='0')

    content = models.TextField(blank=True)

    def __unicode__(self):
        if self.rule_type == 'text':
            return u'%s_%i(%s ...)'%(self.get_rule_type_display(), self.id, self.content[:25])
        if self.rule_type == 'news':
            if self.article_set.count() > 0:
                a = self.article_set.all()[0]
                return u'%s_%i(%s ...)'%(self.get_rule_type_display(), self.id, a.title[:25])
            return u'%s_%i'%(self.get_rule_type_display(), self.id)

    def toxml(self, from_, to_, funcflag='0', pretty_print=False):
        import time
        from lxml import etree
        r = etree.Element('xml')
        tousername = etree.SubElement(r, 'ToUserName')
        tousername.text = etree.CDATA(to_)
        fromusername = etree.SubElement(r, 'FromUserName')
        fromusername.text = etree.CDATA(from_)
        createtime = etree.SubElement(r, 'CreateTime')
        createtime.text = etree.CDATA(str(int(time.time())))

        msgtype = etree.SubElement(r, 'MsgType')
        if self.rule_type == 'text':
            msgtype.text = etree.CDATA('text')
            content = etree.SubElement(r, 'Content')
            content.text = etree.CDATA(self.content)
        if self.rule_type == 'news':
            msgtype.text = etree.CDATA('news')
            content = etree.SubElement(r, 'Content')
            content.text = etree.CDATA('')
            articlecount = etree.SubElement(r, 'ArticleCount')
            articlecount.text = etree.CDATA(str(self.article_set.count()))
            articles = etree.SubElement(r, 'Articles')
            for a in self.article_set.all():
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

class Article(models.Model):
    class Meta:
        verbose_name = u'图文信息回复'
        verbose_name_plural = verbose_name
        app_label = 'weixin'

    rule = models.ForeignKey(Rule)
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=400)
    desp = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.title

    def imgurl(self):
        from django.conf import settings
        return 'http://'+ settings.HOST + self.image.url

class Keyword(models.Model):
    class Meta:
        verbose_name = u'关键词匹配'
        verbose_name_plural = verbose_name
        app_label = 'weixin'

    content = models.CharField(max_length=50, unique=True)
    priority = models.PositiveIntegerField()
    rule = models.ManyToManyField(Rule, null=True)

    is_strict = models.BooleanField(default=False, verbose_name=u'是否完全匹配？')
    is_enabled = models.BooleanField(default=True, verbose_name=u'是否启用？')

    def __unicode__(self):
        return u'%s(%s)'%(self.content, self.priority)
