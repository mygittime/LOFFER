---
layout: post
title: react项目换肤功能
date: 2020-04-27
Author: 来自中世界
tags: [react]
comments: true
---
本章内容为在react项目中实现实时换肤功能

### 项目背景

公司的项目是基于react和less进行开发的，项目分成了几个大的模块。其中有一个模块是深色系，其他模块都是浅色系。开发深色系模块时考虑到以后可能会添加换肤功能，就暂时敲定了一个方案。方案如下：

### 初期方案

创建 **light.less** 和 **dark.less** 文件，分别用来存储浅色系和深色系所有颜色，less文件中使用less自带变量模式定义变量（@color_text:#fff）。每个less文件首先引入 **light.less** 或 **dark.less** 文件，然后使用其中定义的颜色进行开发。打包项目时打包出两套样式文件，切换皮肤时动态加载对应的样式文件。事实证明，问题多多

1. 浅色系和深色系公共模块无法共用，只能复制一份
2. 模块色系不同时，不容易管理
3. 打包时步骤过于繁琐，维护成本较高

### 最终方案

由于疫情原因，最近比较清闲，所以又研究了一遍换肤功能。功夫不负有心人，终于找到了更好的解决方案。方案为使用[css3 var()函数](https://www.runoob.com/cssref/func-var.html)，兼容性如下

![兼容](https://mygittime.github.io/myblog/images/react-skin/1.png)

方案如下：

在静态文件中创建 **light.css** 和 **dark.css** 文件用于放置各个色系的颜色，如果增加色系就新增一个css文件，每个css文件中的变量名称和数量必须保持一致。

变量命名规则：必须以 -- 开头。更多规则网上有很多，这里就不讲了

light.css中代码

    :root{
        --text-1:#fff;
        --text-2:#000;
        --text-3:#f00;
    }
    
dark.css中代码

    :root{
        --text-1:#a3abb0;
        --text-2:#a6a6a6;
        --text-3:#e9c893;
    }

写一个公共方法 loadSkin.js，用来加载对应的皮肤文件

    const normalSkin = "light";
    //加载皮肤
    window.loadSkin = (color) => {
        let link = document.createElement('link');
        link.type = "text/css";
        link.rel = "styleSheet";
        link.id = "wbst-skin";
        link.href = `/static/color_theme/${color}.css`;
        document.head.appendChild(link)

        link.onerror = ()=>{
            if(color != normalSkin){
                console.error(`加载皮肤-${color}失败，加载默认皮肤-${normalSkin}`);
                window.loadSkin(normalSkin);
            }else{
                console.error(`加载默认皮肤-${normalSkin}失败`);
            }
        }
    }

    //切换皮肤
    window.choiceSkin = (color) => {
        document.querySelector('#wbst-skin') && document.querySelector('#wbst-skin').remove();

        window.loadSkin(color);
    }

    //默认加载皮肤
    ((color)=>{
        window.loadSkin(color);
    })(window.localStorage.skinType || normalSkin)

**注意**：link标签一定要定义rel属性，否则less文件中无法获取到变量

当然，你也不必每次都生成新的link标签，但是这样无法监听加载文件是否成功

    window.loadSkin = (color) => {
        let link = document.quertSelector("#wbst-skin");
        if(!link){
            link = document.createElement('link');
            link.type = "text/css";
            link.rel = "styleSheet";
            link.id = "wbst-skin";
            link.href = `/static/color_theme/${color}.css`;
            document.head.appendChild(link)
        }else{
            link.setAttribute("href", `/static/color_theme/${color}.css`);
        }
    }

在入口文件中引入 **loadSkin.js**

    import "/loadSkin.js";

在less文件中使用自定义颜色

    body{
        p{
            color:var(--text-1);
        }
    }

更换皮肤时，加载对应皮肤即可

    window.choiceSkin("dark");

### 总结

初期方案中的三个问题都得到了解决。面向百度和面向谷歌开发时也要时常加入自己的思考，这样方能找到最适合自己的方案。