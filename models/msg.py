#coding=utf-8
from django.db import models

msg_type_choices = (
    ('text', u'文本'),
    ('location', u'地理位置'),
)
class Msg(models.Model):
    class Meta:
        verbose_name = u'收到的用户消息'
        verbose_name_plural = verbose_name
        app_label = 'weixin'

    msg_type = models.CharField(max_length=20, choices=msg_type_choices)

    to_user = models.CharField(max_length=50)
    from_user = models.CharField(max_length=50)
    created_at_from_wx = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    content = models.TextField(blank=True)

    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    scale = models.PositiveIntegerField(null=True, blank=True)
    label = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        if self.msg_type == 'text':
            return u'%s:%s'%(self.get_msg_type_display(), self.content)
        if self.msg_type == 'location':
            if self.label:
                return u'%s:%s'%(self.get_msg_type_display(), self.label)
            else:
                return u'%s:(%s, %s)'%(self.get_msg_type_display(),
                                        self.latitude, self.longitude)
