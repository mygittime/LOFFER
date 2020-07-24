/*禁用浏览器返回按钮*/
/*
	1.打开页面，例：http://www.baidu.com
	2.在历史记录中插入一条记录，url为当前页面，并在url中添加#。(http://www.baidu.com#)
	3.点击返回按钮时会返回（http://www.baidu.com）
	4.返回后执行步骤2

	实际需要返回的时候跳过插入的记录即可
*/
/*
	使用方法
	import BackBtnBanned
	//监测到返回事件后执行回调函数
	var banned = new BackBtnBanned(callback);
	//确认返回时
	banned.back();
*/
export default class BackBtnBanned{
	constructor(bannedFunc){
		//实际返回
		this.back = this.back;

		this._bannedFunc = bannedFunc;

		this._pushHistory(null, '#');
		this._bindEvent();
		

	}
	_pushHistory(url, param){
		window.history.pushState(url, null, param);
	}
	_bindEvent(){
		window.addEventListener("popstate", ()=> { 
			//返回上一页后再次添加历史记录
		    this._pushHistory(null, '#');
		    //通知监测到返回事件
		    this.banneded();
		}, false);
	}
	banneded(){
		this._bannedFunc();
	}

	back(){
		window.history.go(-2);
	}

}





