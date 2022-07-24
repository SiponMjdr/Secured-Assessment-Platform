from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display=['firstname','lastname','email','password','active']
  # list_display=['firstname','lastname','userimg','email','password','active']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display=['question','opt1','opt2','opt3','opt4','correct']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
  list_display=['user','totalquestion','totalgivenans','score','complete']
    

