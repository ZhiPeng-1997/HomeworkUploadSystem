var formSubmit= function(){//提交表单
	fd = new FormData() //构建FormData

	if( $('#homework-choose option:selected').val() == '0' ){
		alert('请选择作业！')
		return
	}
	if( $('#file').val() == '' ){
		alert('请上传文件！')
		return
	}
	if($('#file')[0].files[0].size > 10*1024*1024){
		alert('上传文件过大，不要超过10M！')
		return
	}
	fd.append('file',$('#file')[0].files[0]) //文件
	fd.append('hwID',$('#homework-choose option:selected').val())//作业ID
	fd.append('csrfmiddlewaretoken',$('input[name=csrfmiddlewaretoken]').val())
	//console.log(fd.get("file"))
	$("#file-progress").show() //显示进度条
	//上传开始
	$.ajax({
		url: '/api/upload',
		type: 'POST',
		contentType:"multipart/form-data",
		data: fd, //获取表单数据
		processData: false, // 不处理发送的数据
        contentType: false, //不设置Content-Type请求头
		xhr:function(){
			thisXhr = $.ajaxSettings.xhr()
			if(thisXhr.upload){
				thisXhr.upload.addEventListener('progress',function(e){
					progress = parseInt(100*e.loaded/e.total) + "%" //计算进度
					$('#progress-bar').css('width',progress) //改变长度
					$('#progress-bar').text(progress) //改变内容
				},false)
			}
			return thisXhr
		},
		success:function(res){
			console.log(res)
			if(res['message'] == 0){
				alert('上传成功！')
			}
			else{
				alert('上传失败！')
			}
		},
		error:function(){
			alert('上传失败，请检查网络！')
		}
	})
}