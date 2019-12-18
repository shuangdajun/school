from flask import Blueprint

web=Blueprint("web",__name__)
from . import ErrorHandler
from . import DashBoardBlue
from . import StudentBlue
from . import TeacherBlue
from . import SubjectBlue
from . import PriceBlue
from . import UserBlue

