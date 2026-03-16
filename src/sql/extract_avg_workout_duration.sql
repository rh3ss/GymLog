SELECT 
    AVG((strftime('%s', end_time) - strftime('%s', start_time)) / 60.0) AS avg_duration_minutes
FROM 
    workout
WHERE 
    user_id = ?
AND 
    start_time IS NOT NULL
AND 
    end_time IS NOT NULL;
