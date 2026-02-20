from datetime import date, time
from utils.dbclient import DBClient

class WorkoutService:
    def __init__(self, db: DBClient) -> None:
        self.db = db

    def get_workout_type(self) -> list[tuple]:
        return self.db.execute(
            "SELECT workout_type_id, name FROM workout_type ORDER BY name", fetch=True
        )

    def create_workout(self, user_id: int, workout_type_id: int, workout_date: date, workout_start_time: time, workout_end_time: time, workout_calories: float, workout_note: str) -> None:
        # workout_calories if workout_calories not in ("", None) else None,
        # workout_note if workout_note not in ("", None) else None,
        self.db.execute(
            "INSERT INTO workout (user_id, workout_type_id, date, start_time, end_time, calories_burned, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, workout_type_id, workout_date, workout_start_time or None, workout_end_time or None, workout_calories or None, workout_note or None), commit=True
        )
