import sys, os
import sqlite3

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, time
from utils.dbclient import DBClient
from services.dbcreateservice import DBCreateService

sqlite3.register_adapter(date, lambda d: d.isoformat())
sqlite3.register_adapter(time, lambda t: t.isoformat())


def setup_db():
    dbfilename = f"test_{os.getpid()}.db"
    db = DBClient(dbfilename)
    return db


def test_create_workout():
    db = setup_db()
    service = DBCreateService(db=db)

    workout_type_id = db.execute(
        "INSERT INTO workout_type (name) VALUES (?)",
        ("Strength",),
        commit=True,
        return_lastrowid=True,
    )

    workout_id = service.create_workout(
        user_id=1,
        workout_type_id=workout_type_id,
        workout_name="Push Workout",
        workout_date=date.today(),
        workout_start_time="10:00:00",
        workout_end_time="11:00:00",
        workout_calories=200.0,
        workout_note="Morning session",
    )

    assert isinstance(workout_id, int)

    rows = db.execute(
        "SELECT * FROM workout WHERE workout_id = ?", (workout_id,), fetch=True
    )

    assert len(rows) == 1

    assert rows[0][3] == "Push Workout"


def test_create_workout_template():
    db = setup_db()
    service = DBCreateService(db=db)

    template_id = service.create_workout_template(user_id=1, workout_name="Leg Day")

    assert isinstance(template_id, int)

    rows = db.execute(
        "SELECT * FROM workout_template WHERE workout_template_id = ?",
        (template_id,),
        fetch=True,
    )

    assert len(rows) == 1

    assert rows[0][2] == "Leg Day"


def test_create_exercise():
    db = setup_db()
    service = DBCreateService(db=db)

    equipment_id = db.execute(
        "INSERT INTO equipment (name) VALUES (?)",
        ("Barbell",),
        commit=True,
        return_lastrowid=True,
    )

    muscle_group_id = db.execute(
        "INSERT INTO muscle_group (name) VALUES (?)",
        ("Chest",),
        commit=True,
        return_lastrowid=True,
    )

    service.create_exercise(
        equipment_id=equipment_id,
        muscle_group_id=muscle_group_id,
        name="Bench Press",
        description="Chest exercise",
    )

    rows = db.execute(
        "SELECT * FROM exercise WHERE name = ?", ("Bench Press",), fetch=True
    )

    assert len(rows) == 1


def test_create_exercise_workout():
    db = setup_db()
    service = DBCreateService(db=db)

    exercise_id = db.execute(
        "INSERT INTO exercise (equipment_id, muscle_group_id, name) VALUES (1, 1, 'Test')",
        commit=True,
        return_lastrowid=True,
    )
    workout_id = db.execute(
        "INSERT INTO workout (user_id, workout_type_id, name, date) VALUES (1, 1, 'Test', '2024-01-01')",
        commit=True,
        return_lastrowid=True,
    )

    ew_id = service.create_exercise_workout(workout_id, exercise_id)

    assert isinstance(ew_id, int)


def test_create_set():
    db = setup_db()
    service = DBCreateService(db=db)

    ew_id = db.execute(
        "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (1, 1)",
        commit=True,
        return_lastrowid=True,
    )

    service.create_set(
        exercise_workout_id=ew_id, set_number=1, weight=100.0, repetitions=10
    )

    rows = db.execute(
        "SELECT * FROM set_entry WHERE exercise_workout_id = ?", (ew_id,), fetch=True
    )

    assert len(rows) == 1
