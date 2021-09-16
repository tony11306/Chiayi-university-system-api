# Chayi-university-system-api

一個用來練習 flask 架 restful api 的小專案，把嘉義大學我自己常需要查看的資料包成 api，
以後有人要用也可以 call 看看

## Login 登入

HTTP request: `Post https://chayi-university-system-api.herokuapp.com/login/{學號}/{密碼}` (不包括大括號)

| Parameters | type   | description          |
|------------|--------|----------------------|
| account    | string | 你的學號             |
| password   | string | 你的校務行政系統密碼 |

Response: 
```json
{
  "test": "test"
}
```

