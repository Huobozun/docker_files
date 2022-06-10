import os
import json
import numpy as np
import shutil

import string

import ahocorasick

path = os.getcwd()


def getword(path2):
    with open(path2, 'r', encoding='utf-8') as f:
        data = []
        title = []
        for line in f:
            # 读取一行后，末尾一般会有一个\n，所以用strip函数去掉
            line = line.strip('\n').split('\t')
            #print(line[0])
            #print(line[1])
            #print(line[2])
            #break
            data.append(line[1])
            title.append(line[0])
        #print(data[0])#此时data中的每个元素就是每行的第二列
        #抽出每行的单词
        data1 = []  # 将每行单词都排起来
        data2 = []  # type
        data3 = []  # 出处
        for i in range(0, len(data)):
            line0 = data[i]
            data1.append([])
            data2.append([])
            data3.append([])
            word = ''
            j = 0
            b = 1
            while(j < len(line0)):
                if(b == 1 and line0[j] == '#' and line0[j+1] == '#' and line0[j+2] == '#'):
                    data1[i].append(word)
                    j += 3
                    b = 2
                    word = ''
                    continue
                if(b == 2 and line0[j] == '#' and line0[j+1] == '#' and line0[j+2] == '#'):
                    data2[i].append(word)
                    j += 3
                    b = 3
                    word = ''
                    continue
                if(b == 3 and line0[j] == ' ' and line0[j+1] == '[' and line0[j+2] == 'S' and line0[j+3] == 'E' and line0[j+4] == 'P' and line0[j+5] == ']' and line0[j+6] == ' '):
                    data3[i].append(word)
                    j += 7
                    b = 1
                    word = ''
                    continue
                if(b == 3 and j == len(line0)-1):
                    word += line0[j]
                    data3[i].append(word)
                    j = len(line0)
                    b = 1
                    word = ''
                    continue
                else:
                    word += line0[j]
                    j += 1
    f.close()
    # title是每行的title的list,对应的，data1是每行的英文单词的集合的list,data2是term type，data3是出处
    return title, data1, data2, data3
def build_words(path11,Filelist):
    for i0 in range(0, len(Filelist)):
        ftitle, fw, ft, fr = getword(path11+'/file/before/'+Filelist[i0])  # list里类型为str

        with open(path+'/resultfile/words-word/'+Filelist[i0], 'w', encoding='utf-8', newline='')as fa:
            for i1 in range(0, len(fw)):
                fa.write('%s\t%s\n' % (ftitle[i1], fw[i1]))
        fa.close()

        with open(path+'/resultfile/words-type/'+Filelist[i0], 'w', encoding='utf-8', newline='')as fb:
            for i2 in range(0, len(ft)):
                fb.write('%s\t%s\n' % (ftitle[i2], ft[i2]))
        fb.close()

        with open(path+'/resultfile/words-resouce/'+Filelist[i0], 'w', encoding='utf-8', newline='')as fc:
            for i3 in range(0, len(fr)):
                fc.write('%s\t%s\n' % (ftitle[i3], fr[i3]))
        fc.close()



def get_title(name, file):
    with open(path+'/'+name+file, 'r', encoding='utf-8')as ft0:
        dataci = []
        for line in ft0:
            dataci.append(line)
        ft0.close()
        z = []
        for ii in range(0, len(dataci)):
            xt = dataci[ii]
            y = ''
            for it in range(0, 8):
                y += xt[it]
            z.append(y)
    return z


def get_content(name, file):
    with open(path+'/'+name+file, 'r', encoding='utf-8')as ft00:
        dataci = []
        for line in ft00:
            dataci.append(line)
        ft00.close()
        z = []
        for ii in range(0, len(dataci)):
            xc = dataci[ii]
            yc = ''
            for ic in range(9, len(xc)):
                yc += xc[ic]
            z.append(eval(yc))
    return z


