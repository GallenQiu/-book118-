# -book118-
'''写了个小爬虫，爬取文档投稿赚钱网（book118）的pdf、word文档并生成pdf文件
为什么要写这个爬虫呢？因为我差点被这个网站的文档下载收费气死，明明是搬来搬去的文件，凭什么在这个网站拿来卖钱，而且价格高的不可理喻。
因为刚好它提供免费全文预览，按照爬虫思想：只要是在浏览器上显示的，理论上就可以download。很好，按照这个思路我就写了这个爬虫工具。'''
	
	使用注意：在run.py统计目录下建立两个文件夹：分别命名：图片、文件库
	使用注意：在run.py统计目录下建立两个文件夹：分别命名：图片、文件库
	使用注意：在run.py统计目录下建立两个文件夹：分别命名：图片、文件库

作用：
	下载pdf、word（不包括ppt哦，因为我看到ppt是js生成的），然后转存为pdf文件
	
使用方法：

	一、运行
		run.py,在交互界面把你要下载的文件当前网址复制下来，粘贴上去，鼠标移动到冒号前按enter。
  
	二、注意事项：
    	我发现这个网站的响应有时候会卡并且慢，所以如果报错什么的，重新run一次就行，一般都可以解决。
	还有一点，因为响应慢，所以下载文件页面时，如果太多页，速度你懂的，我觉得是网站的错哈哈哈，其实我程序也只是花不到一天写的，优化还是不够的，但思考下时间成本和收益，emm勉强能拿去用就行吧。
  
	三、pdf横向、纵向修改
	`在img.py中找到如下代码修改：`
   	 #修改PDF文件方向：-默认纵向，改direction为其他则是横向
		direction= '|'
		if direction== '-':
		    imgDoc.setPageSize(landscape(A4))
		    document_width,document_height = landscape(A4)
		else:
		    imgDoc.setPageSize(A4)
		    document_width, document_height = A4
            
 特别鸣谢：
  本程序中参考了某位大神的图片转pdf程序，原github：https://github.com/ilovin/stitch_img_to_pdf。
