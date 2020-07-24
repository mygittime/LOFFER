---
layout: post
title: 禁用浏览器后退按钮
date: 2020-07-24
Author: 来自中世界
tags: [javascript]
comments: true
---
点击浏览器后退按钮、window.history.back()、window.history.go()都会触发浏览器的 **onpopstate** 事件。但是部分浏览器触发有问题，如chrome浏览器点击后退按钮时无法监听到 **onpopstate** 事件，导致无法禁用后退按钮

### 解决思路

不禁用后退事件，而是在历史记录中插入一条当前页面的记录，后退完成后还是在当前页面，同时再次向历史记录中插入一条当前页面的记录。

1. 打开页面，例：`http://www.baidu.com`
2. 在历史记录中插入一条记录，url为当前页面，并在url中添加#，当前页面url变更为http://www.baidu.com#（
3. 点击返回按钮时会返回 `http://www.baidu.com`，同时执行步骤2
4. 实际需要后退时，直接后退两步即可（跳过插入的历史记录）

### 核心代码

	window.history.pushState(null, null, '#');
	window.addEventListener("popstate", ()=> { 
		window.history.pushState(null, null, '#');
	    console.log("监听到浏览器触发了后退事件")
	}, false);

	//需要后退时
	window.history.go(-2)

### [代码下载](https://mygittime.github.io/myblog/downloads/banned-brower-back.js '点击下载')



