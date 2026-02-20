from datetime import date, time
from utils.dbclient import DBClient

class WorkoutService:
    def __init__(self, db: DBClient) -> None:
        self.db = db

    def get_workout_types(self) -> list[tuple]:
        return self.db.execute("SELECT workout_type_id, name FROM workout_type ORDER BY name", fetch=True)
    
    def get_muscle_groups(self) -> list[tuple]:
        return self.db.execute("SELECT muscle_group_id, name FROM muscle_group ORDER BY name", fetch=True)
    
    def get_equipment(self) -> list[tuple]:
        return self.db.execute("SELECT equipment_id, name FROM equipment ORDER BY name", fetch=True)

    def create_workout(self, user_id: int, workout_type_id: int, workout_date: date, workout_start_time: time, workout_end_time: time, workout_calories: float, workout_note: str) -> None:
        self.db.execute(
            "INSERT INTO workout (user_id, workout_type_id, date, start_time, end_time, calories_burned, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, workout_type_id, workout_date, workout_start_time or None, workout_end_time or None, workout_calories or None, workout_note or None), commit=True
        )

    def create_exercise(self, equipment_id: int, muscle_group_id: int, name: str, description: str) -> None:
        self.db.execute(
            "INSERT INTO exercise (equipment_id, muscle_group_id, name, description) VALUES (?, ?, ?, ?)",
            (equipment_id, muscle_group_id, name, description or None), commit=True
        )
