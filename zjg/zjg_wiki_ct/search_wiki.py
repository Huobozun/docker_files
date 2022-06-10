
import argparse
import psutil
import resource
import pickle
import json
import os
path = os.getcwd()

#设置命令
parser = argparse.ArgumentParser(description='wikipedia词条查询')
parser.add_argument('-word', type=str, help='输入想要查询的词条')
parser.add_argument(
    '-type', type=int, help="输入想要查询的类型：'0'为仅输出词条pages,'1'为pages多语言描述,'2'为pages多语言加上categoties")
parser.add_argument('-cat', type=int, default=1,
                    help="输入想要查询父类categories的阶数(默认为'1',表示查找一阶父类,'2'表示查询二阶父类,以此类推。'-1'表示查询所有父类)")
parser.add_argument('-sub', type=int, default=0,
                    help="输入想要查询子类pages的阶数(默认为'0',表示不查找子类,'1'表示查询一阶子类的pages,以此类推。'-1'表示查询所有子类)")
parser.add_argument('-file', type=str, help='输入想要存储的文件名称')
args = parser.parse_args()

#设置内存使用限度，避免跑死
p = psutil.Process()
#print(p.pid)


def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))


limit_memory(1024*1024*50000)   # 限制1800M ，可申请内存，对应虚拟内存


#打开字典
file = open(path+'/categorytree-term.tsv', 'rb')
pk = file.read()
dicc = pickle.loads(pk)
file.close()

file1 = open(path+'/pagetree-term.tsv', 'rb')
pk1 = file1.read()
dicp = pickle.loads(pk1)
file1.close()

#print(1)


#递归寻找categories
def search_cat(catelist, cateword, icat, tcat):
    if(tcat != -1):
        if(icat == tcat):
            return catelist
        else:
            icat += 1
    if cateword.lower() not in dicc:
        return catelist

    if dicc[cateword.lower()]['category_term'] == []:
        return catelist

    for ip in dicc[cateword.lower()]['category_term']:
        if ip in catelist:
            continue
        catelist.append(ip)
        catelist = search_cat(catelist, ip, icat, tcat)

    return catelist
#递归寻找subcategories


def search_subcat(pagelist, sublist, subcateword, isub, tsub):
    if(tsub != -1):
        if(isub == tsub):
            return pagelist
        else:
            isub += 1
    if subcateword.lower() not in dicc:
        return pagelist
    #print(subcateword.lower(),len(dicc[subcateword.lower()]['page_term']))
    for ipageterm in dicc[subcateword.lower()]['page_term']:
        if ipageterm not in pagelist:
            pagelist.append(ipageterm)
    #print(len(pagelist),pagelist)

    for isc in dicc[subcateword.lower()]['subcategory_term']:
        if isc in sublist:
            continue
        sublist.append(isc)
        pagelist = search_subcat(pagelist, sublist, isc, isub, tsub)

    return pagelist


#初始化
page_words = []
result = []
name = args.word
page_words += dicc[name.lower()]['page_term']

isub = 0
sublist = []
#print(len(page_words),page_words)
for itemsub in dicc[name.lower()]['subcategory_term']:
    sublist.append(itemsub)
    page_words = search_subcat(page_words, sublist, itemsub, isub, args.sub)
    #print(len(page_words),page_words)

itotal = 0
for item in page_words:
    itotal += 1
    #print(item)
    x = dict()
    x['term'] = item
    if(args.type >= 1):
        x['lang'] = dicp[item.lower()]['lang']
        if(args.type == 2):
            icat = 1
            x['category'] = []
            for ic in dicp[item.lower()]['category_term']:
                x['category'].append(ic)
                x['category'] = search_cat(x['category'], ic, icat, args.cat)

    result.append(x)

result.append({'total pages:': itotal})


#写入文件
js = json.dumps(result, indent=1, ensure_ascii=False)
file = open(path+'/file/'+args.file, 'w', encoding='utf-8')
file.write(js)
file.close()

#python3 10_search_wiki.py -word 'Routes of administration' -type 1 -sub -1 -file Routes_of_administration_0-1.json
#python3 10_search_wiki.py -word 'Routes of administration' -type 2 -cat -1 -sub -1 -file Routes_of_administration_-1-1.json

#python3 10_search_wiki.py -word 'Research organizations' -type 1 -sub -1 -file Research_organizations_0-1.json

#python3 10_search_wiki.py -word 'Research organizations' -type 2 -cat 3 -sub 3 -file Research_organizations_33.json