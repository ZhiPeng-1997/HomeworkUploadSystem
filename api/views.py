from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from page.models import Homework
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.






'''
apiUpload
返回编码含义：
-1 作业不存在
0 作业存在提交成功

超时提交未处理
'''
def apiUpload(request):
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False):
			return HttpResponse("请登录")
		stuID = request.session['account']#获取学号
		stuName = request.session['stuName']#获取学生姓名
		hwID = request.POST['hwID']#获取作业id
		#尝试通过hwID获取hwName
		#成功则存在该作业
		#否则不存在
		try:
			hw = Homework.objects.get(hwID = hwID)
		except Exception:
			hw = None
		if hw == None: #如若作业不存在
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		#开始写数据
		import os
		if not os.path.exists('static/file/'+ hwID):
			os.makedirs('static/file/'+ hwID)
		file = request.FILES['file']
		f = open('static/file/'+ hwID + '/'+ stuID + stuName + hw.hwName + "." + file.name.split('.')[-1],'wb+') #构建新的文件名 学号+姓名+作业名保存至相应文件夹
		for chunk in file.chunks():
			f.write(chunk)
		f.close()
		from page.models import HomeworkUpload,StuAccount #载入学生上传表
		try:
			HomeworkUpload.objects.filter(stuID=stuID,hwID=hwID).get()#如果不报错说明含有记录 为了避免重复
		except:#发生异常说明不存在
			HomeworkUpload.objects.create(stuID=stuID,hwID=hwID)#存入上传记录
		return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
'''
apiAddHomework
返回编码含义：
-1 提交失败
0 提交成功
-2 时间不合法
'''		
def apiAddHomework(request):
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False) or not request.session.get('isAdmin',False): #未登录或者无权限
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		import random
		import os
		import time
		import datetime
		from page.models import Homework
		hwID = ''.join(str(random.choice(str(int(time.time())))) for _ in range(10)) #随机数
		hwName = request.POST['hwName'] #作业名
		hwContent = request.POST['hwContent']
		hwStart = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		hwEnd = request.POST['endYear'] + '-' + request.POST['endMonth'] + '-' + request.POST['endDay'] + ' ' + request.POST['endHour'] + ':00:00'  #拼时间字符串
		try:#检验时间字符串的合法性
			#合法的话
			time.strptime(hwEnd,'%Y-%m-%d %H:%M:%S')
			Homework.objects.create(hwID=hwID,hwName=hwName,hwContent=hwContent,hwStart=hwStart,hwEnd=hwEnd)
			return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
		except:
			#不合法的话
			return HttpResponse(json.dumps({'message':'-2'}), content_type="application/json")
'''
apiDeleteHomework
返回编码含义：
-1 提交失败
0 提交成功
id:作业编号
'''		
def apiDeleteHomework(request,hwID):
	if request.method == 'POST':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'GET':
		if not request.session.get('isLogin',False) or not request.session.get('isAdmin',False):#验证权限
			return HttpResponse(json.dumps({'message':'-1','id':hwID}), content_type="application/json")
		Homework.objects.filter(hwID=hwID).delete()
		return HttpResponse(json.dumps({'message':'0','id':hwID}), content_type="application/json")
		
def apiAddNotice(request):#发布公告
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False) or not request.session.get('isAdmin',False): #未登录或者无权限
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		from page.models import notice
		noticeTitle = request.POST['noticeTitle'] #公告标题
		noticeContent = request.POST['noticeContent']#公告内容
		notice.objects.create(noticeTitle=noticeTitle,noticeContent=noticeContent)
		return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
'''
apiAddStatistic
返回编码含义：
0:成功
-1:失败 未登录或无权限
-2:时间不合法
'''	
def apiAddStatistic(request):
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False) or not request.session.get('isAdmin',False): #未登录或者无权限
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		import random
		import time
		from page.models import statistic
		id = 's' + ''.join(str(random.choice(str(int(time.time())))) for _ in range(9))
		title = request.POST['title'] #统计标题
		header = request.POST['tbheader']#统计表头
		allow = request.POST['allow']#允许名单
		end = request.POST['end']#截止时间
		
		#验证时间合法性
		try:
			time.strptime(end,'%Y-%m-%d %H:%M:%S')
		except:
			return HttpResponse(json.dumps({'message':'-2'}), content_type="application/json")
		
		statistic.objects.create(title=title,header=header,allow=allow,end=end,id=id)
		#创建带有表头的表格文件
		f = open('static/file/' + id + '.tsv','w',encoding='utf-8')
		#打散header，写入表头
		header = '\t'.join(header.split(';')) + '\n'            # xx\txxx\txxx\t\n 形式
		f.writelines(header)
		f.close()
		return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
		
def apiGetStatistic(request,id):
	from page.models import statistic
	return HttpResponse(json.dumps({'header':statistic.objects.get(id=id).header}), content_type="application/json")

