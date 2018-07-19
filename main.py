# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 19:20:13 2018

@author: LIYifan

"""

"""
未解决问题：
\n\:等转义字符 机翻结果：会出现\缺失
{0}等参数 机翻结果：会出现{ 0 }中间插入了空格
"""
import re
from baidu_translate import *
#import机翻函数
f = open("LocaleResource_en_US.properties","r")
f1 = open("LocaleResource_zh_CN.properties",'w') 
is_untrans="# (\w+.){3}\: (\w+.){5}...(\w+.){4}"
#识别源文件中 Note to translators: DO NOT TRANSLATE THIS SECTION 的部分
is_note="#"
#识别源文件中 Note 部分
is_trans="([^=]+)(= *)(.*)"
#识别源文件语句，保留=和之前部分，后面为待翻译部分
is_dlec="([^\\]*)(\\+.)([^\\]*)"
#识别待翻译部分中是否含有转义字符
is_var="([^{]*)({\d})([^{]*)"
#识别待翻译部分中是否含有{0}等参数
is_set="[^<]*<[^>]*>[^<]*"
#识别待翻译部分中是否含有<>标记
is_split="([^<]*)(<[^>]*>)([^<]*)"
flag=0
for line in f.readlines():
    #按行读原文件
    if flag!=0:
        if re.match('\s',line):
            #判断行是否为空
            if flag==1:
                #如果是不要翻译note下的第一行为空行，直接写入目标文件
                f1.write(line)
                flag=flag+1
                continue
            else:
                #不要翻译note下第n行出现空行，写入当前行并重置flag
                #不要翻译部分直接全部写入目标文件
                f1.write(line)
                flag=0
                continue
        else:
            #不要翻译note下不为空的行，直接写入目标文件
            f1.write(line)
            flag=flag+1
            continue
    if re.match('\s',line):
        #该行为空，直接写入
        f1.write(line)
    elif '.htm' in line and '.html' not in line:
        #补足个别不在不要翻译备注下的文件路径
        f1.write(line)
    else:
        if re.match(is_note,line):
            #识别note行
            if re.match(is_untrans,line):
                #识别不要翻译的note
                f1.write(line)
                flag=1
                continue
            else:
                f1.write(line)
                continue
        get_trans=re.match(is_trans,line)
        #匹配源文件语句
        untrans1=get_trans.group(1)
        untrans2=get_trans.group(2)
        f1.write(untrans1)
        f1.write(untrans2)
        #1,2不用机翻，直接保留写入
        raw_line=get_trans.group(3)
        split_list=re.findall(is_set,raw_line)
        split_list1=re.findall(is_dlec,raw_line)
        split_list2=re.findall(is_var,raw_line)
        #匹配当前待翻译部分中含有<>标记的所有部分
        #此处split_list1和split_list2都没有真正运行
        #虽然考虑到了转义字符和{0}等参数显示的问题，但是一整句含有多种情况的问题无法解决。
        if split_list!=[]:
            for index,item in enumerate(split_list):
                #遍历每个含有<>的部分
                split_line=item
                trans_set=re.match(is_split,split_line)
                raw1=trans_set.group(1)
                raw3=trans_set.group(3)
                #1,3送去机翻
                if raw1=='' or raw1==' ':
                    trans1=raw1
                else:
                    trans1=baidu_translate(raw1)
                if raw3=='' or raw3==' ':
                    trans3=raw3
                else:
                    trans3=baidu_translate(raw3)
                trans_line=trans1+trans_set.group(2)+trans3
                f1.write(trans_line)
            f1.write('\n')
        else:
            #整句机翻
            if raw_line=='' or raw_line==' ':
                trans0=raw_line
            else:
                trans0=baidu_translate(raw_line)+'\n'
            f1.write(trans0)
            
            
        
        
        
f.close()
f1.close()