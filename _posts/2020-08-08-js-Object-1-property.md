---
layout: post
title: 理解对象-属性
date: 2020-07-24
Author: 来自中世界
tags: [javascript Object]
comments: true
---

### 属性类型

1.数据属性

在 **Object** 中，每个属性值都有四个属性,设置属性时使用Object.defineProperty。这个方法接收三个参数：属性所在对象、属性的名字、一个描述符对象（要修改的内容，同时可以修改属性的值）

1. [[Configurable]]:是否可以用delete删除该属性，默认为true
2. [[Enumerable]]:是否可以通过for-in、Object.keys、Object.values来遍历该属性，默认为true
3. [[Writable]]:是否可以修改该属性，默认为true
4. [[Value]]:这个属性的值，默认为undefined

**注意：** 使用defineProperty创建的属性，三个属性值默认都是false

#### 代码

    var person1 = {
        name:"person1"
    }
    console.log(person1.name) //person1

    //禁止修改
    var person2 = {
        name:'person2'
    }
    Object.defineProperty(person2, 'name', {
        writable:false
    })
    person2.name = "noName"
    console.log(person2.name) //person2

    //禁止删除
    var person3 = {}
    Object.defineProperty(person3, 'name', {
        configurable:false,
        value:"person3"
    })
    delete person3.name
    console.log(person3.name) //person3

    //禁止遍历
    var person4 = {
        name:'person4'
    }
    for(var key in person4){
        console.log(key) //name
    }
    Object.defineProperty(person4, 'name', {
        enumerable:false
    })
    for(var key in person4){
        console.log(key) //""
    }

    //默认是false
    var person_false(){};
    Object.defineProperty(person_false, 'name', {
        value:"小明"
    })
    console.log(person_false.configurable) // false
    console.log(person_false.writable) // false
    console.log(person_false.enumerable) // false
    console.log(person_false.value) // 小明
    

2.访问器属性

访问器有四个属性

1. [[Configurable]]:是否可以用delete删除该属性，默认为true
2. [[Enumerable]]:是否可以通过for-in、Object.keys、Object.values来遍历该属性，默认为true
3. [[Get]]:在读取属性时调用的函数，默认值时undefined
4. [[Set]]:在写入属性时调用的函数，默认值时undefined

**注意：** 定义访问器需要使用Object.defineProperty。且访问器无法通过Object.name获取该属性的值

#### 代码

    var person5 = {
        _year:2004,
        age:20
    }
    Object.defineProperty(person5, 'year', {
        get:function(){
            return this._year;
        },
        set:function(year){
            this.age += year - this._year;
            this._year = year;
        }
    })
    Object.defineProperty(person5, 'job', {
        get:function(){
            return this.job;
        },
        set:function(job){
            this.job = job;
        }
    })
    person5.job = 'teacher'; //error
    console.log(person5.job); // error

3.可以使用Object.defineProperties同时设置多个属性

    var person6 = {
        name:"xiaoming"
    };
    Object.defineProperties(person6, {
        //数据
        age:{
            configurable:true,
            value:20
        },
        year:{
            configurable:false,
            value:2004
        },
        //访问器
        _year:{
            set:function(year){
                this.age = year - this.year;
                this.year = year;
            },
            get:function(){
                return this.year
            }
        }
    })

3.读取属性

可以使用Object.getOwnPropertyDescriptor来读取数据属性和访问器属性

#### 代码

    let name = Object.getOwnPropertyDescriptor(person6, 'name');
    let age = Object.getOwnPropertyDescriptor(person6, 'age');
    let year = Object.getOwnPropertyDescriptor(person6, '_year');

    console.log(name.configurable) // true
    console.log(name.writable) // true
    console.log(name.enumerable) // true
    console.log(name.value) // 2004
    console.log(name.get) // undefined

    console.log(age.configurable) // true
    console.log(age.writable) // false
    console.log(age.enumerable) // false
    console.log(age.value) // 20
    console.log(age.get) // undefined

    console.log(_year.configurable) // false
    console.log(_year.enumerable) // false
    console.log(_year.get) // function

    
