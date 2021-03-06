#coding=utf-8
from django.contrib import admin
from models import *

class ArticleInline(admin.StackedInline):
    model = Article

class MusicInline(admin.StackedInline):
    model = Music

class RuleAdmin(admin.ModelAdmin):
    inlines = [
        ArticleInline,
        MusicInline,
    ]
    search_fields = ['content']
    list_filter = ['rule_type']

class KeywordAdmin(admin.ModelAdmin):
    search_fields = ['content']
    list_filter = ['is_strict', 'is_enabled']
admin.site.register(Rule, RuleAdmin)
#admin.site.register(Article)
admin.site.register(Keyword, KeywordAdmin)

admin.site.register(Msg)
admin.site.register(Simichat)
#admin.site.register(Music)
