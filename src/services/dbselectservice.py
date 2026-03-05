from datetime import date
from utils.dbclient import DBClient


class DBSelectService:
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

    def get_exercises_with_equipment_and_musclegroup(self) -> list[tuple]:
        sql = self.db.extract_sql(
            file_name="extract_exercises_with_equipment_and_musclegroup.sql"
        )

        return self.db.execute(sql=sql, fetch=True)

    def do_exercise_already_exists(self, exercise_name: str) -> bool:
        exists = self.db.execute(
            "SELECT name FROM exercise WHERE name = ?", (exercise_name,), fetch=True
        )

        return bool(exists)

    def get_workouts_by_date_filtering(
        self, user_id: int, filter_start_day: date, filter_end_day: date
    ) -> list[tuple]:
        sql = self.db.extract_sql(file_name="extract_workouts_by_date_filtering.sql")

        return self.db.execute(
            sql=sql,
            params=(user_id, filter_start_day.isoformat(), filter_end_day.isoformat()),
            fetch=True,
        )

    def get_last_completed_workout(self, user_id: int) -> list[tuple]:
        sql = self.db.extract_sql(file_name="extract_last_completed_workout.sql")

        return self.db.execute(sql=sql, params=(user_id,), fetch=True)

    def get_exercises_workouts_by_workout_ids(
        self, list_workout_ids: list
    ) -> list[tuple]:
        sql = self.db.extract_sql(
            file_name="extract_exercises_workouts_by_workout_ids.sql"
        ).format(placeholders=", ".join("?" for _ in list_workout_ids))

        return self.db.execute(sql=sql, params=list_workout_ids, fetch=True)

    def get_sets_by_exercise_workout_ids(
        self, list_exercise_workout_ids: list
    ) -> list[tuple]:
        sql = self.db.extract_sql(
            file_name="extract_sets_by_exercise_workout_ids.sql"
        ).format(placeholders=", ".join("?" for _ in list_exercise_workout_ids))

        return self.db.execute(sql=sql, params=list_exercise_workout_ids, fetch=True)
