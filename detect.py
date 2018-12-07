#coding:utf-8
 
import os
import sys
import time
import datetime
import del_func as df
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
 
from page.models import Homework,HomeworkUpload

def getHomework_admin():
	import datetime
	homeworks = Homework.objects.filter(hwEnd__lt=(datetime.datetime.now()-datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')).order_by('-hwStart')#筛选无效作业
	return homeworks
	
def main():
	while True:
		now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '|||'
		print(now + '检测开始')
		try:
			homeworks = getHomework_admin()
		except:
			time.sleep(3600)
			continue
		for homework in homeworks:
			print( now + '检测到过期作业:' + homework.hwName + '\t过期时间：' + str(homework.hwEnd) )
			Homework.objects.filter(hwID=homework.hwID).delete()
			HomeworkUpload.objects.filter(hwID=homework.hwID).delete()
			print( now + '删除了作业，编号为：' + homework.hwID)
			
			print(now + '删除关联文件：' + df.deleteFile(homework.hwID))
			print(now + '删除关联文件夹：' + df.deleteFolder(homework.hwID))
			print('done--------------------------------------------------------------------------------')
		time.sleep(3600)
		
			
	
    
 
if __name__ == "__main__":
	main()
	print('Done!')

