SELECT 
    ex.exercise_id AS exercise_id, 
    eq.name AS equipment_name, 
    mg.name AS muscle_group_name, 
    ex.name AS exercise_name, 
    ex.description AS exercise_description
FROM 
    exercise ex
INNER JOIN 
    equipment eq USING(equipment_id)
INNER JOIN 
    muscle_group mg USING(muscle_group_id)
ORDER BY 
    ex.name;
