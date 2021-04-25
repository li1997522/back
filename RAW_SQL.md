使用 sqlalchemy 有3种方式:
方式1, 使用raw sql; 
方式2, 使用SqlAlchemy的sql expression; 
方式3, 使用ORM.  
前两种方式可以统称为 core 方式. 本文讲解 core 方式访问数据库, 不涉及 ORM. 

对于绝大多数应用, 推荐使用 SqlAlchemy. 即使是使用raw sql, SqlAlchemy 也可以带来如下好处: 
1. 内建数据库连接池. [注意]如果是sqlalchemy+cx_oracle的话, 需要禁掉 connection pool, 否则会有异常. 方法是设置sqlalchemy.poolclass为sqlalchemy.pool.NullPool
2. 强大的log功能
3. 数据库中立的写法, 包括: sql参数写法, limit语法
4. 特别提一下, where()条件的==your_value, 如果your_value等于None, 真正的Sql会转为Is None

SqlAlchemy的sql expression和raw sql的比较:
1. sql expression 写法是纯python代码, 阅读性更好, 尤其是在使用insert()方法时, 字段名和取值成对出现.  
2. raw sql 比 sql expression 更灵活, 如果SQL/DDL很复杂, raw sql就更有优势了. 

==============================
sqlalchemy 超简单教程
==============================
http://solovyov.net/en/2011/04/23/basic-sqlalchemy/
http://flask.pocoo.org/docs/patterns/sqlalchemy/#sql-abstraction-layer
http://www.blog.pythonlibrary.org/2010/09/10/sqlalchemy-connecting-to-pre-existing-databases/
http://www.blog.pythonlibrary.org/2010/02/03/another-step-by-step-sqlalchemy-tutorial-part-1-of-2/
http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
http://mapfish.org/doc/tutorials/sqlalchemy.html
sqlalchemy 官网的pdf文档, 可以作为 reference 使用


==============================
常用的数据库连接字符串
==============================
#sqlite
sqlite_db = create_engine('sqlite:////absolute/path/database.db3')
sqlite_db = create_engine('sqlite://')  # in-memory database
sqlite_db = create_engine('sqlite:///:memory:') # in-memory database
# postgresql
pg_db = create_engine('postgres://scott:tiger@localhost/mydatabase')
# mysql
mysql_db = create_engine('mysql://scott:tiger@localhost/mydatabase')
# oracle
oracle_db = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')
# oracle via TNS name
oracle_db = create_engine('oracle://scott:tiger@tnsname')
# mssql using ODBC datasource names.  PyODBC is the default driver.
mssql_db = create_engine('mssql://mydsn')
mssql_db = create_engine('mssql://scott:tiger@mydsn')
# firebird
firebird_db = create_engine('firebird://scott:tiger@localhost/sometest.gdm')

==============================
关于一些非主流数据库缺少DB API接口的问题
==============================
比如teradata, 没有专门的DB API实现, 但 odbc driver肯定会提供的, 否则就无法在江湖上混了. pypyodbc + ODBC driver 应该是一个选项. pypyodbc 和 pyodbc接口一致, 同时它是纯 python实现, 理论上应该支持 python/ironpython/jython. 另外, 我猜想sqlalchemy应该能基于这一组合访问所有的数据库, 待验证. 
 pypyodbc 主页:  http://code.google.com/p/pypyodbc/


==============================
#connnectionless执行和connnection执行
==============================
1. 直接使用engine执行sql的方式, 叫做connnectionless执行, 
2. 先使用 engine.connect()获取conn, 然后通过conn执行sql, 叫做connection执行
如果要在transaction模式下执行, 推荐使用connection方式, 如果不涉及transaction, 两种方法效果是一样的. 

==============================
#sqlalchemy推荐使用text()函数封装一下sql字符串
==============================
好处巨多:
1. 不同数据库, 可以使用统一的sql参数传递写法. 参数须以:号引出. 在调用execute()的时候, 使用dict结构将实参传进去. 
    from sqlalchemy import text
    result = db.execute(text('select * from table where id < :id and typeName=:type'), {'id': 2,'type':'USER_TABLE'})
2. 如果不指定parameter的类型, 默认为字符串类型; 如果要传日期参数, 需要使用text()的bindparams参数来声明
    from sqlalchemy import DateTime
    date_param=datetime.today()+timedelta(days=-1*10)
    sql="delete from caw_job_alarm_log  where alarm_time<:alarm_time_param"
    t=text(sql, bindparams=[bindparam('alarm_time_param', type_=DateTime, required=True)])
    db.execute(t,{"alarm_time_param": date_param})    

    参数bindparam可以使用type_来指定参数的类型, 也可以使用 initial 值来指定参数类型
        bindparam('alarm_time_param', type_=DateTime) #直接指定参数类型
        bindparam('alarm_time_param', DateTime()) #使用初始值指定参数类型
