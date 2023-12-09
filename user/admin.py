from django.contrib import admin
from .models import *

# Register your models here.
class UserInformationManager(admin.ModelAdmin):
    list_display = ['username', 'is_active']
    list_display_links = ['username']
    list_editable = ['is_active']

class WrongQuestionManager(admin.ModelAdmin):
    list_display = ['wrong_pointid', 'edited_time', 'level_mastery', 'is_active']
    list_display_links = ['wrong_pointid']
    list_editable = ['is_active', 'level_mastery']

admin.site.register(UserInformation, UserInformationManager)
admin.site.register(WrongQuestion, WrongQuestionManager)