class filter_en():

    def __init__(self) -> None:
        file3 = open(path+'/UMLS_library.txt', 'r', encoding='utf-8')  # 统计词的个数
        js3 = file3.read()
        dic3 = json.loads(js3)
        #print(dic[0])
        file3.close()
        self.UMLSlibrary = dic3
        file4 = open(path+'/UMLS_fre_dictionary.txt',
                     'r', encoding='utf-8')  # 统计词频
        js4 = file4.read()
        dic4 = json.loads(js4)
        #print(dic[0])
        file4.close()
        self.UMLSdictionary = dic4

    def googlefre(self, word):  # 判断想要删掉的词是否在Google词频中出现频率很高
        with open(path+'/frequency-all.txt', 'r', encoding='utf-8', errors='ignore')as fr0:
            ig = 0
            for lines in fr0:
                ig += 1
                num = ''
                for ig1 in range(0, len(lines)):
                    num += lines[ig1]
                    if(lines[ig1+1] == ' '):
                        break
                w = ''
                for ig2 in range(11, len(lines)):
                    w += lines[ig2]
                    if(lines[ig2+1] == ' '):
                        break
                if(w == word):
                    #print(num)
                    break
                if(ig > 50000):
                    break
            rnum = int(num)
        fr0.close()
        if(rnum < 50000):
            return True
        else:
            return False

    def pubfre2(self, wordlist, word, l):  # 判断想要删掉的词的词频是否显著大于本词条的其他词
        #print(word)
        if word not in self.UMLSdictionary:
            return False
        else:
            xpn = self.UMLSdictionary[word]
        ic = 0
        if(int(xpn) < 10):  # 词本身词频小于10，不删，影响不大
            ic = 0
            return False
        px = 0
        py = 0
        for ii0 in range(0, len(wordlist)):
            if(wordlist[ii0] != word and l[ii0] != 1):  # 仅查找不同词以及尚未删掉词的频率差距
                if wordlist[ii0] not in self.UMLSdictionary:  # 词典没有
                    ypn = 0
                else:
                    ypn = self.UMLSdictionary[wordlist[ii0]]
                if(int(xpn) < int(ypn)):  # 只比较比该词频率小的词，频率比该词大的词等到判断他自己的时候才有用
                    continue
                py += 1  # 统计除去相同词和已删掉的词之外，频率比该词小的词的个数
                if(int(xpn) <= 125):
                    if(int(xpn)-int(ypn) > 100):
                        px += 1  # 统计差距很大的词的个数
                else:
                    if(int(xpn)/(int(ypn)+1) > 5):  # 如果有词频比x的五分之一大，就说明x的词频不是显著高于其他词，就不删。加1是避免0不能当被除数
                        px += 1  # 统计差距很大的词的个数
        if(px == py and py != 0):  # 所有比该词频率小的词的频率差距都很大
            ic = 1
        if(ic == 1):  # ic=1说明本次比其他所有词频都大于5倍以上,要删
            return True
        else:
            return False

    def dict_normalword(self, word):  # 构建可缺失字典
        worddict = ['s', 'es', 'd', 'ed', 'ing', 'a', 'an', 'of', 'the', 'ting', 'syndrome', 'adult', 'childhood', 'location', 'region', 'structure', 'Antigen',
                    'Antigens', 'Lymphocyte', 'Lymphocytes', '[EPC]', '[EPC', 'EPC', '[TC]', '[TC', 'TC', '[APC]', '[APC', 'APC', '[brand name]', '[brand name', 'brand name']
        for s in worddict:
            if(s.lower() == word.lower()):
                return True

        return False

    # 用来获取如果testword在goodword内部时的前后符号，判断是否含有'/''>''()'，以便于关系判断
    def get_Punctuation(self, testword, goodword):
        A = ahocorasick.Automaton()
        testword2 = []
        testword2.append(testword)

        for index, word in enumerate(testword2):
            A.add_word(word, (index, word))

        A.make_automaton()

        pp = []

        #每个文件读取查找
        for item in A.iter(goodword):
            p = []
            y0 = item[0]  # 比对查找结果
            ih = y0+1
            while(ih < len(goodword) and goodword[ih] == ' '):
                ih += 1
            if(ih < len(goodword)):
                p.append(goodword[ih])
            else:
                p.append(goodword[len(goodword)-1])

            iq = y0-len(testword)
            while(iq > -1 and goodword[iq] == ' '):
                iq -= 1
            if(iq > -1):
                p.append(goodword[iq])
            else:
                p.append(goodword[0])

            pp.append(p)

        return pp

    # 判断本词与其他词有没有或，上下级，别称的关系。这类词通常是不用删的

    def judge_relationship(self, testword, wordlist):
        for i0 in range(0, len(wordlist)):
            if(testword.lower() in wordlist[i0].lower()):  # testword短

                p0 = wordlist[i0].lower().replace(
                    testword.lower(), '')  # 获取剩余部分
                if(len(p0) >= 1):
                    while(p0[len(p0)-1] == ' ' or p0[0] == ' '):
                        p0 = p0.strip(' ')
                p = p0.strip(string.punctuation)  # 获取去除边缘标点符号的剩余部分

                # 不是专有名词，再去判断是不是别称关系(避免这种情况'HER-2/neu Peptide Vaccine')
                if self.is_unique(testword) == False:
                    #['red clover']	['clover red', 'red clover', 'Trifolium pratense / red clover / meadow honeysuckle', 'Trifolium pratense, flower essence']
                    pp = self.get_Punctuation(
                        testword.lower(), wordlist[i0].lower())
                    for ip in range(0, len(pp)):
                        if(pp[ip][0] == r'/' or pp[ip][1] == r'/'):  # 前后有/
                            return True
                #上面为testword在goodword内部，下面为testword在goodword边上
                    if(p0.replace(p, '') == r'/'):  # 缺失部分旁边有个'/'说明是别称关系，不删
                        return True
                pp = self.get_Punctuation(
                    testword.lower(), wordlist[i0].lower())
                for ip in range(0, len(pp)):
                    if(pp[ip][0] == r'>' or pp[ip][1] == r'>'):  # 前后有>
                        return True
                    if(pp[ip][0] == r'(' and pp[ip][1] == r')'):  # 要求testword被括号包住
                        return True
                if(p0.replace(p, '') == r'>'):  # 缺失部分旁边有个'>'说明是从属关系，不删
                    return True
                if(p0.replace(p, '') == r'()'):  # 缺失部分旁边有个'）'说明是别称关系，不删
                    return True
        return False

    def lack_mainfeature(self, testword, goodword, wordlist, wordres):  # 判断是否缺少主要部分
        if(testword.lower() in goodword.lower()):  # testword短

            p0 = goodword.lower().replace(testword.lower(), '')
            if(len(p0) >= 1):
                while(p0[len(p0)-1] == ' ' or p0[0] == ' '):
                    p0 = p0.strip(' ')
            #p=p.replace(' ','')
            p = p0.strip(string.punctuation)
            xp = p.split(' ')

            mwordlist = []
            for i4 in range(0, len(wordlist)):  # 汇总MTH/MSH词，将与该词一样的词也增加权重
                if(wordres[i4] == 'MTH' or wordres[i4] == 'MSH'):
                    mwordlist.append(wordlist[i4].lower())

            end = 0
            for item in xp:  # 判断缺少部分每个词是不是词条的关键部分，如果其中任何一个词是关键部分，那缺少都是不合理的
                if(item in testword.lower()):  # 缺失部分在前面的词里面，就不删
                    continue
                if(len(item) == 1):  # 缺失部分就是一个字母，没有意义去查这个字母是否重要
                    continue
                if self.dict_normalword(item):  # 缺少部分在可缺少字典里面，就不删
                    continue

                pan = 0
                for i3 in range(0, len(wordlist)):
                    if(item.lower() in wordlist[i3].lower()):  # 判断缺少的词的出现次数
                        if(len(wordlist) > 3):  # 3个词以上的词条增加MTH/MSH权重，不然三个词只要缺失MTH/MSH部分必然被删，不合理
                            # MTH/MSH词增加权重
                            if(wordres[i3] == 'MTH' or wordres[i3] == 'MSH' or (wordlist[i3].lower() in mwordlist)):
                                pan += 0.5
                        pan += 1
                if(pan >= len(wordlist)*0.6):  # 缺少部分是主要成分，要删
                    end = 1
                    break

            if(end == 1):
                return True
            else:
                return False
        else:
            return False

    def is_unique(self, word):  # 判断像不像是特有名词
        if len(word.split(' ')) == 1:  # 长度为一个词
            if word[0].isupper() or any(chr0.isupper() for chr0 in str(word)):  # 首字母大写/中间有大写
                return True
            if any(chr.isdigit() for chr in str(word)):  # 包含数字
                return True

            return False
        else:
            if word.isupper():  # 长度大于一个词，但全是大写
                return True

            else:
                return False

    def search_others(self, word, wordlist):  # 判断其他地方是否也出现这个词
        scount = 0
        for iword in wordlist:
            if(word == iword):
                scount += 1
        if(self.UMLSlibrary[word] > scount):  # 统计词典里面的数目大于本词条，说明该词在其他地方也出现过
            return True
        else:
            return False

    def is_abbreviation(self, word, wordlist):  # 判断专有名词是不是完整对应的缩写，如是不删
        for i0 in range(0, len(wordlist)):
            y = wordlist[i0].split(' ')
            z = ''
            for i1 in range(0, len(y)):
                z += y[i1][0]
            if(word.lower() == z.lower()):
                return True

        return False

    def compare_words(self, word1, word2):  # 判断两个词是否相关（是否有重叠部分）
        count = 0
        for iw1 in word1:
            for iw2 in word2:
                if(iw1.lower() == iw2.lower()):
                    count += 1

        if(count == 0):
            return False  # 两词毫不相关
        else:
            return True  # 两词有关系

    def _filter_en_(self, word, wtype, resouce):
        l=[]
        for ill in range(0,len(word)):
            l.append(0)
        index_pn = None
        for itype in range(0, len(wtype)):
            if(wtype[itype] == 'PN'):
                index_pn = itype
        for i1 in range(0, len(word)):
            # PN词不删
            if(index_pn != None and (i1 == index_pn or word[i1].lower() == word[index_pn].lower())):
                continue
            if self.is_unique(word[i1]):  # 像是特有名词
                # 其他地方没有该词汇，该词具有独特性，不删
                if self.search_others(word[i1], word) == False:
                    continue
                if self.is_abbreviation(word[i1], word):  # 是与词条完整对应的缩写，不删
                    continue

            # 与本词条中的其他词是‘或’‘别称’‘从属’关系，不删（['Iris douglasiana / iris', 'Iris douglasiana, flower essence', 'iris flower essence', 'iris']）
            if self.judge_relationship(word[i1], word):
                continue

            # 存在PN词汇，以PN词汇作为基准;并且想要判断的词与PN有关系时
            if(index_pn != None and (word[i1].lower() in word[index_pn].lower())):
                # 缺少主要成分
                if self.lack_mainfeature(word[i1], word[index_pn], word, resouce):
                    #if self.search_others(word[i1],word):#如果其他地方存在该词，进行下一步判断；其他地方没有该词，可以不删
                    if(len(word[i1].split(' ')) == 1):
                        # 判断想要删掉的词的Google词频，如果词频排位比较靠前，说明经常出现，说明不是专有名词，确实要删
                        if self.googlefre(word[i1]):
                            l[i1] = 1
                        # 判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                        if self.pubfre2(word, word[i1], l):
                            l[i1] = 1
                    else:
                        # 判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                        if self.pubfre2(word, word[i1], l):
                            l[i1] = 1
            else:
                # 存在PN，但是与PN毫不相关的，一般是正确的。
                if(index_pn != None and self.compare_words(word[i1], word[index_pn]) == False):
                    continue
                else:  # 没有PN词汇，或者有PN词但是与需要判断的词的关系不明朗，对整个词条逐个比较

                    for i2 in range(0, len(word)):
                        # 缺少/多余主要成分
                        if self.lack_mainfeature(word[i1], word[i2], word, resouce):
                            #if self.search_others(word[i1],word):#如果其他地方存在该词，进行下一步判断；其他地方没有该词，可以不删
                            if(len(word[i1].split(' ')) == 1):
                                # 判断想要删掉的词的Google词频，如果词频排位比较靠前，说明经常出现，说明不是专有名词，确实要删
                                if self.googlefre(word[i1]):
                                    l[i1] = 1
                                    break
                                # 判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                                if self.pubfre2(word, word[i1], l):
                                    l[i1] = 1
                                    break
                            else:
                                # 判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                                if self.pubfre2(word, word[i1], l):
                                    l[i1] = 1
                                    break

        return l




