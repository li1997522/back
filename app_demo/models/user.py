from app_demo.config import db
from collections import OrderedDict
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer)
    address = db.Column(db.String(100))
    tel = db.Column(db.String(15))
    create_time = db.Column(db.DateTime)

    # 定义一个属性，默认是读取的操作，这里报错，意思是不可读
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    # 定义上面那个password属性的可写属性，这里默认换算成哈希值，然后保存下来
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验传入的密码和哈希值是否是一对儿
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

    # 用户对象转为字典
    def user2dict(self):
        return OrderedDict(
            userId=self.id,
            name=self.name,
            age=self.age,
            address=self.address,
            createTime=self.create_time
        )
