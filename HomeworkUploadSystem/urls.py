"""HomeworkUploadSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from page import views as page
from api import views as api
urlpatterns = [
	path('admin/admin', admin.site.urls),
	path('',page.index),
	path('index',page.index,name='index'),
	path('login/mobile',page.mobile_login,name='mobile_login'),
	path('login',page.login,name='login'),
	path('talk', page.talk,name='talk'),
	path('signin',page.signIn,name='signIn'),
	path('homework/<str:hwID>',page.homeworkDetail,name='homeworkDetail'),
	path('notice/<str:noticeID>',page.noticeDetail,name='noticeDetail'),
	
	path('api/talk',api.apiTalk,name='apiTalk'),
	path('api/upload',api.apiUpload,name='apiUpload'),
	path('api/addHomework',api.apiAddHomework,name='apiAddHomework'),
	path('api/deleteHomework/<str:hwID>',api.apiDeleteHomework,name='deleteHomework'),
	path('api/addNotice',api.apiAddNotice,name='addNotice'),
	path('api/zipFiles',api.apiZipFiles,name='apiZipFiles'),
	path('api/downloadFile/<str:file>',api.apiDownloadFile,name='apiDownloadFile'),
	path('api/uploadInfo',api.apiUploadInfo,name='apiUploadInfo'),
	path('api/changePassword',api.apiChangePassword,name='apiChangePassword'),
	path('api/addStatistic',api.apiAddStatistic,name='apiAddStatistic'),
	path('api/getStatistic/<str:id>',api.apiGetStatistic,name='apiGetStatistic'),
	path('api/replyStatistic',api.apiReplyStatistic,name='apiReplyStatistic'),

	
	path('upload',page.upload,name='upload'),
	path('profile',page.myProfile,name='profile'),

	path('admin', page.admin,name='admin'),
	path('quit',page.quit,name='quit'),
]
