#! /usr/bin/python
from pathlib import Path
import re

#include和exclude中某条规则冲突时，使用include中的规则
#输入普通字符串为完全匹配
#输入特殊字符*为模糊匹配，a*b会匹配以a开头以b结尾，*ab会匹配以ab结尾, '*a', 'a*', 'a*b', 'a.*', 'a.*b'
includes = []
excludes = ['images', '.*', 'iconfont', '*.less', '*.css', '*.html']
p = Path('/Users/pengpeng/Desktop/pla-internet/platformFront-dev/src')
p_json = './filemap.json'

#读取注释的格式
#文件夹会在该文件夹下查找._init.js文件并读取注释
#文件会根据规则提取第一行注释
#提取规则直接写python支持的正则格式-只会读取第一个符合格式的注释，所以注释要写在头部
format = '\/\*(.*?)\*\/' #js注释格式为 /*注释内容*/

#为防止内存占用过大，读取文件时只读取100个字节
BLOCK_SIZE = 100


filemap = {'name':'', 'children':[]}
def setNode(p, filemap):
    name = re.sub('.*?/', '', str(p))
    title = readAnnotation(p)
    if p.is_dir():
        if checkName(name) == True: 
            return

        node = {
            'name': name,
            'type': 0,  # 0:文件夹，1:文件
            'title': title,
            'children': []
        }
        filemap['children'].append(node)

        for pit in p.iterdir():
            subName = re.sub('.*?/', '', str(pit))
            if checkName(subName) == True:
                continue
            setNode(pit, node)
    elif p.is_file():
        if not checkName(name) == True:
            filemap['children'].append({
                'name': name,
                'title': title,
                'type': 0,  # 0:文件夹，1:文件
            })



    return filemap

#检查是否为需忽略文件
#先检查include，再检查exclude
#ture为需要忽略，false为不需要忽略
def checkName(name):
    result = False
    for item in includes:
        if re.sub(item, '', name) == '':
            return result
    for item in excludes:
        if re.sub(item, '', name) == '':
            result = True
            break

    return result


#读取注释信息
def readAnnotation(fpath):
    path = str(fpath)
    if fpath.is_dir():
        path = path + '/' + '._init.js'

    try:
        with open(path, 'r', encoding='utf-8') as f:
            block = f.read(BLOCK_SIZE)
            result = re.search(format, block, re.S)
            if result:
                result = re.sub('\n','',result.group(1))
                return result
            else:
                return ''
    except:
        return ''


#将exclude处理为python可用的正则格式
def parseEnclude(exclude):
    for index, item in enumerate(exclude):
        if not item.find('*') == -1:
            #存在特殊字符
            n = re.sub('\.', '\.', item)
            n = re.sub('\*', '(.*?)', n)

            if not n[-1] == ')':
                n = n + '$'
            else:
                n = n[:-2] + n[-1]
            if not n[0] == '(':
                n = '^' + n

            exclude[index] = n

    return exclude

def createJson(content):
    result = re.sub('\'', '"', content)
    try:
        with open(p_json, 'w', encoding='utf-8') as f:
            f.write(result)
            print('successfully')
    except:
        print('error')


def main():
    global excludes, includes

    excludes = parseEnclude(excludes)
    includes = parseEnclude(includes)
    result = str(setNode(p, filemap))
    createJson(result)

if __name__ == "__main__":
    main()

