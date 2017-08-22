#coding:utf-8
"""命令行翻译工具
    -作者:想飞的男孩
    -duanyph@qq.com
    -2011.8.17
Usage:
    fanyi.py [-A|-Z|-J|-E|-K|-F|-R|-P|-C] (-a|-z|-j|-e|-k|-f|-r|-p|-c) <wb>

Options:
    -h           帮助
    -A,-a        自动
    -Z,-z        汉语
    -J,-j        日语
    -E,-e        英语
    -K,-k        韩语
    -F,-f        法语
    -R,-r        俄语
    -P,-p        葡萄牙语
    -C,-c        西班牙语

Example:
    fanyi.py [源语言(可选参数)] (目标语言(必选参数))  被翻译的文本(必选参数)
    fanyi.py -Z -e 被翻译的文本(如果可选参数没有填则相应的参数设为自动识别，即auto)
"""
import hashlib
import random
import re
import json
from urllib.parse import *
from urllib import request
from docopt import docopt
#相关参数处理
yyys={"-A":"auto","-Z":"zh-CHS","-J":"ja","-E":"EN","-K":"ko","-F":"fr","-R":"ru","-P":"pt","-C":"es","-a":"auto","-z":"zh-CHS","-j":"ja","-e":"EN","-k":"ko","-f":"fr","-r":"ru","-p":"pt","-c":"es"}
yy=docopt(__doc__)
wb=yy["<wb>"]
yyy=None
for a,b in yy.items():
    if b==True:
        if re.search(r"[A-Z]",a)!=None:
            yyy=yyys[a]
        if re.search(r"[a-z]",a)!=None:
            mbyy=yyys[a]
if yyy==None:
    yyy="auto"
sjs=str(random.randint(0,9))
#计算签名
qmxx="7f2989a0eadf2e5f"+wb+sjs+"62gvXFNxqwwocxoG2RXmoWRgJAszeWx4"
qm=hashlib.md5(qmxx.encode("utf-8")).hexdigest()
#构建提交接口，获取返回的json数据
jk=quote("http://openapi.youdao.com/api?q="+wb+"&from="+yyy+"&to="+mbyy+"&appKey=7f2989a0eadf2e5f&salt="+sjs+"&sign="+qm,'\/:?=;@&+$,%.#')
tj=request.urlopen(jk)
sj=tj.read().decode("utf-8")
sj=json.loads(sj)
#解析返回的数据
if sj["errorCode"]=="101":
    print("错误，可能缺少必填的参数！")
elif sj["errorCode"]=="102":
    print("错误，不支持的语言类型！")
elif sj["errorCode"]=="103":
    print("错误，翻译文本过长！")
elif sj["errorCode"]=="301":
    print("错误，辞典查询失败！")
elif sj["errorCode"]=="302":
    print("错误，翻译查询失败！")
elif sj["errorCode"]=="303":
    print("错误，服务端异常！")
elif sj["errorCode"]=="0":
    print( sj["translation"][0])
    if "basic" in sj.keys():
        print("其它翻译：")
        for a in sj["basic"]["explains"]:
            print(a)
else:
    print("出现错误，需要帮助请联系作者！错误码："+sj["errorCode"])
