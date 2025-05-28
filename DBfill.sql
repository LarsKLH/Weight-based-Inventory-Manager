-- Insert additional sample data into Storage table with medical equipment names
INSERT INTO Storage (storage_id, tot_weight, weight_pr)
VALUES
    ('Mini-Spike Filter', 100, 6),
    ('Clear Sight Wipe', 100, 7),
    ('Syringe', 100, 8),
    ('Scalpel', 150, 11),
    ('Gloves', 70, 2),
    ('Bandages', 100, 5),
    ('Scissors', 140, 12),
    ('Forceps', 140, 12),
    ('Fourniquet', 100, 4),
    ('Sutures', 100, 3);

-- Insert additional sample data into Operations table
INSERT INTO Operations (operation_id, procedure_link)
VALUES
    ('Nose', 'procedure1'),
    ('Ear', 'procedure2'),
    ('Throat', 'new procedure'),
    ('Eye', 'procedure3'),
    ('Dental', 'procedure4'),
    ('Orthopedic', 'procedure5'),
    ('Cardiac', 'procedure6'),
    ('Neurological', 'procedure7'),
    ('Gastrointestinal', 'procedure8'),
    ('Urological', 'procedure9'),
    ('Dermatological', 'procedure10');

-- Insert additional sample data into Calendar table with upcoming dates
INSERT INTO Calendar (datetime_id, operation_id)
VALUES
    ('03/05/2024 12:00:00', 'Nose'),
    ('04/05/2024 15:00:00', 'Ear'),
    ('05/05/2024 13:00:00', 'Throat'),
    ('06/05/2024 16:00:00', 'Eye'),
    ('07/05/2024 11:00:00', 'Dental'),
    ('08/05/2024 13:00:00', 'Orthopedic'),
    ('09/05/2024 14:00:00', 'Cardiac'),
    ('10/05/2024 10:00:00', 'Neurological'),
    ('11/05/2024 12:00:00', 'Gastrointestinal'),
    ('12/05/2024 09:00:00', 'Urological');

-- Insert additional sample data into Operation_Storage_map table
INSERT INTO Operation_Storage_map (map_id, operation_id, storage_id, quantity)
VALUES
    (4, 'Throat', 'Mini-Spike Filter', 2),
    (5, 'Ear', 'Clear Sight Wipe', 1),
    (6, 'Ear', 'Syringe', 2),
    (7, 'Nose', 'Scalpel', 1),
    (8, 'Nose', 'Gloves', 5),
    (9, 'Ear', 'Bandages', 2),
    (10, 'Throat', 'Scissors', 1),
    (11, 'Nose', 'Forceps', 1),
    (12, 'Ear', 'Fourniquet', 1),
    (13, 'Throat', 'Sutures', 3),
    (14, 'Dental', 'Scalpel', 1),
    (15, 'Orthopedic', 'Gloves', 2),
    (16, 'Cardiac', 'Bandages', 3),
    (17, 'Neurological', 'Scissors', 1),
    (18, 'Gastrointestinal', 'Forceps', 1),
    (19, 'Urological', 'Fourniquet', 1),
    (20, 'Dermatological', 'Sutures', 2),
    (21, 'Nose', 'Mini-Spike Filter', 1),
    (22, 'Ear', 'Clear Sight Wipe', 1),
    (23, 'Ear', 'Syringe', 2),
    (24, 'Nose', 'Scalpel', 1),
    (25, 'Nose', 'Gloves', 5),
    (26, 'Ear', 'Bandages', 2),
    (27, 'Throat', 'Scissors', 1),
    (28, 'Nose', 'Forceps', 1),
    (29, 'Ear', 'Fourniquet', 1),
    (30, 'Throat', 'Sutures', 3),
    (31, 'Dental', 'Scalpel', 1),
    (32, 'Orthopedic', 'Gloves', 2),
    (33, 'Cardiac', 'Bandages', 3),
    (34, 'Neurological', 'Scissors', 1),
    (35, 'Gastrointestinal', 'Forceps', 1),
    (36, 'Urological', 'Fourniquet', 1),
    (37, 'Dermatological', 'Sutures', 2);

-- Insert additional sample data into Orders table
INSERT INTO Orders (storage_id, quantity, order_date, received_date)
VALUES
    ('Mini-Spike Filter', 20, '23/04/2024 12:00:00', '26/04/2024 12:00:00'),
    ('Clear Sight Wipe', 15, '23/04/2024 12:00:00', '27/04/2024 12:00:00'),
    ('Syringe', 5, '25/04/2024 12:00:00', '27/04/2024 12:00:00'),
    ('Mini-Spike Filter', 10, '01/05/2024 12:00:00', 'not recived'),
    ('Scalpel', 5, '30/04/2024 12:00:00', '01/05/2024 12:00:00'),
    ('Scalpel', 5, '30/04/2024 12:00:00', 'not recived'),
    ('Gloves', 10, '01/05/2024 12:00:00', 'not recived'),
    ('Bandages', 15, '04/05/2024 12:00:00', 'not recived'),
    ('Scissors', 5, '06/05/2024 12:00:00', 'not recived'),
    ('Forceps', 5, '09/05/2024 12:00:00', 'not recived');

