from django.contrib import admin
from .models import StuAccount,Homework,HomeworkUpload,Admin,StuCheck
# Register your models here.
admin.site.register(StuAccount)
admin.site.register(Homework)
admin.site.register(HomeworkUpload)
admin.site.register(Admin)
admin.site.register(StuCheck)