# Chiayi-university-system-api

一個用來練習 flask 架 restful api 的小專案，把嘉義大學我自己常需要查看的資料包成 api，
以後有人要用也可以 call 看看。

由於開發時只有用我的帳號來測試，所以可能呼叫時會有無法預期的錯誤，可以的話告訴我，我會嘗試修正的。

放心，我不會拿來用其他東西的，我的程式碼都放在這邊了，有疑慮的可以自己看看。

## Login 登入

此功能會回傳 webpid1，類似一個 id，其他有關個人帳號的操作都需要這個參數。

另外，webpid1 有時效性，沒有測試過有多久，反正只要失效了，重新 call 這個 api 就好。

> **URL**: `https://chayi-university-system-api.herokuapp.com/login`

> **Request type**: `POST`

| Parameters | type   | description          |
|------------|--------|----------------------|
| account    | string | 你的學號             |
| password   | string | 你的校務行政系統密碼 |

> **Request schema**:
> ```json
> {
>   "account": "",
>   "password": ""
> }
> ```


> **Successful response**: 
> ```json
> {
>   "result": {
>     "webpid1": "Your webpid1"
>   }
> }
> ```

> **Failed response**:
> ```json
> {
>   "message": {
>     "result": "according to what error"
>   }
> }
> ```

## Course 取得本學期選上的所有課堂

此功能需要 webpid1 參數，會回傳這個帳號這學期選到的課程資料。

由於程式是在`網路選課作業/選課結果查詢`爬取結果的，所以那個網頁關閉時，將無法回傳資料，未來可能考慮用`網路選課作業/選課計劃書`來爬。

> **URL**: `Post https://chayi-university-system-api.herokuapp.com/course`

> **Request type**: `POST`

| Parameters | Type   | Description                  |
|------------|--------|------------------------------|
| webpid1    | string | 由上面 login 功能取得的參數     |

>**Successful response**: 
> ```json
> {
>   "result": {
>     "所有課程": [{
>       "上課教室": "地點",
>       "上課時間": [{
>         "星期": "一/二/.../日",
>         "開始": "2",
>         "結束": "4",
>       }],
>       "學分數": "3",
>       "學期數": "1",
>       "授課老師": "老師名字",
>       "校區": "xx校區",
>       "課程修別": "必修/選修",
>       "課程名稱": "課程名稱",
>       "適用年級": "1",
>       "選上人數": "87",
>       "選課修別": "必修/通識/選修",
>       "限修人數": "87"
>     }]
>   }
> }
> ```

> **Failed response**:
> ```json
> {
>   "message": {
>     "result": "according to what error"
>   }
> }
> ```

## Grade 取得帳號的所有學期的學期成績

此功能需要 webpid1 參數，會回傳這個帳號所有學期的學期成績。

> **URL**: `Post https://chayi-university-system-api.herokuapp.com/grade`

> **Request type**: `POST`

| Parameters | Type   | Description                  |
|------------|--------|------------------------------|
| webpid1    | string | 由上面 login 功能取得的參數     |

>**Successful response**: 
> ```json
> {
>   "result": {
>     "所有學期": [{
>       "GPA": 3.9,
>       "學期": "1xx 學年第 1 學期",
>       "學期平均": 87.6,
>       "實得學分": 20.0,
>       "課程": [{
>         "修別": "通識/選修/必修",
>         "學分": 2.0,
>         "學期成績": 87,
>         "課程代號": "xxxxxxxxxxx",
>         "課程名稱": "課程"
>       }]
>     }]
>   }
> }
> ```

> **Failed response**:
> ```json
> {
>   "message": {
>     "result": "according to what error"
>   }
> }
> ```

