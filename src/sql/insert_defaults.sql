INSERT OR IGNORE INTO workout_type (name) VALUES 
('Krafttraining'),
('Cardio'),
('Mobility');

INSERT OR IGNORE INTO equipment (name) VALUES
('Maschine'),
('Kabelturm'),
('Hantelbank'),
('Kurzhantel'),
('Langhantel'),
('Kettlebell'),
('Körpergewicht'),
('Powerkette'),
('Frei');

INSERT OR IGNORE INTO muscle_group (name) VALUES 
('Brust'),
('Rücken'),
('Trizeps'),
('Bizeps'),
('Schultern'),
('Beine'),
('Bauch'),
('Unterarme');

INSERT OR IGNORE INTO exercise (equipment_id, muscle_group_id, name, description) VALUES
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Brust'),'Schrägbankdrücken ', 'Drücken an der Schrägbankmaschine zur Stärkung der oberen Brust'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Brust'), 'Butterfly', 'Zusammenführen der Arme an der Maschine zur Isolation der Brustmuskeln'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Brust'), 'Brustpress', 'Horizontales Drücken an der Maschine für die Brustmuskulatur'),
((SELECT equipment_id FROM equipment WHERE name='Kabelturm'), (SELECT muscle_group_id FROM muscle_group WHERE name='Rücken'),'Überzüge', 'Ziehbewegung mit gestreckten Armen am Kabel zur Aktivierung des Latissimus'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Rücken'),'T-Bar Rudern', 'Rudern an der Maschine zur Kräftigung des oberen Rückens'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Rücken'),'Rudermaschine', 'Sitzendes Rudern an der Maschine für den gesamten Rücken'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Rücken'),'Lat Pull Down', 'Herunterziehen der Stange zur Brust zur Stärkung des Latissimus'),
((SELECT equipment_id FROM equipment WHERE name='Körpergewicht'), (SELECT muscle_group_id FROM muscle_group WHERE name='Rücken'),'Hyperextension ', 'Aufrichten des Oberkörpers an der Vorrichtung zur Stärkung des unteren Rückens'),
((SELECT equipment_id FROM equipment WHERE name='Kabelturm'), (SELECT muscle_group_id FROM muscle_group WHERE name='Trizeps'),'Trizepsdrücken', 'Strecken der Arme am Kabelgriff zur Isolation des Trizeps'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Trizeps'),'Trizeps Extension', 'Armstrecken an der Maschine zur Kräftigung des Trizeps'),
((SELECT equipment_id FROM equipment WHERE name='Kurzhantel'), (SELECT muscle_group_id FROM muscle_group WHERE name='Bizeps'),'Preacher Curls', 'Bizepscurls auf der Schrägbank zur isolierten Belastung des Bizeps'),
((SELECT equipment_id FROM equipment WHERE name='Kurzhantel'), (SELECT muscle_group_id FROM muscle_group WHERE name='Bizeps'),'Bizeps Curls', 'Bizepscurls hinter dem Körper für eine stärkere Dehnung des Muskels'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Schultern'),'Seitheben', 'Seitliches Anheben der Arme an der Maschine für die Schultern'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Schultern'),'Schulterdrücken', 'Überkopfdrücken an der Multipresse-Maschine zur Kräftigung der Schultern'),
((SELECT equipment_id FROM equipment WHERE name='Kurzhantel'), (SELECT muscle_group_id FROM muscle_group WHERE name='Schultern'),'Hintere Schulter', 'Anheben der Kurzhanteln nach hinten für die hintere Schultermuskulatur'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Beine'),'Beinstrecker', 'Strecken der Beine an der Maschine für den vorderen Oberschenkel'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Beine'),'Beinbeuger', 'Beugen der Beine an der Maschine für den hinteren Oberschenkel'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Beine'),'Adduktoren', 'Zusammenführen der Beine an der Maschine für die Innenschenkel'),
((SELECT equipment_id FROM equipment WHERE name='Maschine'), (SELECT muscle_group_id FROM muscle_group WHERE name='Beine'),'Beinpresse', 'Drücken der Plattform mit den Beinen zur Kräftigung der Beinmuskeln'),
((SELECT equipment_id FROM equipment WHERE name='Kabelturm'), (SELECT muscle_group_id FROM muscle_group WHERE name='Bauch'),'Crunches am Kabel', 'Crunchbewegung am Kabelturm zur Belastung der Bauchmuskeln'),
((SELECT equipment_id FROM equipment WHERE name='Körpergewicht'), (SELECT muscle_group_id FROM muscle_group WHERE name='Bauch'),'Dragon Flag', 'Langsames Absenken des Körpers für eine intensive Bauchübung'),
((SELECT equipment_id FROM equipment WHERE name='Kabelturm'), (SELECT muscle_group_id FROM muscle_group WHERE name='Unterarme'),'Wrist Curls am Kabel', 'Beugen der Handgelenke am Kabel zur Kräftigung der Unterarme'),
((SELECT equipment_id FROM equipment WHERE name='Kurzhantel'), (SELECT muscle_group_id FROM muscle_group WHERE name='Unterarme'),'Wrist Curls mit KH', 'Handgelenkcurls mit Kurzhanteln für die Unterarmmuskulatur');