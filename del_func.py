#coding:utf-8
 
import os
import sys
import time
import datetime
import platform
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomeworkUploadSystem.settings")
import django
if django.VERSION >= (1, 7):#自动判断版本
	django.setup()


osName = platform.system()
if(osName == 'Windows'):
	HOMEWORK_PATH = 'static\\file\\'
	DELETE_FOLDER_COMMAND = 'rmdir /s/q ' + HOMEWORK_PATH
	DELETE_FILE_COMMAND = 'del /f/q ' + HOMEWORK_PATH
elif(osName == 'Linux'):
	HOMEWORK_PATH = 'static/file/'
	DELETE_FOLDER_COMMAND = 'rm -rf ' + HOMEWORK_PATH
	DELETE_FILE_COMMAND = 'rm -f ' + HOMEWORK_PATH

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
''' 

 
def deleteFile(id):
	statu_zip = os.system(DELETE_FILE_COMMAND + id + '.zip')
	statu_tsv = os.system(DELETE_FILE_COMMAND + id + '.tsv')
	return 'zip删除：%(zip)s，tsv删除：%(tsv)s'%{'zip':statu_zip,'tsv':statu_tsv}
	
def deleteFolder(id):
	statu = os.system(DELETE_FOLDER_COMMAND + id)

	return '文件夹删除：%(code)s'%{'code':statu}