3. 如要转换查询的结果中的数据类型, 可以通过text()的参数typemap参数指定. 这点比mybatis还灵活,
        t = text("SELECT id, name FROM users",
                typemap={
                    'id':Integer,
                    'name':Unicode
                }
        )
4. 还有其他, 详见sqlalchemy\sql\expression.py中的docstring. 


==============================
#sqlalchemy访问数据库的示例
==============================
#-----------------------------------
#获取数据库
#-----------------------------------
from sqlalchemy import create_engine
db=create_engine("sqlite:///:memory:", echo=True)


#-----------------------------------
#DDL
#-----------------------------------
db.execute("create table users(userid char(10), username char(50))")


#-----------------------------------
#DML
#-----------------------------------
resultProxy=db.execute("insert into users (userid,username) values('user1','tony')")
resultProxy.rowcount  #return rows affected by an UPDATE or DELETE statement


#-----------------------------------
#Query
#-----------------------------------
resultProxy=db.execute("select * from users")
resultProxy.close(), resultProxy 用完之后, 需要close
resultProxy.scalar(), 可以返回一个标量查询的值
ResultProxy 类是对Cursor类的封装(在文件sqlalchemy\engine\base.py),
ResultProxy 类有个属性cursor即对应着原来的cursor.
ResultProxy 类有很多方法对应着Cursor类的方法, 另外有扩展了一些属性/方法.
resultProxy.fetchall()
resultProxy.fetchmany()
resultProxy.fetchone()
resultProxy.first()
resultProxy.scalar()
resultProxy.returns_rows  #True if this ResultProxy returns rows.
resultProxy.rowcount  #return rows affected by an UPDATE or DELETE statement. It is not intended to provide the number of rows present from a SELECT.

****遍历ResultProxy时, 得到的每一个行都是RowProxy对象, 获取字段的方法非常灵活, 下标和字段名甚至属性都行. rowproxy[0] == rowproxy['id'] == rowproxy.id, 看得出 RowProxy 已经具备基本 POJO 类特性.  


#-----------------------------------
#使用transaction
#-----------------------------------
#SqlAlchemy支持支持事务, 甚至事务可以嵌套. 缺省事务是自动提交，即执行一条SQL就自动提交。

#-如果更精准地控制事务, 最简单的方法是使用 connection, 然后通过connection获取transaction对象
connection = db.connect()
trans = connection.begin()
try:
    dosomething(connection)
    trans.commit()
except:   
    trans.rollback()

#-还有一种方式是,在创建engine时指定strategy='threadlocal'参数，这样会自动创建一个线程局部的连接，对于后续的无连接的执行都会自动使用这个连接，这样在处理事务时，只要使用 engine 对象来操作事务就行了。如：
#参见 http://hi.baidu.com/limodou/blog/item/83f4b2194e94604043a9ad9c.html
db = create_engine(connection, strategy='threadlocal')
db.begin()
try:
    dosomething()
except:
    db.rollback()
else:
    db.commit()


#-缺省事务是自动提交，即执行一条SQL就自动提交. 也可以在connection和statement上通过execution_options()方法修改为手动commit模式
conn.execution_options(autocommit=False)
设置为手动提交模式后, 要提交, 需要调用conn.commit()



#-----------------------------------
#如何使用 pyDbRowFactory
#-----------------------------------
#pyDbRowFactory是我开发的一个通用RowFactory, 可以绑定cursor和你的 model pojo 类, 新版本的pyDbRowFactoryResultProxy. 下面示例是pyDbRowFactory的最基本用法
#方法1, 使用 cursor对象
cursor=resultProxy.cursor
from pyDbRowFactory import DbRowFactory
rowFactory=DbRowFactory(cursor, "your_module.your_row_class") 
lst=factory.fetchAllRowObjects()

#方法2, 直接使用 resultProxy
from pyDbRowFactory import DbRowFactory 
factory=DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "your_module.your_row_class")
lst=factory.fetchAllRowObjects()

前面讲过, SQLAlchemy使用 ResultProxy封装了cursor, ResultProxy的每一个行记录是一个RowProxy 类对象. RowProxy 使用起来非常方便,  对于查询select userName from users,  
每一个行结果都可以使用rowproxy来访问, 写法相当灵活.  rowproxy.userName=rowproxy["userName"]==rowproxy[0], 所以有了RowProxy,  很多时候, 没有必要再为每个表创建一个 model pojo 类.  



