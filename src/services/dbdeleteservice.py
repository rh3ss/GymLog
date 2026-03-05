from utils.dbclient import DBClient


class DBDeleteService:
    def __init__(self, db: DBClient) -> None:
        self.db = db

    def delete_workout_entry(self, workout_id: int) -> None:
        self.db.execute(
            "DELETE FROM workout WHERE workout_id = ?;",
            params=(workout_id,),
            commit=True,
        )

    def delete_exercise_workout_entry(self, exercise_workout_id: int) -> None:
        self.db.execute(
            "DELETE FROM set_entry WHERE exercise_workout_id = ?;",
            params=(exercise_workout_id,),
            commit=True,
        )
        self.db.execute(
            "DELETE FROM exercise_workout WHERE exercise_workout_id = ?;",
            params=(exercise_workout_id,),
            commit=True,
        )

    def delete_set_entry(self, set_entry_id: int) -> None:
        self.db.execute(
            "DELETE FROM set_entry WHERE set_entry_id = ?;",
            params=(set_entry_id,),
            commit=True,
        )
