from django.contrib import admin
from .models import *

# Register your models here.

class SelectionsManager(admin.ModelAdmin):
    list_display = ['id', 'select', 'judge']
    list_display_links = ['select']
    list_editable = ['judge']
    list_filter = ['topic']

class KnowledgeManager(admin.ModelAdmin):
    list_display = ['id', 'point', 'science_education_edition']
    list_display_links = ['point']
    list_editable = ['science_education_edition']
    list_filter = ['type']

class TopicManager(admin.ModelAdmin):
    list_display = ['id', 'topic']
    list_display_links = ['topic']
    list_filter = ['type']



admin.site.register(Topic, TopicManager)
admin.site.register(Selections, SelectionsManager)
admin.site.register(KnowledgePoints, KnowledgeManager)