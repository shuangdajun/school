import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Command, Server
# from app.models import Student, Teacher, Subject
# from app import app,db

from app import app, Schuduler
from flask_script import Manager

from app.model.Base import db
from app.model.Role import Role
from app.model.Students import Students
from app.model.User import User

manager=Manager(app)
migrate=Migrate(app,db)

#Shell的回调函数，在shell交互环境中导入dict中的模型
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Students=Students)


manager.add_command("db",MigrateCommand)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(use_debugger=True,use_reloader=True)) #Server()代指主函數

if __name__ == '__main__':
    Schuduler.start()
    manager.run()
    # app.run(debug=True)




