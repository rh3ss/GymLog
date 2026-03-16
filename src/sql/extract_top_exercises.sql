SELECT 
    e.name, 
    COUNT(*) AS count
FROM 
    exercise_workout ew
JOIN 
    exercise e
ON 
    ew.exercise_id = e.exercise_id
JOIN 
    workout w
ON 
    ew.workout_id = w.workout_id
WHERE 
    w.user_id = ?
GROUP BY 
    e.name
ORDER BY 
    count DESC
LIMIT 
    5;