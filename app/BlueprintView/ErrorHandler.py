
from app.BlueprintView import web
@web.errorhandler(410)
def error_4001_handle(error):
    return  "禁止重复登陆!!!"