SELECT 
    wt.name, 
    COUNT(*) AS count
FROM 
    workout w
JOIN 
    workout_type wt
ON 
    w.workout_type_id = wt.workout_type_id
WHERE 
    w.user_id = ?
GROUP BY 
    wt.name
ORDER BY 
    count DESC;
