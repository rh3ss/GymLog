SELECT
    set_entry_id,
    exercise_workout_id,
    set_number,
    weight,
    repetitions
FROM
    set_entry
WHERE
    exercise_workout_id IN ({placeholders})
ORDER BY
    exercise_workout_id, set_number;
