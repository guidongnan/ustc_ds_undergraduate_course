import requests
import re
import os



def scrapypage(url):
    
    #通过给定url爬取网页全部内容
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    response=requests.get(url=url,headers=headers)
    response.encoding='utf-8'
    page_text=response.text
    
    #利用正则表达式获取word_url
    ex='<p class="con-tool tr tm10">.*?<a href="(.*?)" downid=.*?</p>'
    word_url=re.findall(ex,page_text,re.S)[0]
    
    #获得文档内容
    word_data=requests.get(url=word_url,headers=headers).content
    
    #利用正则表达式获取word_name
    ex_name='<p class="c-b6 ti2">.*?</strong>(.*?)</p>'
    word_name=re.findall(ex_name,page_text,re.S)[0]
    
    #只获取非答案内容
    if('答案' in word_name):
        return False
    
    #建立存储文件夹
    word_ospath='./高考试题word版'
    if not os.path.exists(word_ospath):
        os.mkdir(word_ospath)
    
    #通过字符串分割获得要求的文件名
    word_list1=word_name.split('年')
    word_list2=word_list1[1].split('高考')
    word_list3=word_list2[1].split('试题')
    word_path=word_ospath+'./'+word_list1[0]+'_'+word_list2[0]+'_'+word_list3[0]+'.docx'
    
    #打开文件并写入，输出文件爬取成功信息
    with open(word_path,'wb') as fp:
        fp.write(word_data)
    print(word_path,'finished!')
    return True
    

def scrapyword(num,n):
    
    #函数爬取不同科目的word版试卷n份
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    
    #获取搜索的url
    list_name=['语文','数学','英语','文综','理综']
    url='http://tiku.gaokao.com/search/type0/'
    url=url+list_name[num]+'试题（word版）/pg'
    
    #初始化页码，以获得不同页面的信息
    page_num=1
    while(n>0):
        
        #如果爬取的页面个数不够时，再进行爬取
        
        #获取不同页面的url并爬取页面信息
        url=url+str(page_num)+'0'
        response=requests.get(url=url,headers=headers)
        response.encoding='utf-8'
        page_text=response.text
        
        #利用正则表达式获取所有word的url
        ex='<article class="result-item">.*?<a href="(.*?)" id=.*?</article>'
        page_url_list=re.findall(ex,page_text,re.S)
        
        #遍历所有page_url调用scrapypage函数
        for page_url in page_url_list:
            if(scrapypage(page_url)):
            #不爬取答案，另需爬取数目减1
                n=n-1
            if(n==0):
            #爬取结束
                break
        
        #没有爬取结束则爬取下一页
        page_num+=1


n=int(input("请输入爬取word总数："))
#每科爬取总数的五分之一份
for num in range(5):
    scrapyword(num,n/5)

print("爬取word完成！！！")