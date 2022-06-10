#import urllib2
import re
import string
import operator
import os
import json
import re 
import argparse

path=os.getcwd()

#设置命令
parser = argparse.ArgumentParser(description='生成词频字典')
parser.add_argument('-g', type=int, help="输入想要生成词频字典的词数（'n-gram'的'n')")
parser.add_argument('-d', type=str, help="输入想要生成词频字典的类型：'Y'为区分大小写,'N'为不区分大小写")

args = parser.parse_args()


def cleanText(input,Dul):
    if(str(Dul)=='Y'):
        input = re.sub('\n+', " ", input) # 匹配换行用空格替换成空格
    else:
        input = re.sub('\n+', " ", input).lower() # 匹配换行用空格替换成空格
    input = re.sub('\t+', " ", input) # 匹配置位用空格替换成空格
    input = re.sub('\[[0-9]*\]', "", input) # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    input = bytes(input.encode('utf-8'))#.encode('utf-8') # 把内容转换成utf-8格式以消除转义字符
    
    #print(type(input))#input = input.decode("ascii", "ignore")
    return input

def cleanInput(input,Dul):
    input = cleanText(input,Dul)
    cleanInput = []
    input = input.decode().split(' ') #以空格为分隔符，返回列表


    for item in input:
        item = item.strip(string.punctuation) # string.punctuation获取所有标点符号

        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'): #找出单词，包括i,a等单个单词(其他的单个字母的查找没有意义)
            cleanInput.append(item)
    return cleanInput

def getNgrams(output,input, n ,Dul):
    input = cleanInput(input,Dul)

    
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])#.encode('utf-8')
        if ngramTemp not in output: #词频统计
            output[ngramTemp] = 0 #典型的字典操作
        output[ngramTemp] += 1
    return output


if __name__=='__main__':
    
    Ngram=int(args.g)
    Dul=str(args.d)
    path1=path+'/file/articles'
    Filelist=os.listdir(path1)
    #方法一：对网页直接进行读取
    #content = urllib2.urlopen(urllib2.Request("http://pythonscraping.com/files/inaugurationSpeech.txt")).read()
    #方法二：对本地文件的读取，测试时候用，因为无需联网
    #content = open("1.txt").read()

    output = {} # 构造字典
    for i0 in range(0,len(Filelist)):
        print(i0,Filelist[i0])
        content = open(path+'/file/articles/'+Filelist[i0]).read()
        ngrams = getNgrams(output,content,Ngram, Dul)
        sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True) #=True 降序排列
        output=ngrams

    fr = open(path+'/word_library.txt','w')
    for i in range(0,len(sortedNGrams)):
        fr.write('%s\t%s\n' %(sortedNGrams[i][0],sortedNGrams[i][1]))
    fr.close()
    #print(sortedNGrams)


    #转化为用json.dumps写入文件
    worddict=dict()

    fr=open(path+'/word_library.txt','r')
    for lines in fr:
        lines = re.sub('\n+', "", lines)#剔除文件中换行符
        lines0=lines.split('\t')
        worddict[lines0[0]]=lines0[1]

    fr.close()


    js = json.dumps(worddict, indent=1)   
    file = open(path+'/file/word_dictionary.txt', 'w')  
    file.write(js)  
    file.close()  
