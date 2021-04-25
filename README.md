pyinstaller -F run.py

项目目录
```
├─flask-restful-demo
│  ├─app_demo
│  │  ├─app_api_v1
│  │  ├─config
│  │  ├─dto
│  │  ├─models
│  │  ├─routes
│  ├─static
│  ├─templates
```
依赖
- flask – Python的微框架
- flask_restful – 这是Flask的扩展，可快速构建REST API。
- flask_script – 提供了在Flask中编写外部脚本的支持。
- flask_migrate – 使用Alembic的Flask应用进行SQLAlchemy数据库迁移。
- marshmallow – ORM/ODM/框架无关的库，用于复杂数据类型（如对象）和Python数据类型转换。
- flask_sqlalchemy – Flask扩展，增加了对SQLAlchemy的支持。
- flask_marshmallow – 这是Flask和marshmallow的中间层。
- marshmallow-sqlalchemy – 这是sqlalchemy和marshmallow的中间层。
- psycopg – Python的PostgreSQL API。

安装依赖
```shell script
 pip install -r requirements.txt
```

常用的HTTP动词有下面五个（括号里是对应的SQL命令）。

- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH（UPDATE）：在服务器更新资源（客户端提供部分改变的属性）。
- DELETE（DELETE）：从服务器删除资源。
- HEAD：获取资源的元数据。
- OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。


状态码[更多状态码 https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html]
- 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
- 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
- 202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
- 204 NO CONTENT - [DELETE]：用户删除数据成功。
- 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
- 401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
- 403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
- 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
- 406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
- 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
- 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
- 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。

```shell script
curl http://127.0.0.1:5000/api/Category --data '{"name":"test5","id":5}' -H "Content-Type: application/json"
```