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

    def get_exercises(self) -> list[tuple]:
        return self.db.execute("""
            SELECT ex.exercise_id AS exercise_id, eq.name AS equipment_name, mg.name AS muscle_group_name, ex.name AS exercise_name, ex.description AS exercise_description
            FROM exercise ex
            INNER JOIN equipment eq USING(equipment_id)
            INNER JOIN muscle_group mg USING(muscle_group_id)
            ORDER BY ex.name; 
            """, fetch=True
        )

    def create_workout(self, user_id: int, workout_type_id: int, workout_name: str, workout_date: date, workout_start_time: time, workout_end_time: time, workout_calories: float, workout_note: str) -> int:
        inserted_workout_id = self.db.execute(
            "INSERT INTO workout (user_id, workout_type_id, name, date, start_time, end_time, calories_burned, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, workout_type_id, workout_name, workout_date, workout_start_time or None, workout_end_time or None, workout_calories or None, workout_note or None), 
            commit=True, return_lastrowid=True
        )
        return inserted_workout_id
    
    def create_exercise(self, equipment_id: int, muscle_group_id: int, name: str, description: str) -> None:
        self.db.execute(
            "INSERT INTO exercise (equipment_id, muscle_group_id, name, description) VALUES (?, ?, ?, ?)",
            (equipment_id, muscle_group_id, name, description or None), commit=True
        )

    def create_exercise_workout(self, workout_id: int, exercise_id: int) -> int:
        inserted_exercise_workout_id = self.db.execute(
            "INSERT INTO exercise_workout (workout_id, exercise_id) VALUES (?, ?)",
            (workout_id, exercise_id),
            commit=True, return_lastrowid=True
        )
        return inserted_exercise_workout_id
    
    def create_set(self, exercise_workout_id: int, set_number: int, weight: float, repetitions: int) -> None:
        self.db.execute(
            "INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
            (exercise_workout_id, set_number, weight, repetitions), commit=True
        )