#-----------------------------------
#连接池
#-----------------------------------
sqlalchemy 默认的连接池算法选用规则为:
1.连接内存中的sqlite, 默认的连接池算法为 SingletonThreadPool 类, 即每个线程允许一个连接
2.连接基于文件的sqlite, 默认的连接池算法为 NullPool 类, 即没有连接池
3.对于其他情况, 默认的连接池算法为 QueuePool 类
当然, 我们也可以实现自己的连接池算法, 
db = create_engine('sqlite:///file.db', poolclass=YourPoolClass)
create_engine()函数和连接池相关的参数有:
-pool_recycle, 默认为-1, 推荐设置为7200, 即如果connection空闲了7200秒, 自动重新获取, 以防止connection被db server关闭. 
-pool_size=5, 连接数大小，默认为5，正式环境该数值太小，需根据实际情况调大
-max_overflow=10, 超出pool_size后可允许的最大连接数，默认为10, 这10个连接在使用过后, 不放在pool中, 而是被真正关闭的. 
-pool_timeout=30, 获取连接的超时阈值, 默认为30秒



#-----------------------------------
#log输出
#-----------------------------------
--如果只需在sys.stdout输出, 用不着引用 logging 模块就能实现
db = create_engine('sqlite:///file.db', echo=True)

--如果要在文件中输出, log文件不具备rotate功能, 不推荐在生产环境中使用. 
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


#-----------------------------------
#使用 sqlalchemy core 的最佳实践
#-----------------------------------
我不太喜欢使用ORM方式, 主要是ORM学习成本比较高, 另外, 构建复杂的查询也比较困难. 更多的时候是使用raw sql和sql expression方法. 
1. declarative 是 SqlAlchemy的一个新的扩展, 只能用在 ORM 中, 不能用在SQL Expression中
2. 如果要使用ORM时, table必须有主键; 使用 raw sql和sql expression, 没有这个约束.

使用心得: 
1. 查询不管是否复杂, 直接使用 raw sql; 增删改多是单表操作, 使用sql expression 就足够了. 
2. 具体讲, 对于增删改, 比如一个User类, 可包含一个固定的 _table 的成员, _table=Table('users', metadata, autoload=True), 增删改直接使用_table对象来完成.
3. 对于查询, 若结果集能映射到一个实体对象, 使用pyDbRowFactory完成对象实例化. 若结果集涉及多个实体, 直接使用ResultProxy, ResultProxy的每一行对象也具有基本的对象特征, 多数情况下没有必要再专门映射成一个特别的类. 
4. 表之间关系的处理, 比如: users 表和 addresses 表, 存在 1:n的关系, 对应地, User 类也会有个AddressList的成员, 在实体化一个User对象后, 我们可立即查询 addresses 表, 获取该用户的address列表, 分2步就可以完成这种1:n的关系映射.


使用 sqlalchemy 的写法太灵活了, 下面仅仅是我喜欢的一种写法, 仅仅从排版看, 就相当漂亮.
构建insert语句: _table.insert().values(f1=value1,f2=value2,)
构建update语句: _table.update().values(f1=newvalue1,f2=newvalue2).where(_table.c.f1==value1).where(_table.c.f2==value2)
构建delete语句: _table.delete().where(_table.c.f1==value1).where(_table.c.f2==value2)
批量insert/update/delete, 将每行数据组成一个dict, 再将这些dict组成一个list, 和_table.insert()/update()/delete()一起作为参数传给 conn.execute(). 
    conn.execute(_table.insert(), [
    {’user_id’: 1, ’email_address’ : ’jack@yahoo.com’},
    {’user_id’: 1, ’email_address’ : ’jack@msn.com’},
    {’user_id’: 2, ’email_address’ : ’www@www.org’},
    {’user_id’: 2, ’email_address’ : ’wendy@aol.com’},
    ])
sql expression 也可以像raw sql的text函数一样使用bindparam, 方法是, 在调用insert()/update()/delete()时声明参数, 然后在conn.execute()执行时候, 将实参传进去. 
    d=_table.delete().where(_table.c.hiredate<=bindparam("hire_day",DateTime(), required=True))
    conn.execute(d, {"hire_day":datetime.today()})



where()和ORM中的filter()接受的参数是一样, 各种SQL条件都支持. 
#equals:
where(_table.c.name == ’ed’)
#not equals:
where(_table.c.name != ’ed’)
#LIKE:
where(_table.c.name.like(’%ed%’))
#IN:
where(_table.c.name.in_([’ed’, ’wendy’, ’jack’]))
#NOT IN:
where(~_table.c.name.in_([’ed’, ’wendy’, ’jack’]))
#IS NULL:
where(_table.c.name == None)
#IS NOT NULL:
where(_table.c.name != None)
#AND:
from sqlalchemy import and_
where(and_(_table.c.name == ’ed’, _table.c.fullname == ’Ed Jones’))
#AND也可以通过多次调用where()来实现
where(_table.c.name == ’ed’).where(_table.c.fullname == ’Ed Jones’)
#OR:
from sqlalchemy import or_
where(or_(_table.c.name == ’ed’, _table.c.name == ’wendy’))
#match: The contents of the match parameter are database backend specific.
where(_table.c.name.match(’wendy’))


