import sys, os
import sqlite3

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, time
from utils.dbclient import DBClient
from services.dbupdateservice import DBUpdateService

sqlite3.register_adapter(date, lambda d: d.isoformat())
sqlite3.register_adapter(time, lambda t: t.isoformat())


def setup_db():
    dbfilename = f"test_update_{os.getpid()}.db"
    db = DBClient(dbfilename)
    return db


def test_update_workout():
    db = setup_db()
    service = DBUpdateService(db=db)

    workout_id = db.execute(
        "INSERT INTO workout (user_id, workout_type_id, name, date) VALUES (1, 1, 'Old Name', '2024-01-01')",
        commit=True,
        return_lastrowid=True,
    )
    new_type_name = f"Cardio_{os.getpid()}"
    new_type_id = db.execute(
        "INSERT INTO workout_type (name) VALUES (?)",
        (new_type_name,),
        commit=True,
        return_lastrowid=True,
    )
    service.update_workout(
        workout_id=workout_id,
        workout_type_id=new_type_id,
        workout_name="Updated Workout",
        workout_date=date.today(),
        workout_start_time="12:00:00",
        workout_end_time="13:00:00",
        workout_calories=300.0,
        workout_note="Updated note",
    )
    rows = db.execute(
        "SELECT * FROM workout WHERE workout_id = ?", (workout_id,), fetch=True
    )

    row = rows[0]

    assert row[2] == new_type_id
    assert row[3] == "Updated Workout"
    assert row[8] == "Updated note"


def test_update_exercise():
    db = setup_db()
    service = DBUpdateService(db=db)

    exercise_id = db.execute(
        "INSERT INTO exercise (equipment_id, muscle_group_id, name, description) VALUES (1, 1, 'Bench', 'Old')",
        commit=True,
        return_lastrowid=True,
    )
    service.update_exercise(exercise_id=exercise_id, description="New Description")
    rows = db.execute(
        "SELECT description FROM exercise WHERE exercise_id = ?",
        (exercise_id,),
        fetch=True,
    )

    assert rows[0][0] == "New Description"


def test_update_exercise_workout():
    db = setup_db()
    service = DBUpdateService(db=db)

    ew_id = db.execute(
        "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (1, 1)",
        commit=True,
        return_lastrowid=True,
    )
    service.update_exercise_workout(
        exercise_workout_id=ew_id, workout_id=2, exercise_id=3
    )
    rows = db.execute(
        "SELECT workout_id, exercise_id FROM exercise_workout WHERE exercise_workout_id = ?",
        (ew_id,),
        fetch=True,
    )

    assert rows[0][0] == 2
    assert rows[0][1] == 3


def test_update_set_entry():
    db = setup_db()
    service = DBUpdateService(db=db)

    ew_id = db.execute(
        "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (1, 1)",
        commit=True,
        return_lastrowid=True,
    )
    set_id = db.execute(
        "INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
        (ew_id, 1, 100.0, 10),
        commit=True,
        return_lastrowid=True,
    )
    service.update_set_entry(
        set_entry_id=set_id,
        exercise_workout_id=ew_id,
        set_number=2,
        weight=120.0,
        repetitions=8,
    )
    rows = db.execute(
        "SELECT set_number, weight, repetitions FROM set_entry WHERE set_entry_id = ?",
        (set_id,),
        fetch=True,
    )

    assert rows[0][0] == 2
    assert rows[0][1] == 120.0
    assert rows[0][2] == 8
