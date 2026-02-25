SELECT 
    ew.exercise_workout_id AS exercise_workout_id, 
    ew.workout_id AS workout_id, 
    ex.exercise_id AS exercise_id, 
    eq.name AS equipment_name, 
    mg.name AS muscle_group_name, 
    ex.name AS exercise_name, 
    ex.description AS exercise_description
FROM 
    exercise_workout ew
INNER JOIN 
    exercise ex ON ew.exercise_id = ex.exercise_id
INNER JOIN 
    equipment eq ON ex.equipment_id = eq.equipment_id
INNER JOIN 
    muscle_group mg ON ex.muscle_group_id = mg.muscle_group_id
WHERE 
    ew.workout_id IN ({placeholders});
