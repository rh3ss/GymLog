from flask import Blueprint
from utils.dbclient import DBClient
from services.dbuserservice import DBUserService
from services.dbselectservice import DBSelectService
from services.dbcreateservice import DBCreateService
from services.dbupdateservice import DBUpdateService
from services.dbdeleteservice import DBDeleteService

gymlog_db = DBClient("gymlog.db")
db_user_service = DBUserService(db=gymlog_db)
db_select_service = DBSelectService(db=gymlog_db)
db_create_service = DBCreateService(db=gymlog_db)
db_update_service = DBUpdateService(db=gymlog_db)
db_delete_service = DBDeleteService(db=gymlog_db)

auth_bp = Blueprint("auth", __name__)
pages_bp = Blueprint("pages", __name__)
workouts_bp = Blueprint("workouts", __name__)

from .auth import auth
from .pages import pages
from .workouts import (
    create_workout,
    edit_workout,
    delete_workout,
    create_workout_template,
    create_exercise,
)
