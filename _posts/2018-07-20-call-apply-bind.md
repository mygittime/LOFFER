---
layout: post
title: call、apply和bind
date: 2020-07-24
Author: 来自中世界
tags: [javascript]
comments: true
---

### 相同点

都是用来改变this指向

### 不同点

1. 参数格式不同

	**call** 可以传任意参数

	**apply** 参数是一个数组

	**bind** 可以传任意参数

2. 是否立即执行

	**call** 和 **apply** 会立即执行
	
	**bind** 不会立即执行

### 代码

	var one = {
		name:'one',
		sayName:function(){
			console.log(this.name)
		}
	}
	var two = {
		name:'two',
		sayName:function(){
			console.log(this.name, arguments)
		}
	}

	one.sayName(); //one
	two.sayName(); //two

	two.sayName.call(one, 'n',['a','m'],'e');  //one
	two.sayName.apply(one, ['n','a','m','e']); //one
	two.sayName.bind(one, 'n')('a',['m','e']);           //one



