查找词条的categories功能，需要先将工作目录移动到/zjg_wiki_ct下  
然后运行命令 python3 search_wiki.py -word 'Routes of administration' -type 1 -cat 1 -sub 1 -file 'Routes_of_administration_11.json'就可以进行Wiki的categoriy提取工作  
wikipedia词条查询  

optional arguments:  

  -h, --help  show this help message and exit  

  -word WORD  输入想要查询的词条  

  -type TYPE  输入想要查询的类型：'0'为仅输出词条pages,'1'为pages多语言描述,'2'为pages多语言加上categoties  

  -cat CAT    输入想要查询父类categories的阶数(默认为'1',表示查找一阶父类,'2'表示查询二阶父类,以此类推。'-1'表示查询所有父类)  

  -sub SUB    输入想要查询子类pages的阶数(默认为'0',表示不查找子类,'1'表示查询一阶子类的pages,以此类推。'-1'表示查询所有子类)  

  -file FILE  输入想要存储的文件名称  

运行结束后/file文件夹下面就会出现结果文件（依靠查找难度可能需要时间在4mins到更长，如果查找很复杂可能要运行很久）  
！！请在使用完成后将本次前后过滤文件移出/file文件夹，不要影响下一次使用  
结果文件的格式是这样的：[{'term':'','lang':{'en':'','zh':''},'category':['','','']},{},{}].('term'的类型为str，记录page页的标题。'lang'是一个dict,记录了本page页有的多语言信息(ISO 639-1)。'category'是一个list，无序记录了本page页的限定阶数的categories）  
[  
 {  
  "term": "Gastrointestinal tract",  
  "lang": {  
   "en": "Gastrointestinal tract",
   "ar": "قناة هضمية",
   "as": "পাচন নলী",
   "ast": "Tracto gastrointestinal",
   "be": "Страўнікава-кішачны тракт",
   "bn": "পরিপাক নালি",
   "ca": "Tub digestiu",
   "ce": "Адаман хьеран-чуьйрийн тракт",
   "cs": "Trávicí soustava",
   "es": "Tracto gastrointestinal",
   "et": "Seedekulgla",
   "eu": "Traktu gastrointestinal",
   "fa": "لوله گوارش",
   "fr": "Appareil digestif",
   "gor": "Toniya",
   "hi": "जठरांत्र क्षेत्र",
   "hif": "Gastrointestinal tract",
   "hy": "Ստամոքսաղիքային համակարգ",
   "id": "Saluran pencernaan",
   "kn": "ಜಠರಗರುಳು ವ್ಯೂಹ",
   "ko": "위장관계",
   "ks": "ہَضٕم نٲلؠ",
   "ku": "Koendama herisê ya mirovan",
   "ky": "Тамак сиңирүү системасы",
   "ml": "മനുഷ്യരിലെ പചനവ്യൂഹം",
   "ms": "Saluran gastrousus",
   "nl": "Maag-darmstelsel",
   "nn": "Meltingskanalen",
   "oc": "Sistèma digestiu",
   "pl": "Przewód pokarmowy",
   "pt": "Tubo digestivo",
   "ru": "Желудочно-кишечный тракт",
   "simple": "Alimentary canal",
   "ta": "மனித இரையகக் குடற்பாதை",
   "th": "ทางเดินอาหาร",
   "ur": "معدی امعائی حلقہ",
   "vi": "Ống tiêu hóa",
   "wuu": "消化道",
   "zh": "消化道"
  }  
 },  
 {  
  "term": "Enema",  
  "lang": {  
   "en": "Enema",
   "ar": "حقنة شرجية",
   "bg": "Клизма",
   "ca": "Ènema",
   "cs": "Klystýr",
   "da": "Lavement",
   "de": "Einlauf (Medizin)",
   "eo": "Klistero",
   "es": "Enema",
   "fa": "تنقیه",
   "fi": "Peräruiske",
   "fr": "Lavage de l\\'intestin",
   "gl": "Enema",
   "he": "חוקן",
   "id": "Enema",
   "io": "Klistero",
   "is": "Stólpípa",
   "it": "Clistere",
   "ja": "浣腸",
   "ka": "ოყნა",
   "kk": "Клизма",
   "ko": "관장",
   "ky": "Клизма",
   "ml": "എനിമ",
   "ms": "Enema",
   "nl": "Klysma",
   "pl": "Lewatywa",
   "pt": "Enema",
   "ro": "Clismă",
   "ru": "Клизма",
   "scn": "Cristeriu",
   "sk": "Klystír",
   "sr": "Klizma",
   "sv": "Lavemang",
   "te": "ఎనిమా",
   "uk": "Клізма (процедура)",
   "zh": "灌肠 (医学)"
  }  
 },  
  {  
  "total pages:": 71  
 }  
]  