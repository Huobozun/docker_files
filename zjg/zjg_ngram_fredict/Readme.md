
#/zjg_ngram_fredict文件夹下有/file文件夹，其中又有一个文件夹/articles，其中存放需要提取词频的文章，可以是多篇，格式不限。  

#当需要进行提取词频字典的工作时，首先需要将想要提取的文章放到/file/articles文件夹下，将路径改到zjg_ngram_fredict下,然后再运行python3 n-gram.py -g 1 -d N 即可。  

  生成词频字典  

  optional arguments:  
    -h, --help  show this help message and exit  
    -g G        输入想要生成词频字典的词数（'n-gram'的'n')  
    -d D        输入想要生成词频字典的类型：'Y'为区分大小写,'N'为不区分大小写  


  '-g'表示查找词频字典的词数，类型为int；'-d'表示是否区分大小写，'Y'表示区分大小写，即最后生成的词频字典区分大小写。'N'表示不区分大小写，即最后生成的词频字典一律小写。  

运行完指令后，就会生成词频字典word_dictionary.txt,并自动保存在本地/file目录下  
word_dictionary.txt格式如下：  

{  
 "the": "1466",  
 "of": "1285",  
 "and": "1011",  
 "in": "781",  
 "a": "663",  
 "to": "508",  
 "with": "484",  
 "for": "308",  
 "is": "243",  
 "was": "218",  
 "patients": "178",  
 "were": "178",  
 "this": "160",  
 "on": "152",  
 "by": "150"  
 }  

