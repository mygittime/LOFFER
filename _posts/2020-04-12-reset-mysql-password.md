---
layout: post
title: 使用brew安装mysql并修改初始密码
date: 2020-04-12
author: 来自中世界
tags: [brew, mysql]
comments: true
toc: true
pinned: true
---
使用brew安装mysql后无法获得初始密码，此时需要设置初始密码

## 图文教程

注意我使用mysql版本是8.0.19

### 第一步 安装mysql

	brew install mysql

### 第二步 初始化mysql

运行命令

	mysql_secure_installation

期间会要求你设置密码强度，如下图：
![img](https://mygittime.github.io/myblog/images/reset-mysql-password/1.jpg)
根据你设置的密码强度进行设置密码，然后一直回车就可以了
注意：密码强度最低要求是包含八个字符，所以无法设置成123456这种简单密码，如果要设置为简单密码，请继续第三步

### 第三步 修改密码强度验证规则

启动mysql

	mysql.server start

连接mysql

	mysql -uroot -p密码

查看密码强度设置

	show variables like 'validate_password%’;

结果如下图
![img](https://mygittime.github.io/myblog/images/reset-mysql-password/2.jpg)
其中policy是当前密码强度等级，length表示密码长度

修改密码长度限制为最少6个字符

	set global validate_password.length = 6;

查看修改是否成功（我修改后policy值变了，再将policcy值改为0即可）

	set global validate_password.policy = 0;

最后再次设置密码
	
	alter user 'root'@'localhost' identified by '123456’;

### 修改完成





