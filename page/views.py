# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def index(request):#首页
	if not request.session.has_key('isLogin') or not request.session.get('isLogin',False): #检查是否登录
		return render(request,'index.html',{'isLogin':False,'homeworks':getHomework_stu(),'notices':getNotice(),'statistics':getStatistics()})
	else:
		stuName = request.session.get('stuName',None)
		isAdmin = request.session.get('isAdmin',False)
		return render(request,'index.html',{'isLogin':True,'loginName':stuName,'homeworks':getHomework_stu(),'isAdmin':isAdmin,'notices':getNotice(),'statistics':getStatistics()})
	
def login(request):
	if request.method == 'GET':#如果为GET则为正常访问
		if not request.session.has_key('isLogin') or not request.session.get('isLogin',False):#如果真的未登录
			return render(request,'login.html',{'isLogin':False})
		else:#如果已登录，错误访问
			return HttpResponseRedirect('/index')
	else:#如果为POST即为登录
		from .models import StuAccount,Admin #引入学生信息名单模型，验证密码
		account = request.POST['account'] #获取登录账号
		password = request.POST['password']
		#查询学生信息
		try:
			student = StuAccount.objects.get(stuID = account) #进行一次查询
		except Exception:
			student = None
		if not student == None and student.stuPassword == password: #验证成功，允许登陆
			#判断是否为管理员
			try:
				temp_admin = Admin.objects.get(stuID = account) #管理员则追加
				request.session['isAdmin'] = True;
			except Exception:
				pass
			request.session['isLogin'] = True
			request.session['stuName'] = student.stuName
			request.session['account'] = student.stuID
			request.session['password'] = student.stuPassword
			return HttpResponseRedirect('/index')
		else:
			return render(request,'login.html',{'isLogin':False,'loginFail':True})
			
def mobile_login(request):
	if request.method == 'GET':#如果为GET则为正常访问
		if not request.session.has_key('isLogin') or not request.session.get('isLogin',False):#如果真的未登录
			return render(request,'login_mobile.html',{'isLogin':False})
		else:#如果已登录，错误访问
			return HttpResponseRedirect('/index')
	else:#如果为POST即为登录
		from .models import StuAccount,Admin #引入学生信息名单模型，验证密码
		account = request.POST['account'] #获取登录账号
		password = request.POST['password']
		try:
			student = StuAccount.objects.get(stuID = account) #进行一次查询
		except Exception:
			student = None
		if not student == None and student.stuPassword == password: #验证成功，允许登陆
			try:
				temp_admin = Admin.objects.get(stuID = account) #管理员则追加
				request.session['isAdmin'] = True;
			except Exception:
				pass
			request.session['isLogin'] = True
			request.session['stuName'] = student.stuName
			request.session['account'] = student.stuID
			request.session['password'] = student.stuPassword
			return HttpResponseRedirect('/index')
		else:
			return render(request,'login_mobile.html',{'isLogin':False,'loginFail':True})
	
def talk(request):
	if not request.session.has_key('isLogin') or not request.session.get('isLogin',False): #检查是否登录
		return render(request,'talk.html',{'isLogin':False})
	else:
		stuName = request.session.get('stuName',None)
		isAdmin = request.session.get('isAdmin',False)
		return render(request,'talk.html',{'isLogin':True,'loginName':stuName})

def signIn(request):
	if request.method == 'GET':#如果为GET则为正常访问
		if not request.session.has_key('isLogin') or not request.session.get('isLogin',False):#如果真的未登录
			return render(request,'signin.html')
		else:#如果已登录，错误访问
			return HttpResponseRedirect('/index')
	else:#如果为POST即为注册
		import json
		from .models import StuAccount,StuCheck #引入学生信息名单模型，验证密码
		account = request.POST['account'] #获取登录账号
		password = request.POST['password']
		name = request.POST['name']
		phone = request.POST['phone']
		#查询学生信息
		try:
			StuCheck.objects.get(stuID=account,phone=phone)#验证是否存在允许名单，存在则继续
			try:
				StuAccount.objects.get(stuID=account)#是否已注册
				return HttpResponse(json.dumps({'message':'-2'}), content_type="application/json")
			except:
				StuAccount.objects.create(stuID=account,stuPassword=password,stuName=name)
				return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
		except:
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")

