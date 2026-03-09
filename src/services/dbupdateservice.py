from datetime import date, time
from utils.dbclient import DBClient


class DBUpdateService:
    def __init__(self, db: DBClient) -> None:
        self.db = db

    def update_workout(
        self,
        workout_id: int,
        workout_type_id: int,
        workout_name: str,
        workout_date: date,
        workout_start_time: time,
        workout_end_time: time,
        workout_calories: float,
        workout_note: str,
    ) -> None:
        self.db.execute(
            sql="UPDATE workout SET workout_type_id = ?, name = ?, date = ?, start_time = ?, end_time = ?, calories_burned = ?, note = ? WHERE workout_id = ?",
            params=(
                workout_type_id,
                workout_name,
                workout_date,
                workout_start_time or None,
                workout_end_time or None,
                workout_calories or None,
                workout_note or None,
                workout_id,
            ),
            commit=True,
        )

    def update_exercise_workout(
        self, exercise_workout_id: int, workout_id: int, exercise_id: int
    ) -> None:
        self.db.execute(
            sql="UPDATE exercise_workout SET workout_id = ?, exercise_id = ? WHERE exercise_workout_id = ?",
            params=(workout_id, exercise_id, exercise_workout_id),
            commit=True,
        )

    def update_set_entry(
        self,
        set_entry_id: int,
        exercise_workout_id: int,
        set_number: int,
        weight: float,
        repetitions: int,
    ) -> None:
        self.db.execute(
            sql="UPDATE set_entry SET exercise_workout_id = ?, set_number = ?, weight = ?, repetitions = ? WHERE set_entry_id = ?",
            params=(exercise_workout_id, set_number, weight, repetitions, set_entry_id),
            commit=True,
        )
