from flask import Blueprint
from utils.dbclient import DBClient
from services.userservice import UserService
from services.workoutservice import WorkoutService

gymlog_db = DBClient("gymlog.db")
user_service = UserService(db=gymlog_db)
workout_service = WorkoutService(db=gymlog_db)

auth_bp = Blueprint("auth", __name__)
pages_bp = Blueprint("pages", __name__)
workouts_bp = Blueprint("workouts", __name__)

from . import auth
from . import pages
from . import add_workout
from . import add_exercise
