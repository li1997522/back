from app_demo.config import create_app

def init_db(mysql_db='default'):
    from app_demo.config import db
    # 初始化数据祝 如果models里的对象无任何引用，刚不会创建表结构
    from app_demo.models.user import User
    from app_demo.models.office import Office

    app = create_app(mysql_db)
    app.app_context().push()
    db.drop_all()
    db.create_all()
    db.session.commit()


init_db()
