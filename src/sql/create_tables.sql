CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    height_cm NUMERIC(5,2) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS workout_type (
    workout_type_id INTEGER NOT NULL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (workout_type_id)
);

CREATE TABLE IF NOT EXISTS muscle_group (
    muscle_group_id INTEGER NOT NULL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (muscle_group_id)
);

CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INTEGER NOT NULL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (equipment_id)
);

CREATE TABLE IF NOT EXISTS exercise (
    exercise_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    muscle_group_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    PRIMARY KEY (exercise_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id),
    FOREIGN KEY (muscle_group_id) REFERENCES muscle_group(muscle_group_id)
);

CREATE TABLE IF NOT EXISTS workout_template (
    workout_template_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (workout_template_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS exercise_workout_template (
    id INTEGER NOT NULL,
    workout_template_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    order_number INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (workout_template_id) REFERENCES workout_template(workout_template_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
);

CREATE TABLE IF NOT EXISTS workout (
    workout_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    workout_type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    calories_burned NUMERIC(4,2),
    note TEXT,
    PRIMARY KEY (workout_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (workout_type_id) REFERENCES workout_type(workout_type_id)
);

CREATE TABLE IF NOT EXISTS exercise_workout (
    id INTEGER NOT NULL,
    workout_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (workout_id) REFERENCES workout(workout_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
);

CREATE TABLE IF NOT EXISTS set_entry (
    set_id INTEGER NOT NULL,
    exercise_workout_id INTEGER NOT NULL,
    set_number INTEGER NOT NULL,
    weight NUMERIC(4,2) NOT NULL,
    repetitions INTEGER NOT NULL,
    PRIMARY KEY (set_id),
    FOREIGN KEY (exercise_workout_id) REFERENCES exercise_workout(id)
);
