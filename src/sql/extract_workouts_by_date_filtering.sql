SELECT 
    workout_id, 
    user_id, 
    workout_type_id, 
    name, 
    date, 
    start_time, 
    end_time, 
    calories_burned, 
    note
FROM 
    workout
WHERE 
    user_id = ? AND date BETWEEN ? AND ?
ORDER BY 
    date DESC;
