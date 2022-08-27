# Chiayi-university-system-api

一個用來練習 flask 架 restful api 的小專案，把嘉義大學我自己常需要查看的資料包成 api，
以後有人要用也可以 call 看看。

由於開發時只有用我的帳號來測試，所以可能呼叫時會有無法預期的錯誤，可以的話告訴我，我會嘗試修正的。

放心，我不會拿來用其他東西的，我的程式碼都放在這邊了，有疑慮的可以自己看看。

## Login 登入

此功能會回傳 webpid1，類似一個 id，其他有關個人帳號的操作都需要這個參數。

另外，webpid1 有時效性，沒有測試過有多久，反正只要失效了，重新 call 這個 api 就好。

> **URL**: `https://ncyu-courseapi.azurewebsites.net/login`

> **Request type**: `POST`

| Parameters | type   | description          |Required|
|------------|--------|----------------------|--------|
| account    | string | 你的學號              |Required|
| password   | string | 你的校務行政系統密碼    |Required|

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
>     "result": "error message"
>   }
> }
> ```

## Personal Course 取得個人本學期選上的所有課堂

此功能需要 webpid1 參數，會回傳這個帳號這學期選到的課程資料。

目前是使用`當學期選課查詢`來爬取，不確定是否穩定。

> **URL**: `https://ncyu-courseapi.azurewebsites.net/course`

> **Request type**: `POST`

> **Request schema**:
> ```json
> {
>   "webpid1": ""
> }
> 

| Parameters | Type   | Description                  | Required|
|------------|--------|------------------------------|---------|
| webpid1    | string | 由上面 login 功能取得的參數     |Required|

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
>     "result": "error message"
>   }
> }
> ```

## Grade 取得帳號的所有學期的學期成績

此功能需要 webpid1 參數，會回傳這個帳號所有學期的學期成績。

> **URL**: `https://ncyu-courseapi.azurewebsites.net/grade`

> **Request type**: `POST`

> **Request schema**:
> ```json
> {
>   "webpid1": ""
> }
> 

| Parameters | Type   | Description                  |Required|
|------------|--------|------------------------------|--------|
| webpid1    | string | 由上面 login 功能取得的參數     |Required|

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
>     "result": "error message"
>   }
> }
> ```

## Course Selection 取得符合條件的選課

查詢選課學期符合條件的課程，若沒有附上任何參數，則回傳所有課程，若沒有符合條件的結果，則回傳空的結果。

> **URL**: `https://ncyu-courseapi.azurewebsites.net/course_selection`

> **Request type**: `GET`


| Parameters | Type   | Description                  |Required|
|------------|--------|------------------------------|--------|
| 校區        | string | 選項有 `蘭潭校區`、`民雄校區`、`新民校區`、`林森校區`。 |Optional|
|上課系所|string|就是上課的系所，一般是系名縮寫，例如`資工系`、`景觀系`、`應數系`等。|Optional|
|適用年級|string|限定上課的年級，選項有 `1`、`2`、`3`、`4`、`5`。|Optional|
|課程修別|string|選項有`選修`和`必修`|Optional|
|上課學院|string|選項有`師範學院`、`人文藝術學院`、`管理學院`、`理工學院`、`農學院`、`生命科學院`、`獸醫學院`|Optional|
|星期|string|選項有`一`、`二`、`三`、`四`、`五`、`六`、`日`|Optional|
|開始節次|string|選項有 `1`、`2`、`3`、`4`、`F`、`5`、`6`、`7`、`8`、`9`、`A`、`B`、`C`、`D`，若有附上結束節次，則會搜尋有在時間區間內的結果。|Optional|
|結束節次|string|選項有 `1`、`2`、`3`、`4`、`F`、`5`、`6`、`7`、`8`、`9`、`A`、`B`、`C`、`D`，若有附上開始節次，則會搜尋有在時間區間內的結果。|Optional|
|課程類別|string|選項有`專業選修課程`、`專業必修課程`、`通識教育必修選項：基礎程式設計`、`通識教育必修科目`、`通識教育必修選項：英文`、`通識教育必修選項：體育`、`通識教育必修選項：大學國文`、`通識教育選修選項：通識領域課程`、`校訂選修`、`教育學程必修科目：教育實踐課程`、`共同選修`、`其他選修`、`教育學程必修科目：教育方法課程`、`教育學程必修科目：專門課程`、`教育學程必修科目：教育基礎課程`|Optional|
|上課學制|string|選項有 `博士班`、`大學部`、`碩士班`、`碩專班`、`進學班`|Optional|

>**Successful response**: 
> ```json
>"result": [{
>        "上課學制": "進學班",
>        "上課學院": "xx學院",
>        "上課教室": "xxx",
>        "上課時間": [{
>                "星期": "一",
>                "結束節次": "B",
>                "開始節次": "B"
>            },
>            {
>                "星期": "六",
>                "結束節次": "A",
>                "開始節次": "A"
>            }
>        ],
>        "上課班別": "甲班",
>        "上課系所": "xx系",
>        "上課組別": "不分組",
>        "備註": "",
>        "學分數": "2",
>        "學期數": "1",
>        "授課老師": "xxx",
>        "授課類別": "正課",
>        "時數": "2",
>        "校區": "蘭潭校區",
>        "永久課號": "65100090",
>        "課程修別": "必修",
>        "教學大綱": "url",  
>        "課程名稱": "xxx",
>        "課程類別": "專業必修課程",
>        "適用年級": "2",
>        "選課類別": "一般專業課程(含專業必修及專業選修課程)",
>        "開課單位": "xx系",
>        "開課序號": "0075",
>        "開課系號": "651",
>        "限修人數": "50",
>        "限選條件": "開放外系修課"
>    },
> ],
> "semester": "xxx 學年度第 x 學期"
> ```

> **Failed response**:
> ```json
> {
>   "message": {
>     "result": "error message"
>   }
> }
> ```

