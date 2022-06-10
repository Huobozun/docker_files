
#本文件是写了一个streamlit的demo，可以展示Wikipedia的词典
#运行指令streamlit run show_streamlit_nm.py，然后可以浏览器打开
#读入文件：categorytree-nm-pickle.tsv
#写出文件：
import streamlit as st
import pickle
import os
path = os.getcwd()


st.title('Search in Wikipedia')


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def read_in_frequency_dictionary():
    st.write('Wikipedia is loading ...')
    file = open(path+'/categorytree-nm-pickle.tsv', 'rb')
    js = file.read()
    dic0 = pickle.loads(js)  # dic2为字典
    file.close()
    st.write('Wikipedia is ready!')

    return dic0


url = st.text_input('The word/words category you want to search in Wikipedia:')

a = st.button('SEARCH!')



dic = read_in_frequency_dictionary()


p = 0

if a:
    if (url != ''):
        x = str(url).lower()
        if x not in dic:
            p = -1
        else:
            p = 1
            y_lang = dic[x]['lang']
            if('hidden_parent_nm' in dic[x]):
                y_hidden_parent_nm = dic[x]['hidden_parent_nm']
            else:
                y_hidden_parent_nm = []
            y_parent_nm = dic[x]['parent_nm']
            y_sub_nm = dic[x]['sub_nm']
            y_pages = dic[x]['pages_nm']





if(p == -1):
    st.write('"%s" is not in Wikipedia' % (url))
if(p == 1):
    st.write('lang: %s\n' % (y_lang))
    st.write('hidden_category: %s\n' % (y_hidden_parent_nm))
    st.write('category: %s\n' % (y_parent_nm))
    st.write('subcategory: %s' % (y_sub_nm))
    st.write('pages: %s' % (y_pages))
