将路径改到zjg_translate下，然后python3 translate_allwords.py即可将/needtran-words的文件翻译并将结果存到/aftertran-words  



本文件夹下有一个/file文件夹，其中又要包括两个文件夹，分别为/needtran-words和/aftertran-words.前者用来存放需要进行翻译的文件，后者用来存放翻译结果。  

/needtran-words需要在运行翻译代码前提前存放需要翻译的文件  
/needtran-words中文件类型可以是.txt/.tsv/.csv/.json，翻译结果在/aftertran-words中生成相对应的文件名称和文件类型。  
/needtran-words文件中的格式要求为每一行为一个list,每个list的元素为需要翻译的内容，元素类型为str。并且文件最后不要有空行。如下所示：  
    ['11 Hydroxycorticosteroids', '11-Hydroxycorticosteroids']  
    ['15 Ketosteryl Oleate Hydrolase', '15-Ketosteryl Oleate Hydrolase', 'Hydrolase, 15-Ketosteryl Oleate']  
    ['15S RNA', 'RNA, 15S']  

/needtran-words中对文件数目没有要求，可以放多个文件，运行全部文件结束后功能停止。  
将需要翻译的文件放到/file/needtran-words文件夹下之后，只需要运行translate_allwords.py即可进行翻译  
翻译结果会同步到/aftertran-words文件夹中。  
/aftertran-words文件夹下的翻译结果是与/needtran-words中文件以及文件中的内容一一对应的翻译文件。  
！！请在翻译工作结束后将自己的文件移除/file/needtran-words和/file/aftertran-words，避免下次使用的时候还会翻译这次的文件  