'''
restful
GET:
	有参:获取新的,
		parma:last: models.talk.id
		return:
		{
			'last':xx, #返回JSON中的最新一个记录的ID
			1:{'nickname':'xxxx','content':'xxxxxx','time':'xx:xx:xx'},
			2:{---------------------------------------------------},
			.......
			x:{---------------------------------------------------}
		} 
	无参:获取50最新的当天的,
		return:
		{
			'last':xx, #返回JSON中的最新一个记录的ID
			1:{'nickname':'xxxx','content':'xxxxxx','time':'xx:xx:xx'},
			2:{---------------------------------------------------},
			.......
			x:{---------------------------------------------------}
		} 
POST:添加一个新的
		parma:
			{
				'nickname':'xxxxxxxx',
				'content':'xxxxxxxxx',
				'time':'xx:xx:xx'
			}
		return:
			{
				'message':0 #OK  other #failed
			}
'''	
@csrf_exempt
def apiTalk(request):
	if request.method == 'GET':#HTTP METHOD  GET ~~~获取
		last_id = request.GET.get('last',None)#容错
		return HttpResponse(getTalk(last_id), content_type="application/json")
	else: #POST
		nickname = request.POST.get('nickname',None)
		content = request.POST.get('content',None)
		talk_time = request.POST.get('time',None)
		stuID = request.session.get('account','null')
		if not (nickname or content or talk_time):#如果三者任意为空
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		from page.models import talk
		talk.objects.create(nickname=nickname,content=content,talk_time=talk_time,stuID=stuID)
		return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
		
		
			
			
'''
0:成功
-1:失败 未登录
-2:表单验证失败
-3:不在允许列表
-4:不存在此项统计
'''
def apiReplyStatistic(request):
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False): #未登录或者无权限
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		from page.models import statistic
		id = request.POST['id']
		header = request.POST['header']
		columnContent = request.POST['columnContent']
		
		try:
			statisticItem = statistic.objects.get(id=id) #获取某项统计
		except:#获取失败则不存在
			return HttpResponse(json.dumps({'message':'-4'}), content_type="application/json")
		
		if not statisticItem.header == header:#如果表头验证失败
			return HttpResponse(json.dumps({'message':'-2'}), content_type="application/json")
		
		allowed = True #是否允许的标志变量
		#存在允许名单的情况下
		if not statisticItem.allow == 'null':
			stuID = request.session['account']
			allowed = True if not statisticItem.allow.find(stuID) == -1 else False
		#不存在允许名单的情况下
		if allowed:
			with open('static/file/' + id + '.tsv','a',encoding='utf-8') as f:
				f.writelines('\t'.join(columnContent.split(';')) + '\n')
			return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({'message':'-3'}), content_type="application/json")
'''
apiZipFiles
返回编码含义：
0:成功
非0:失败 系统调用错误号
'''		
def apiZipFiles(request):
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False) or not request.session.get('isAdmin',False): #未登录或者无权限
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		import os
		BASE_DIR_ = '/var/www/HomeworkUploadSystem/static/file/'
		hwID = request.POST['hwID']
		statu = str(os.system('zip -rj ' + BASE_DIR_ + str(hwID) + '.zip ' + BASE_DIR_ + str(hwID)))
		if not statu == '0':
			return HttpResponse(json.dumps({'message':statu}), content_type="application/json")
		return HttpResponse(json.dumps({'message':'0','file':str(hwID) + '.zip'}), content_type="application/json")
		
def apiDownloadFile(request,file):
	if request.method == 'POST':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'GET':
		if not request.session.get('isLogin',False) or not request.session.get('isAdmin',False): #未登录或者无权限
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		from django.http import FileResponse
		BASE_DIR_ = '/var/www/HomeworkUploadSystem/static/file/'
		response = FileResponse(open(BASE_DIR_ + file ,'rb')) #读文件到response
		response['Content-Type']='application/octet-stream'
		response['Content-Disposition']='attachment;filename='+ file
		return response
		
def apiUploadInfo(request):
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False) or not request.session.get('isAdmin',False): #未登录或者无权限
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		from page.models import HomeworkUpload,StuAccount
		BASE_DIR_ = '/var/www/HomeworkUploadSystem/static/file/'
		hwID = request.POST['hwID']
		hwup = HomeworkUpload.objects.filter(hwID=hwID).order_by('stuID') #查询该作业的记录
		f = open(BASE_DIR_ + hwID + '.tsv','w')
		for item in hwup:
			f.writelines(item.stuID + '\t' + StuAccount.objects.get(stuID=item.stuID).stuName + '\t\n')
		f.close()
		return HttpResponse(json.dumps({'message':'0','file':str(hwID) + '.tsv'}), content_type="application/json")
		
def apiChangePassword(request):
	if request.method == 'GET':
		return HttpResponse("请以正确方式使用该url")
	elif request.method == 'POST':
		if not request.session.get('isLogin',False):
			return HttpResponse("请登录")
		from page.models import StuAccount
		stuID = request.session['account']
		oldPassword = request.POST['oldPassword']
		newPassword = request.POST['newPassword']
		if not StuAccount.objects.get(stuID=stuID).stuPassword == oldPassword:#如果密码不正确
			return HttpResponse(json.dumps({'message':'-1'}), content_type="application/json")
		StuAccount.objects.filter(stuID=stuID).update(stuPassword = newPassword)
		#清除session
		del request.session['isLogin']
		del request.session['account']
		del request.session['password']
		del request.session['stuName']
		return HttpResponse(json.dumps({'message':'0'}), content_type="application/json")
		
def getTalk(last_id):
	import datetime
	from page.models import talk
	if last_id:#有参
		talk_content = talk.objects.filter(id__gt=last_id,talk_date=datetime.datetime.now().strftime('%Y-%m-%d')).order_by('id')[0:50]
	else:
		talk_content = talk.objects.filter(talk_date=datetime.datetime.now().strftime('%Y-%m-%d')).order_by('id')[0:50]
	#转化为JSON
	talks = {}
	for item in talk_content:
		#item 数据库内的具体一条记录
		#key:value
		talks[item.id] = {'nickname':item.nickname,'content':item.content,'time':item.talk_time}
	talks['last'] = talk_content[len(talk_content)-1].id if len(talk_content)>0 else (last_id if last_id else 0)
	return json.dumps(talks)
		