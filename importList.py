#coding:utf-8
 
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomeworkUploadSystem.settings")
 
'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
 
import django
if django.VERSION >= (1, 7):#自动判断版本
	django.setup()
 
 
def main():
	fileName = sys.argv[1]
	if not fileName:
		return -1
	from page.models import StuCheck
	f = open(fileName,'r',encoding='utf-8')
	for line in f:
		line = line.split('\t')
		StuCheck.objects.create(stuID=line[0],phone=line[1].replace('\n',''))
	f.close()
    
 
if __name__ == "__main__":
	main()
	print('Done!')
