import sys, os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.dbclient import DBClient
from services.dbdeleteservice import DBDeleteService


def setup_db():
    dbfilename = f"test_delete_{os.getpid()}.db"
    db = DBClient(dbfilename)
    return db


def test_delete_workout_entry():
    db = setup_db()
    service = DBDeleteService(db=db)

    workout_id = db.execute(
        "INSERT INTO workout (user_id, workout_type_id, name, date) VALUES (1, 1, 'Test Workout', '2024-01-01')",
        commit=True,
        return_lastrowid=True,
    )

    service.delete_workout_entry(workout_id)

    rows = db.execute(
        "SELECT * FROM workout WHERE workout_id = ?", (workout_id,), fetch=True
    )

    assert rows == [] or rows is None


def test_delete_set_entry():
    db = setup_db()
    service = DBDeleteService(db=db)

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

    service.delete_set_entry(set_id)

    rows = db.execute(
        "SELECT * FROM set_entry WHERE set_entry_id = ?", (set_id,), fetch=True
    )

    assert rows == [] or rows is None


def test_delete_set_entry_by_exercise_workout_id():
    db = setup_db()
    service = DBDeleteService(db=db)

    ew_id = db.execute(
        "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (1, 1)",
        commit=True,
        return_lastrowid=True,
    )
    db.execute(
        "INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
        (ew_id, 1, 100.0, 10),
        commit=True,
    )
    db.execute(
        "INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
        (ew_id, 2, 90.0, 8),
        commit=True,
    )

    service.delete_set_entry_by_exercise_workout_id(ew_id)

    rows = db.execute(
        "SELECT * FROM set_entry WHERE exercise_workout_id = ?", (ew_id,), fetch=True
    )

    assert rows == [] or rows is None


def test_delete_exercise_workout_entry():
    db = setup_db()
    service = DBDeleteService(db=db)

    ew_id = db.execute(
        "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (1, 1)",
        commit=True,
        return_lastrowid=True,
    )

    db.execute(
        "INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
        (ew_id, 1, 100.0, 10),
        commit=True,
    )

    service.delete_exercise_workout_entry(ew_id)

    ew_rows = db.execute(
        "SELECT * FROM exercise_workout WHERE exercise_workout_id = ?",
        (ew_id,),
        fetch=True,
    )

    assert ew_rows == [] or ew_rows is None

    set_rows = db.execute(
        "SELECT * FROM set_entry WHERE exercise_workout_id = ?", (ew_id,), fetch=True
    )

    assert set_rows == [] or set_rows is None
