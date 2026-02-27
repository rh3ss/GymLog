from datetime import date, time
from utils.dbclient import DBClient


class WorkoutService:
    def __init__(self, db: DBClient) -> None:
        self.db = db

    def get_workout_types(self) -> list[tuple]:
        return self.db.execute(
            sql="SELECT workout_type_id, name FROM workout_type ORDER BY name",
            fetch=True,
        )

    def get_muscle_groups(self) -> list[tuple]:
        return self.db.execute(
            sql="SELECT muscle_group_id, name FROM muscle_group ORDER BY name",
            fetch=True,
        )

    def get_equipment(self) -> list[tuple]:
        return self.db.execute(
            sql="SELECT equipment_id, name FROM equipment ORDER BY name", fetch=True
        )

    def get_exercises(self) -> list[tuple]:
        sql = self.db.extract_sql(file_name="extract_exercises.sql")
        return self.db.execute(sql=sql, fetch=True)

    def get_workouts(
        self, user_id: int, filter_start_day: date, filter_end_day: date
    ) -> list[tuple]:
        sql = self.db.extract_sql(file_name="extract_workouts.sql")
        return self.db.execute(
            sql=sql,
            params=(user_id, filter_start_day.isoformat(), filter_end_day.isoformat()),
            fetch=True,
        )

    def get_last_workout(self, user_id: int) -> list[tuple]:
        sql = self.db.extract_sql(file_name="extract_last_workout.sql")
        return self.db.execute(sql=sql, params=(user_id,), fetch=True)

    def get_exercises_workouts(self, list_workout_ids: list) -> list[tuple]:
        sql = self.db.extract_sql(
            file_name="extract_exercises_workouts_by_workout_ids.sql"
        ).format(placeholders=", ".join("?" for _ in list_workout_ids))
        return self.db.execute(sql=sql, params=list_workout_ids, fetch=True)

    def get_sets(self, list_exercise_workout_ids: list) -> list[tuple]:
        sql = self.db.extract_sql(
            file_name="extract_sets_by_exercise_workout_ids.sql"
        ).format(placeholders=", ".join("?" for _ in list_exercise_workout_ids))
        return self.db.execute(sql=sql, params=list_exercise_workout_ids, fetch=True)

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

    def create_set(
        self, exercise_workout_id: int, set_number: int, weight: float, repetitions: int
    ) -> None:
        self.db.execute(
            sql="INSERT INTO set_entry (exercise_workout_id, set_number, weight, repetitions) VALUES (?, ?, ?, ?)",
            params=(exercise_workout_id, set_number, weight, repetitions),
            commit=True,
        )