def myProfile(request):
	if not request.session.has_key('isLogin') or not request.session.get('isLogin',False): #检查是否登录
		return HttpResponseRedirect('/index')#未登录则返回首页
	else:
		from .models import HomeworkUpload,Homework
		stuID = request.session.get('account','0')
		stuName = request.session.get('stuName',None)
		isAdmin = request.session.get('isAdmin',False)
		try:
			homeworks = HomeworkUpload.objects.filter(stuID=stuID).order_by('-id')[0:9]  #切片获取前十个,根据时间
		except:
			homeworks = None
		homeworksInfo = []#交作业情况
		for item in homeworks:
			homeworksInfo.append(Homework.objects.get(hwID=item.hwID).hwName)
		return render(request,'profile.html',{'isLogin':True,'loginName':stuName,'isAdmin':isAdmin,'homeworksInfo':homeworksInfo})
		
	
def quit(request):
	try:
		del request.session['isLogin']
		del request.session['account']
		del request.session['password']
		del request.session['stuName']
	except:
		pass
	return HttpResponseRedirect('/index')
	
def upload(request):
	if not request.session.has_key('isLogin') or not request.session.get('isLogin',False): #检查是否登录
		return render(request,'uploadPage.html',{'isLogin':False})
	else:#如果登录
		isAdmin = request.session.get('isAdmin',False)#是否有管理员权限
		stuName = request.session.get('stuName')
		return render(request,'uploadPage.html',{'isLogin':True,'loginName':stuName,'isAdmin':isAdmin,'homeworks':getHomework_stu()})#渲染
		
def admin(request):
	isLogin = request.session.get('isLogin',False)
	isAdmin = request.session.get('isAdmin',False)
	if isLogin and isAdmin:#如果登录且是管理员
		stuName = request.session.get('stuName',None)
		return render(request,'admin.html',{'isLogin':True,'loginName':stuName,'isAdmin':isAdmin,'homeworks':getHomework_admin(),'statistics':getStatistics_admin()})
	else:#不是管理员则跳转
		return HttpResponseRedirect('/index')

def homeworkDetail(request,hwID):
	from .models import Homework
	try:
		hw = Homework.objects.filter(hwID = hwID).get()
		return render(request,'detail.html',{'homework':hw})
	except:
		return HttpResponseRedirect('/index')

		
def noticeDetail(request,noticeID):
	from .models import notice
	try:
		nt = notice.objects.filter(id = noticeID).get()
		return render(request,'detail.html',{'notice':nt})
	except:
		return HttpResponseRedirect('/index')
		
		
		
		
		
		
		
		
		
		
		
def getHomework_stu():
	import datetime
	from .models import Homework
	homeworks = Homework.objects.filter(hwEnd__gt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')).order_by('-hwStart')#筛选有效作业
	return homeworks
	
def getHomework_admin():
	import datetime
	from .models import Homework
	homeworks = Homework.objects.filter(hwEnd__gt=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')).order_by('-hwStart')#筛选有效作业
	return homeworks

def getNotice():
	from .models import	notice
	return notice.objects.order_by('-id')[0:4]
	
def getStatistics():#获取有效统计
	import datetime
	from .models import statistic
	statistics = statistic.objects.filter(end__gt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')).order_by('-id')
	return statistics
	
def getStatistics_admin():#获取有效统计
	import datetime
	from .models import statistic
	statistics = statistic.objects.filter(end__gt=(datetime.datetime.now()-datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')).order_by('-id')
	return statistics
	