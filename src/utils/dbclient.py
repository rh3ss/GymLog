import sqlite3
from pathlib import Path

class DBClient:
    def __init__(self, file_path: str) -> None:
        self.db_file = Path("src/data") / file_path
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_file)

    def _execute(self, sql: str, params: tuple = (), fetch=False, commit=False) -> list[tuple] | None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if commit:
                conn.commit()
            if fetch:
                return cursor.fetchall()

    def _create_tables(self) -> None:
        # user
        self._execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                height_cm NUMERIC(5,2) NOT NULL,
                PRIMARY KEY (user_id)
            )
        """, commit=True)

        # workout_type
        self._execute("""
            CREATE TABLE IF NOT EXISTS workout_type (
                workout_type_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                PRIMARY KEY (workout_type_id)
            )
        """, commit=True)

        # muscle_group
        self._execute("""
            CREATE TABLE IF NOT EXISTS muscle_group (
                muscle_group_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                PRIMARY KEY (muscle_group_id)
            )
        """, commit=True)

        # equipment
        self._execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                equipment_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                PRIMARY KEY (equipment_id)
            )
        """, commit=True)

        # exercise
        self._execute("""
            CREATE TABLE IF NOT EXISTS exercise (
                exercise_id INTEGER NOT NULL,
                equipment_id INTEGER NOT NULL,
                muscle_group_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                PRIMARY KEY (exercise_id),
                FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id),
                FOREIGN KEY (muscle_group_id) REFERENCES muscle_group(muscle_group_id)
            )
        """, commit=True)

        # workout_template
        self._execute("""
            CREATE TABLE IF NOT EXISTS workout_template (
                workout_template_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                PRIMARY KEY (workout_template_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            )
        """, commit=True)

        # exercise_workout_template
        self._execute("""
            CREATE TABLE IF NOT EXISTS exercise_workout_template (
                id INTEGER NOT NULL,
                workout_template_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                order_number INTEGER NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (workout_template_id) REFERENCES workout_template(workout_template_id),
                FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
            )
        """, commit=True)

        # workout
        self._execute("""
            CREATE TABLE IF NOT EXISTS workout (
                workout_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                workout_type_id INTEGER NOT NULL,
                date DATE NOT NULL,
                start_time TIME,
                end_time TIME,
                calories_burned NUMERIC(4,2),
                note TEXT,
                PRIMARY KEY (workout_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (workout_type_id) REFERENCES workout_type(workout_type_id)
            )
        """, commit=True)

        # exercise_workout
        self._execute("""
            CREATE TABLE IF NOT EXISTS exercise_workout (
                id INTEGER NOT NULL,
                workout_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (workout_id) REFERENCES workout(workout_id),
                FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
            )
        """, commit=True)

        # set_entry
        self._execute("""
            CREATE TABLE IF NOT EXISTS set_entry (
                set_id INTEGER NOT NULL,
                exercise_workout_id INTEGER NOT NULL,
                set_number INTEGER NOT NULL,
                weight NUMERIC(4,2) NOT NULL,
                repetitions INTEGER NOT NULL,
                PRIMARY KEY (set_id),
                FOREIGN KEY (exercise_workout_id) REFERENCES exercise_workout(id)
            )
        """, commit=True)

    def _insert_defaults(self) -> None:
        defaults_muscle_groups = [("Brust",), ("Rücken",), ("Trizeps",), ("Bizeps",), ("Schultern",), ("Beine",), ("Bauch",), ("Unterarme",)]
        defaults_workout_types = [("Krafttraining",), ("Cardio",), ("Mobility",)]
        defaults_equipment = [("Maschine",), ("Kabelturm",), ("Kurzhantel",), ("Langhantel",), ("Kettlebell",), ("Körpergewicht",)]

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT OR IGNORE INTO muscle_group (name) VALUES (?)",
                defaults_muscle_groups
            )
            cursor.executemany(
                "INSERT OR IGNORE INTO workout_type (name) VALUES (?)",
                defaults_workout_types
            )
            cursor.executemany(
                "INSERT OR IGNORE INTO equipment (name) VALUES (?)",
                defaults_equipment
            )
            conn.commit()

