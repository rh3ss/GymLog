SELECT 
    w.workout_id AS workout_id, 
    w.user_id AS user_id, 
    wt.name AS workout_type_name, 
    w.name AS name, 
    w.date AS date, 
    w.start_time AS start_time, 
    w.end_time AS end_time, 
    w.calories_burned AS calories_burned, 
    w.note AS note
FROM 
    workout w
INNER JOIN
    workout_type wt ON w.workout_type_id = wt.workout_type_id
WHERE
    w.user_id = ?
ORDER BY
    w.date DESC
LIMIT 
    1;
