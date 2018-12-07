var homeworkAdd= function(){//提交表单
	fd = new FormData() //构建FormData
	if(!$("#hwContent").val()||!$("#hwName").val()||!$("#addHomework #endYear").val()||!$("#addHomework #endMonth").val()||!$("#addHomework #endDay").val()||!$("#addHomework #endHour").val()){
		alert('请完整填写')
		return
	}
	if((
		/\[2017-2019\]/g.test($('#addHomework #endYear').val())&&
		/\[1-12\]/g.test($('#addHomework #endMonth').val()) &&
		/\[1-31\]/g.test($('#addHomework #endDay').val()) &&
		/\[0-23\]/g.test($('#addHomework #endHour').val()) &&
		(/^[0-9]{1,20}$/.test($('#addHomework #endYear').val()),
		/^[0-9]{1,20}$/.test($('#addHomework #endMonth').val()),
		/^[0-9]{1,20}$/.test($('#addHomework #endDay').val()),
		/^[0-9]{1,20}$/.test($('#addHomework #endHour').val())
		)
	)){
		alert('请输入正确的日期')
		return
	}
	fd.append('hwName',$('#hwName').val()) //标题
	fd.append('hwContent',$('#hwContent').val())
	fd.append('endYear',$('#addHomework #endYear').val())
	fd.append('endMonth',$('#addHomework #endMonth').val())
	fd.append('endDay',$('#addHomework #endDay').val())
	fd.append('endHour',$('#addHomework #endHour').val())
	fd.append('csrfmiddlewaretoken',$('input[name=csrfmiddlewaretoken]').val())
	//console.log(fd.get("file"))
	//上传开始
	$.ajax({
		url: '/api/addHomework',
		type: 'POST',
		processData:false,
		contentType: false,
		data: fd, //获取表单数据
		success:function(res){
			console.log(res)
			if(res['message'] == 0){
				alert('提交成功！')
			}
			else if(res['message'] == -2){
				alert('时间不合法！')
			}
			else{
				alert('提交失败！')
			}
		},
		error:function(){
			alert('提交失败，请检查网络！')
		}
	})
}
var noticeAdd = function(){
	fd = new FormData() //构建FormData
	if(!$("#noticeContent").val()||!$("#noticeTitle").val()){
		alert('请完整填写')
		return
	}
	fd.append('noticeTitle',$('#noticeTitle').val()) //标题
	fd.append('noticeContent',$('#noticeContent').val())
	fd.append('csrfmiddlewaretoken',$('input[name=csrfmiddlewaretoken]').val())
	//console.log(fd.get("file"))
	//上传开始
	$.ajax({
		url: '/api/addNotice',
		type: 'POST',
		processData:false,
		contentType: false,
		data: fd, //获取表单数据
		success:function(res){
			console.log(res)
			if(res['message'] == 0){
				alert('提交成功！')
			}
			else{
				alert('提交失败！')
			}
		},
		error:function(){
			alert('提交失败，请检查网络！')
		}
	})
	
}

var downloadFile = function(id,url){
	fd = new FormData() //构建FormData
	fd.append('hwID',id)
	fd.append('csrfmiddlewaretoken',$('input[name=csrfmiddlewaretoken]').val())
	//console.log(fd.get("file"))
	//上传开始
	$.ajax({
		url: url,
		type: 'POST',
		processData:false,
		contentType: false,
		data: fd, //获取表单数据
		success:function(res){
			console.log(res)
			if(res['message'] == 0){
				fileName = res['file']
				window.location = 'api/downloadFile/' + fileName
			}
			else{
				alert('失败,请查看作业是否无人提交！')
			}
		},
		error:function(){
			alert('提交失败，请检查网络！')
		}
	})
	
}
var homeworkDelete = function(url){
	if (confirm('确定删除吗?')==true){  
		$.ajax({
			url: url,
			type: 'GET',
			success:function(res){
				console.log(res)
				if(res['message'] == 0){
					alert('删除成功！')
				}
				else{
					alert('删除失败！')
				}
			},
			error:function(){
				alert('提交失败，请检查网络！')
			}
		}) 
	}else{  
		return false;  
	}  
}
var statisticAdd = function(id){
	//获取值
	/**/
	title = $('#statistics-title').val()
	/**/
	header = (()=>{
		temp = '' //返回给header 开始拼凑
		father_ele = $('#statistics-content .statistics-content-item')
		father_ele.each(
			(index,item)=>{
				if($(item).val()){
					temp = temp + $(item).val() + ';'
				}
			}
		)
		return temp.substring(0,temp.length-1)
	})()
	/**/
	end = (()=>{
		date = (()=>{ //拼日期串
			temp = ''
			$('#statistics-time input:not(#endHour)').each(
				(index,item)=>{
					if($(item).val()){
						temp = temp + $(item).val() + '-'
					}
					else{
						temp = null
						return
					}
				}
			)

			return temp?temp.substring(0,temp.length-1):null
		})()
		time = (()=>{
			if(!date||!$('#statistics-time #endHour').val()){
				return null
			}
			return $('#statistics-time #endHour').val() + ':00:00'
		})()
		if(!date||!time){
			return null
		}
		return date + ' ' + time
	})()
	/**/
	allow = (()=>{
		switch_ = $("#statistics-switch")
		if(switch_.prop("checked")){
			return $('#allowList').val()
		}
		return 'null'
	})()
	/**/
	if(!title||!header||!end){
		alert('请完整填写！')
		console.log(title,header,end)
		return
	}
	console.log(title,header,end,allow)
	/**/
	/*formdata构建*/
	fd = new FormData()
	fd.append('title',title)
	fd.append('tbheader',header)
	fd.append('end',end)
	fd.append('allow',allow)
	fd.append('csrfmiddlewaretoken',$('input[name=csrfmiddlewaretoken]').val())
	console.log(fd)
	/*ajax开始*/
	$.ajax({
		url: '/api/addStatistic',
		
		data: fd,
		
		type: 'POST',
		
		processData:false,
		
		contentType: false,
		
		success:function(res){
			if(res['message']=='0'){
				alert('提交成功')
			}
			else if(res['message']=='-2'){
				alert('提交失败，时间不合法！')
			}
			else{
				alert('提交失败')
			}
		},
		error:function(e){
			alert('提交失败，请检查网络或服务器！')
		}
			
		
	})
	
	
	
}