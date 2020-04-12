---
layout: post
title: 生成带注释的项目目录结构
date: 2020-04-12
author: 来自中世界
tags: [python, project]
comments: true
toc: true
pinned: true
---
大型项目中，各种文件目录数不胜数。如果一个人只负责一两个模块还能胜任，当需要了解的模块过多时会分不清楚每个文件的功能。特别是新人入职后需要对项目进行熟悉，更是一大挑战。此插件可用于生成项目目录，同时在文件中抓取特定规则的注释信息，生成带注释的目录树，方便对项目文件进行管理

### 插件地址

[点击下载](https://mygittime.github.io/myblog/_code/filemap.py, '点击下载')

### 参数说明

includes:需要抓取的文件夹或文件（注意：includes权重高于excludes）    
excludes:需要忽略的文件夹或文件。输入普通字符串时为精确匹配，如images，会忽略images文件夹；配合\*使用可实现模糊匹配，如.\*会忽略所有带后缀的文件，a\*b会忽略所有以a开头以b结束的文件夹或文件    
p:项目地址   
p_json:生成文件目录及名称   
format:要读取的注释格式（注意：要写成正则格式）   
BLOCK_SIZE:为防止内存占用过大，读取文件时只读取指定个数的字节

### 使用方法

打开命令窗口后运行

	python3 filemap.py

### 核心代码如下

遍历文件目录生成filemap.json

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

读取注释信息

    try:
        with open(path, 'r', encoding='utf-8') as f:
            BLOCK_SIZE = 100
            block = f.read(BLOCK_SIZE)
            result = re.search('\/\*(.*?)\*\/', block, re.S)
            if result:
                result = re.sub('\n','',result.group(1))
                return result
            else:
                return ''
    except:
        return ''

