SELECT 
    ewt.exercise_id AS exercise_id, 
    eq.name AS equipment_name, 
    mg.name AS muscle_group_name, 
    ex.name AS exercise_name, 
    ex.description AS exercise_description
FROM 
    exercise_workout_template ewt
INNER JOIN 
    exercise ex ON ewt.exercise_id = ex.exercise_id
INNER JOIN 
    equipment eq ON ex.equipment_id = eq.equipment_id
INNER JOIN 
    muscle_group mg ON ex.muscle_group_id = mg.muscle_group_id
WHERE 
    ewt.workout_template_id = ?
ORDER BY
    ewt.order_number;