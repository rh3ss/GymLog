from datetime import date, time
from utils.dbclient import DBClient


class DBCreateService:
    def __init__(self, db: DBClient) -> None:
        self.db = db

    def create_workout(
        self,
        user_id: int,
        workout_type_id: int,
        workout_name: str,
        workout_date: date,
        workout_start_time: time,
        workout_end_time: time,
        workout_calories: float,
        workout_note: str,
    ) -> int:
        inserted_workout_id = self.db.execute(
            sql="INSERT INTO workout (user_id, workout_type_id, name, date, start_time, end_time, calories_burned, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            params=(
                user_id,
                workout_type_id,
                workout_name,
                workout_date,
                workout_start_time or None,
                workout_end_time or None,
                workout_calories or None,
                workout_note or None,
            ),
            commit=True,
            return_lastrowid=True,
        )
        return inserted_workout_id

    def create_workout_template(self, user_id: int, workout_name: str) -> int:
        inserted_workout_template_id = self.db.execute(
            sql="INSERT INTO workout_template (user_id, name) VALUES (?, ?)",
            params=(user_id, workout_name),
            commit=True,
            return_lastrowid=True,
        )
        return inserted_workout_template_id

    def create_exercise(
        self, equipment_id: int, muscle_group_id: int, name: str, description: str
    ) -> None:
        self.db.execute(
            sql="INSERT INTO exercise (equipment_id, muscle_group_id, name, description) VALUES (?, ?, ?, ?)",
            params=(equipment_id, muscle_group_id, name, description or None),
            commit=True,
        )

    def create_exercise_workout(self, workout_id: int, exercise_id: int) -> int:
        inserted_exercise_workout_id = self.db.execute(
            sql="INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (?, ?)",
            params=(workout_id, exercise_id),
            commit=True,
            return_lastrowid=True,
        )
        return inserted_exercise_workout_id

    def create_exercise_workout_template(
        self, workout_template_id: int, exercise_id: int, order_number: int
    ) -> None:
        self.db.execute(
            sql="INSERT INTO exercise_workout_template (workout_template_id, exercise_id, order_number) VALUES (?, ?, ?)",
            params=(workout_template_id, exercise_id, order_number),
            commit=True,
            return_lastrowid=True,
        )

    def create_set(
        self, exercise_workout_id: int, set_number: int, weight: float, repetitions: int
    ) -> None:
        self.db.execute(
            sql="INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
            params=(exercise_workout_id, set_number, weight, repetitions),
            commit=True,
        )
