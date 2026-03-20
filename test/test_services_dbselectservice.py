import sys, os
import sqlite3

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date
from utils.dbclient import DBClient
from services.dbselectservice import DBSelectService

sqlite3.register_adapter(date, lambda d: d.isoformat())


def setup_db():
    dbfilename = f"test_select_{os.getpid()}.db"
    db = DBClient(dbfilename)
    return db


def test_get_workout_types():
    db = setup_db()
    service = DBSelectService(db=db)

    db.execute("INSERT INTO workout_type (name) VALUES ('test_type')", commit=True)

    result = service.get_workout_types()

    assert len(result) > 0
    assert any(row[1] == "test_type" for row in result)


def test_get_muscle_groups():
    db = setup_db()
    service = DBSelectService(db=db)

    db.execute("INSERT INTO muscle_group (name) VALUES ('Chest')", commit=True)

    result = service.get_muscle_groups()

    assert len(result) > 0
    assert any(row[1] == "Chest" for row in result)


def test_get_equipment():
    db = setup_db()
    service = DBSelectService(db=db)

    db.execute("INSERT INTO equipment (name) VALUES ('Barbell')", commit=True)

    result = service.get_equipment()

    assert len(result) > 0
    assert result[0][1] == "Barbell"


def test_do_exercise_already_exists():
    db = setup_db()
    service = DBSelectService(db=db)

    db.execute(
        "INSERT INTO exercise (equipment_id, muscle_group_id, name) VALUES (1, 1, 'Bench Press')",
        commit=True,
    )

    assert service.do_exercise_already_exists("Bench Press") is True
    assert service.do_exercise_already_exists("Squat") is False


def test_get_workout_templates():
    db = setup_db()
    service = DBSelectService(db=db)

    db.execute(
        "INSERT INTO workout_template (user_id, name) VALUES (1, 'Leg Day')",
        commit=True,
    )

    result = service.get_workout_templates(user_id=1)

    assert len(result) == 1
    assert result[0][1] == "Leg Day"


def test_calorie_calculations():
    db = setup_db()
    service = DBSelectService(db=db)

    db.execute(
        "INSERT INTO workout (user_id, workout_type_id, name, date, calories_burned) VALUES (1, 1, 'W1', '2024-01-01', 200)",
        commit=True,
    )
    db.execute(
        "INSERT INTO workout (user_id, workout_type_id, name, date, calories_burned) VALUES (1, 1, 'W2', '2024-01-02', 300)",
        commit=True,
    )

    total = service.get_total_calories_burnd(1)
    avg = service.get_avg_calories(1)

    assert total == 500
    assert avg == 250


def test_duration_calculations():
    db = setup_db()
    service = DBSelectService(db=db)

    db.execute(
        """
        INSERT INTO workout (user_id, workout_type_id, name, date, start_time, end_time)
        VALUES (1, 1, 'W1', '2024-01-01', '10:00:00', '11:00:00')
        """,
        commit=True,
    )

    total_duration = service.get_total_duration(1)

    assert total_duration == 60.0


def test_get_exercises_workouts_by_workout_ids():
    db = setup_db()
    service = DBSelectService(db=db)

    workout_id = db.execute(
        "INSERT INTO workout (user_id, workout_type_id, name, date) VALUES (1, 1, 'Test', '2024-01-01')",
        commit=True,
        return_lastrowid=True,
    )
    exercise_id = db.execute(
        "INSERT INTO exercise (equipment_id, muscle_group_id, name) VALUES (1, 1, 'Bench')",
        commit=True,
        return_lastrowid=True,
    )
    db.execute(
        "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (?, ?)",
        (workout_id, exercise_id),
        commit=True,
    )

    result = service.get_exercises_workouts_by_workout_ids([workout_id])

    assert len(result) > 0


def test_get_sets_by_exercise_workout_ids():
    db = setup_db()
    service = DBSelectService(db=db)

    ew_id = db.execute(
        "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (1, 1)",
        commit=True,
        return_lastrowid=True,
    )
    db.execute(
        "INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
        (ew_id, 1, 100, 10),
        commit=True,
    )

    result = service.get_sets_by_exercise_workout_ids([ew_id])

    assert len(result) > 0
