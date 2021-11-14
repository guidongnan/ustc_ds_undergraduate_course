import requests
import re
import os

def scrapypage(urlfirst):
    
    #爬取以urlfirst为链接的页面的一系列图片
    
    if not os.path.exists('./高考试题图片版'):
        os.mkdir('./高考试题图片版')
        
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    
    #对每一页面进行爬取，30为预设最大页面数
    for page_number in range(1,30):
        
        url=urlfirst.split('.shtml')[0]
        #得到不同页面的url
        
        #对第一页，url不同，单独操作
        if(page_number==1):
            
            #获取页面数据
            url=url+'.shtml'
            response=requests.get(url=url,headers=headers)
            response.encoding = 'gb2312'
            page_text=response.text
            
            #利用正则表达式获取图片url
            ex='<p style="text-align: center;">.*?src="(.*?)" style.*?</p>'
            img_src0=re.findall(ex,page_text,re.S)
            if(not img_src0):
                return False
            img_src=img_src0[0]
            
            
            #获取图片名称
            ex_name='<h1>.*?target="_blank">(.*?)</a>.*?</h1>'
            img_name=re.findall(ex_name,page_text,re.S)[0]
            
            #利用字符串操作获取要求图片名称
            if('试题' not in img_name):
                return False
            img_namelist1=img_name.split('年')
            img_namelist2=img_namelist1[1].split('高考')
            img_namelist3=img_namelist2[1].split('试题')
            
            img_ospath=img_namelist1[0]+'_'+img_namelist2[0]+'_'+img_namelist3[0]
            
            
            
            #获取图片二进制名称
            img_data=requests.get(url=img_src,headers=headers).content
            
            #创建文件夹
            if not os.path.exists('./高考试题图片版/'+img_ospath):
                os.mkdir('./高考试题图片版/'+img_ospath)
            
            #得到图片名称
            img_path='./高考试题图片版/'+img_ospath+'/'+img_ospath+'_'+str(page_number)+'.jpg'
            
            #二进制方式写入图片
            with open(img_path,'wb') as fp:
                fp.write(img_data)
            
            print(img_path,'finished!')
            
        else:
            #获取不同页面的url
            url=url+'_'+str(page_number)+'.shtml'
            
            #无异常访问页面，有异常(没有新的url,爬取完成)跳过访问
            try:
                
                response=requests.get(url=url,headers=headers)
                response.encoding = 'gb2312'
                page_text=response.text
                
                #利用正则表达式获取图片url
                ex='<p style="text-align: center;">.*?src="(.*?)" style.*?</p>'
                img_src=re.findall(ex,page_text,re.S)[0]
                
                #得到图片二进制内容和存储路径
                img_data=requests.get(url=img_src,headers=headers).content            
                img_path='./高考试题图片版/'+img_ospath+'/'+img_ospath+'_'+str(page_number)+'.jpg'
                
                #写入文件
                with open(img_path,'wb') as fp:
                    fp.write(img_data)
                    
                print(img_path,'finished!')
                
            except(IndexError):
                #有异常则直接退出函数
                return True

def scrapyjpg(n):
#爬取指定页面图片信息，爬取总数为n
    
    url='http://www.gaokao.com/zyk/gkst/'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    
    #获取页面信息
    response=requests.get(url=url,headers=headers)
    response.encoding='gb2312'
    page_text=response.text
    
    #利用正则表达式获取.shtml链接
    ex='<td width="25%">.*?<a href="(.*?)" target.*?</td>'
    url_list=re.findall(ex,page_text,re.S)
    print(url_list[:20])
    return
    #获取含'.shtml'的链接
    url_lists=[]
    for url in url_list:
        if('.shtml' in url):
            url_lists.append(url)
            
    #去除重复元素
    url_newlist=list(set(url_lists))

#调用scrapypage函数爬取制定url的图片
    list_number=0
    while(n>0):
        if(scrapypage(url_lists[list_number])):
            n=n-1
            list_number+=1
        else:
            list_number+=1
        

n=int(input("请输入要爬取的图片版试卷份数："))
scrapyjpg(n)