--==========================
--python file: mydatabase.py
--==========================
from sqlalchemy import create_engine 
from sqlalchemy.schema import MetaData

#db = create_engine('sqlite:///:memory:',  echo=True)
db = create_engine('sqlite:///c://caw.sqlite.db',  echo=True)
metadata = MetaData(bind=db) 


--==========================
--python file: dal.py 
--==========================
from sqlalchemy.sql.expression import text, bindparam
from sqlalchemy.sql import select,insert, delete, update
from sqlalchemy.schema import Table

from mydatabase import db,metadata
from pyDbRowFactory import DbRowFactory    

class caw_job(object):
    FULL_NAME="dal.caw_job"
    tablename="caw_job"
    _table=Table(tablename, metadata, autoload=True)

    def __init__(self):
        self.app_domain       =None
        self.job_code         =None
        self.job_group        =None 
        self.cron_year        =None
        self.cron_month       =None
        self.cron_day         =None
        self.cron_week        =None
        self.cron_day_of_week =None
        self.cron_hour        =None
        self.cron_minute      =None
        self.description      =None 

    @classmethod    
    def getEntity(cls, app_domain, jobCode):
        sql="select * from caw_job where app_domain=:app_domain and job_code=:job_code";
        resultProxy=db.execute(text(sql),{'app_domain':app_domain,
                                          'job_code':jobCode})
        DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, cls.FULL_NAME)
        return DbRowFactory.fetchOneRowObject()


    def insert(self):
        i=self._table.insert().values(
                                      app_domain      =self.app_domain      ,     
                                      job_code        =self.job_code        ,
                                      job_group       =self.job_group       ,
                                      cron_year       =self.cron_year       ,
                                      cron_month      =self.cron_month      ,
                                      cron_day        =self.cron_day        ,
                                      cron_week       =self.cron_week       ,
                                      cron_day_of_week=self.cron_day_of_week,
                                      cron_hour       =self.cron_hour       ,
                                      cron_minute     =self.cron_minute     ,
                                      description     =self.description     ,                                      
                                      ) 
        db.execute(i)

    def update(self):
        u=self._table.update().values(
                                      app_domain       =self.app_domain       ,     
                                      job_code         =self.job_code         ,
                                      job_group        =self.job_group        ,
                                      cron_year        =self.cron_year        ,
                                      cron_month       =self.cron_month       ,
                                      cron_day         =self.cron_day         ,
                                      cron_week        =self.cron_week        ,
                                      cron_day_of_week =self.cron_day_of_week ,
                                      cron_hour        =self.cron_hour        ,
                                      cron_minute      =self.cron_minute      ,
                                      description      =self.description      ,                ,                                         
                                      ).where(self._table.c.app_domain==self.app_domain)\
                                      .where(self._table.c.job_code==self.job_code)
        db.execute(u)


    def delete(self):
        d=self._table.delete().where(self._table.c.app_domain==self.app_domain)\
         .where(self._table.c.job_code==self.job_code)
        db.execute(d)




#-----------------------------------
#使用sqlalchemy.ext.declarative 来生成表, 所有的表都必须有主键.
#在系统初期, 数据模型往往需要经常调整, 使用这种方式修改表结构更方便些.
#-----------------------------------
--python file: models.py
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , Boolean, DateTime, Float

engine = create_engine('sqlite:///:memory:',  echo=True)
Base = declarative_base()

#  ddl_caw_job 是专门用来生成数据库对象的, 没有其他用处    
class ddl_caw_job(Base): 
    __tablename__="caw_job"
    job_name   =Column(String(200), primary_key=True)
    job_group  =Column(String(200))

def init_db():
    Base.metadata.create_all(bind=engine,)    
    
    
resultProxy.rowcount  #return rows affected by an UPDATE or DELETE statement. 

resultProxy.scalar() # 可以返回一个标量查询的值
#ResultProxy 类是对Cursor类的封装(在文件sqlalchemy\engine\base.py),
#ResultProxy 类有个属性cursor即对应着原来的cursor.
#ResultProxy 类有很多方法对应着Cursor类的方法, 另外有扩展了一些属性/方法.
#resultProxy.fetchall()
#resultProxy.fetchmany()
#resultProxy.fetchone()
#resultProxy.first()
#resultProxy.returns_rows  #True if this ResultProxy returns rows.

resultProxy.close() # resultProxy 用完之后, 需要close