if __name__ == "__main__":



    Filelist = os.listdir(path+'/file/before')
    if os.path.exists(path+'/resultfile')==True:
        shutil.rmtree(path+'/resultfile',True)
        os.makedirs(path+'/resultfile')
        os.makedirs(path+'/resultfile/words-word')
        os.makedirs(path+'/resultfile/words-type')
        os.makedirs(path+'/resultfile/words-resouce')
    else:
        os.makedirs(path+'/resultfile')
        os.makedirs(path+'/resultfile/words-word')
        os.makedirs(path+'/resultfile/words-type')
        os.makedirs(path+'/resultfile/words-resouce')

    build_words(path,Filelist)



    path1 = path+'/resultfile/words-word/'
    Filelist = os.listdir(path1)
    
    x_filter = filter_en()
   
    for i in range(0, len(Filelist)):
        ftitle = get_title('resultfile/words-type/', Filelist[i])  # list里类型为str
        fw = get_content('resultfile/words-word/', Filelist[i])  # list里类型为list
        ft = get_content('resultfile/words-type/', Filelist[i])  # list里类型为list
        fr = get_content('resultfile/words-resouce/', Filelist[i])  # list里类型为list
        if os.path.exists(path+'/resultfile/filter_result_marker')==False:
            os.makedirs(path+'/resultfile/filter_result_marker')
        with open(path+'/resultfile/filter_result_marker/'+Filelist[i], 'w', encoding='utf8', newline='')as ff:
            for if0 in range(0, len(fw)):
                fw1 = fw[if0]
                ft1 = ft[if0]
                fr1 = fr[if0]
                x = x_filter._filter_en_(fw1, ft1, fr1)
                ff.write('%s\t%s\n' % (ftitle[if0], x))

        ff.close()
    

    total = 0
    totaly = 0
    with open(path+'/file/result/allshow_filteren.tsv', 'w', encoding='utf-8', newline='')as fa:
        for i in range(0, len(Filelist)):
            x = 0
            y = 0
            fa.write('%s\n' % (Filelist[i]))
            ftitle = get_title('resultfile/words-type/', Filelist[i])  # list里类型为str
            ft = get_content('resultfile/words-type/', Filelist[i])  # list里类型为list
            fr = get_content('resultfile/words-resouce/', Filelist[i])  # list里类型为list
            fw = get_content('resultfile/words-word/', Filelist[i])  # list里类型为list
            fl = get_content('resultfile/filter_result_marker/',
                             Filelist[i])  # list里类型为list

            for ii in range(0, len(ft)):
                sh = []
                ft1 = ft[ii]
                fr1 = fr[ii]
                fw1 = fw[ii]
                fl1 = fl[ii]
                la = 0
                for iii in range(0, len(fl1)):
                    y += 1
                    totaly += 1
                    if(fl1[iii] == 1):
                        la = 1
                        sh.append(fw1[iii])
                        x += 1
                        total += 1
                if(la == 1):
                    shd = fw1
                    fa.write('%s\t%s\t%s\n' % (ftitle[ii], sh, shd))

            print(Filelist[i], x, y)
            fa.write('%s\t%s\t%s\n' % (Filelist[i], x, y))

        print('total: ', total, totaly)
        fa.write('%s\t%s\n' % (total, totaly))
    fa.close()



    for i0 in range(0, len(Filelist)):
        ftitle = get_title('resultfile/words-type/', Filelist[i0])  # list里类型为str
        fw = get_content('resultfile/words-word/', Filelist[i0])  # list里类型为list
        ft = get_content('resultfile/words-type/', Filelist[i0])  # list里类型为list
        fr = get_content('resultfile/words-resouce/', Filelist[i0])  # list里类型为list
        fm = get_content('resultfile/filter_result_marker/', Filelist[i0].replace('zh-', ''))#list里类型为list
        with open(path+'/file/result/Filtered_'+Filelist[i0], 'w', encoding='utf-8', newline='')as ff:
            x = 0
            for ii in range(0, len(fm)):
                fw1 = fw[ii]
                ft1 = ft[ii]
                fr1 = fr[ii]
                fm1 = fm[ii]
                ib = 0
                fword = ''
                for iii in range(0, len(fm1)):
                    if ib == 1 and fm1[iii] ==0:
                        fword += ' [SEP] '
                    if fm1[iii] == 0:
                        ib = 1
                        fword += fw1[iii]+'###'+ft1[iii]+'###'+fr1[iii]
                    else:
                        x += 1
                ff.write('%s\t%s\n' % (ftitle[ii], fword))
        ff.close()

    
