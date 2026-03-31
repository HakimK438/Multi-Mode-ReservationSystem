select * from users
select * from vehicles
select * from routes
select * from trips
select * from seats
select * from bookings
select * from payments

INSERT INTO users (name, email, phone) VALUES
('Amit Sharma', 'amit.sharma1@gmail.com', '9000000001'),
('Priya Verma', 'priya.verma2@gmail.com', '9000000002'),
('Rahul Mehta', 'rahul.mehta3@gmail.com', '9000000003'),
('Sneha Iyer', 'sneha.iyer4@gmail.com', '9000000004'),
('Arjun Patel', 'arjun.patel5@gmail.com', '9000000005'),
('Neha Gupta', 'neha.gupta6@gmail.com', '9000000006'),
('Vikram Singh', 'vikram.singh7@gmail.com', '9000000007'),
('Pooja Nair', 'pooja.nair8@gmail.com', '9000000008'),
('Karan Malhotra', 'karan.malhotra9@gmail.com', '9000000009'),
('Anjali Desai', 'anjali.desai10@gmail.com', '9000000010'),
('Rohit Kapoor', 'rohit.kapoor11@gmail.com', '9000000011'),
('Meera Joshi', 'meera.joshi12@gmail.com', '9000000012'),
('Siddharth Roy', 'siddharth.roy13@gmail.com', '9000000013'),
('Kavya Reddy', 'kavya.reddy14@gmail.com', '9000000014'),
('Aditya Kulkarni', 'aditya.kulkarni15@gmail.com', '9000000015'),
('Ishita Chatterjee', 'ishita.chatterjee16@gmail.com', '9000000016'),
('Manish Yadav', 'manish.yadav17@gmail.com', '9000000017'),
('Divya Bansal', 'divya.bansal18@gmail.com', '9000000018'),
('Harsh Jain', 'harsh.jain19@gmail.com', '9000000019'),
('Ritika Sinha', 'ritika.sinha20@gmail.com', '9000000020');


INSERT INTO vehicles (type, name, number_code) VALUES
('train', 'Rajdhani Express', 'TR1001'),
('train', 'Shatabdi Express', 'TR1002'),
('train', 'Duronto Express', 'TR1003'),
('train', 'Garib Rath', 'TR1004'),
('train', 'Vande Bharat Express', 'TR1005'),
('flight', 'Air India AI202', 'FL2001'),
('flight', 'IndiGo 6E303', 'FL2002'),
('flight', 'SpiceJet SG404', 'FL2003'),
('flight', 'Vistara UK505', 'FL2004'),
('flight', 'GoAir G8506', 'FL2005'),
('ship', 'Ocean Queen', 'SH3001'),
('ship', 'Sea Explorer', 'SH3002'),
('ship', 'Island Cruiser', 'SH3003'),
('ship', 'Blue Water Ship', 'SH3004'),
('ship', 'Coral Voyager', 'SH3005'),
('train', 'Intercity Express', 'TR1006'),
('flight', 'AirAsia I5507', 'FL2006'),
('ship', 'Sunset Cruise', 'SH3006'),
('train', 'Tejas Express', 'TR1007'),
('flight', 'Emirates EK508', 'FL2007');



INSERT INTO routes (from_location, to_location, distance) VALUES
('Mumbai', 'Delhi', 1400),
('Delhi', 'Kolkata', 1500),
('Chennai', 'Bangalore', 350),
('Hyderabad', 'Mumbai', 700),
('Pune', 'Goa', 450),
('Ahmedabad', 'Jaipur', 650),
('Kolkata', 'Bhubaneswar', 440),
('Delhi', 'Chandigarh', 250),
('Mumbai', 'Ahmedabad', 530),
('Bangalore', 'Hyderabad', 570),
('Chennai', 'Kolkata', 1650),
('Delhi', 'Lucknow', 500),
('Mumbai', 'Pune', 150),
('Jaipur', 'Delhi', 280),
('Goa', 'Bangalore', 560),
('Hyderabad', 'Chennai', 630),
('Ahmedabad', 'Mumbai', 530),
('Kolkata', 'Patna', 600),
('Delhi', 'Amritsar', 450),
('Bangalore', 'Chennai', 350);




INSERT INTO trips (vehicle_id, route_id, departure_time, arrival_time, price) VALUES
(1, 1, '2026-04-01 08:00:00', '2026-04-01 20:00:00', 1500.00),
(2, 2, '2026-04-02 06:00:00', '2026-04-02 18:00:00', 1400.00),
(3, 3, '2026-04-03 09:00:00', '2026-04-03 14:00:00', 800.00),
(4, 4, '2026-04-04 07:30:00', '2026-04-04 17:30:00', 1200.00),
(5, 5, '2026-04-05 05:00:00', '2026-04-05 13:00:00', 900.00),
(6, 6, '2026-04-01 10:00:00', '2026-04-01 12:00:00', 4500.00),
(7, 7, '2026-04-02 11:00:00', '2026-04-02 13:00:00', 4000.00),
(8, 8, '2026-04-03 12:00:00', '2026-04-03 14:00:00', 3500.00),
(9, 9, '2026-04-04 15:00:00', '2026-04-04 17:00:00', 4200.00),
(10, 10, '2026-04-05 16:00:00', '2026-04-05 18:00:00', 3800.00),
(11, 11, '2026-04-06 08:00:00', '2026-04-06 20:00:00', 2000.00),
(12, 12, '2026-04-07 06:00:00', '2026-04-07 12:00:00', 1000.00),
(13, 13, '2026-04-08 07:00:00', '2026-04-08 09:00:00', 500.00),
(14, 14, '2026-04-09 08:00:00', '2026-04-09 12:00:00', 700.00),
(15, 15, '2026-04-10 09:00:00', '2026-04-10 15:00:00', 1100.00),
(16, 16, '2026-04-11 10:00:00', '2026-04-11 16:00:00', 1300.00),
(17, 17, '2026-04-12 11:00:00', '2026-04-12 13:00:00', 4100.00),
(18, 18, '2026-04-13 12:00:00', '2026-04-13 20:00:00', 2200.00),
(19, 19, '2026-04-14 06:00:00', '2026-04-14 14:00:00', 1600.00),
(20, 20, '2026-04-15 07:00:00', '2026-04-15 12:00:00', 900.00);



INSERT INTO seats (trip_id, seat_number, status) VALUES
-- Trip 1
(1,1,'available'),(1,2,'booked'),(1,3,'available'),(1,4,'booked'),(1,5,'available'),
-- Trip 2
(2,1,'available'),(2,2,'available'),(2,3,'booked'),(2,4,'available'),(2,5,'booked'),
-- Trip 3
(3,1,'booked'),(3,2,'available'),(3,3,'available'),(3,4,'booked'),(3,5,'available'),
-- Trip 4
(4,1,'available'),(4,2,'booked'),(4,3,'available'),(4,4,'available'),(4,5,'booked'),
-- Trip 5
(5,1,'available'),(5,2,'available'),(5,3,'booked'),(5,4,'available'),(5,5,'available'),
-- Trip 6
(6,1,'booked'),(6,2,'available'),(6,3,'available'),(6,4,'booked'),(6,5,'available'),
-- Trip 7
(7,1,'available'),(7,2,'available'),(7,3,'booked'),(7,4,'available'),(7,5,'booked'),
-- Trip 8
(8,1,'available'),(8,2,'booked'),(8,3,'available'),(8,4,'available'),(8,5,'available'),
-- Trip 9
(9,1,'booked'),(9,2,'available'),(9,3,'available'),(9,4,'booked'),(9,5,'available'),
-- Trip 10
(10,1,'available'),(10,2,'available'),(10,3,'booked'),(10,4,'available'),(10,5,'available'),
-- Trip 11
(11,1,'available'),(11,2,'booked'),(11,3,'available'),(11,4,'available'),(11,5,'booked'),
-- Trip 12
(12,1,'available'),(12,2,'available'),(12,3,'booked'),(12,4,'available'),(12,5,'available'),
-- Trip 13
(13,1,'booked'),(13,2,'available'),(13,3,'available'),(13,4,'booked'),(13,5,'available'),
-- Trip 14
(14,1,'available'),(14,2,'available'),(14,3,'booked'),(14,4,'available'),(14,5,'available'),
-- Trip 15
(15,1,'available'),(15,2,'booked'),(15,3,'available'),(15,4,'available'),(15,5,'booked'),
-- Trip 16
(16,1,'available'),(16,2,'available'),(16,3,'booked'),(16,4,'available'),(16,5,'available'),
-- Trip 17
(17,1,'booked'),(17,2,'available'),(17,3,'available'),(17,4,'booked'),(17,5,'available'),
-- Trip 18
(18,1,'available'),(18,2,'available'),(18,3,'booked'),(18,4,'available'),(18,5,'available'),
-- Trip 19
(19,1,'available'),(19,2,'booked'),(19,3,'available'),(19,4,'available'),(19,5,'available'),
-- Trip 20
(20,1,'booked'),(20,2,'available'),(20,3,'available'),(20,4,'booked'),(20,5,'available');





INSERT INTO bookings (user_id, trip_id, seat_id, booking_reference, status) VALUES
(1, 1, 2, 'BKG001', 'confirmed'),
(2, 2, 8, 'BKG002', 'confirmed'),
(3, 3, 11, 'BKG003', 'confirmed'),
(4, 4, 17, 'BKG004', 'confirmed'),
(5, 5, 23, 'BKG005', 'confirmed'),
(6, 6, 26, 'BKG006', 'confirmed'),
(7, 7, 33, 'BKG007', 'confirmed'),
(8, 8, 37, 'BKG008', 'confirmed'),
(9, 9, 41, 'BKG009', 'confirmed'),
(10, 10, 48, 'BKG010', 'confirmed'),
(11, 11, 52, 'BKG011', 'confirmed'),
(12, 12, 58, 'BKG012', 'confirmed'),
(13, 13, 61, 'BKG013', 'confirmed'),
(14, 14, 68, 'BKG014', 'confirmed'),
(15, 15, 72, 'BKG015', 'confirmed'),

(16, 16, 78, 'BKG016', 'confirmed'),
(17, 17, 81, 'BKG017', 'confirmed'),
(18, 18, 88, 'BKG018', 'confirmed'),
(19, 19, 92, 'BKG019', 'confirmed'),
(20, 20, 96, 'BKG020', 'confirmed');





INSERT INTO payments (booking_id, amount, payment_method, status, transaction_id)
VALUES
(1, 1500.00, 'upi', 'success', 'TXN1001'),
(2, 1400.00, 'card', 'success', 'TXN1002'),
(3, 800.00, 'wallet', 'success', 'TXN1003'),
(4, 1200.00, 'netbanking', 'success', 'TXN1004'),
(5, 900.00, 'upi', 'success', 'TXN1005'),
(6, 4500.00, 'card', 'success', 'TXN1006'),
(7, 4000.00, 'upi', 'success', 'TXN1007'),
(8, 3500.00, 'wallet', 'success', 'TXN1008'),
(9, 4200.00, 'netbanking', 'success', 'TXN1009'),
(10, 3800.00, 'card', 'success', 'TXN1010'),
(11, 2000.00, 'upi', 'success', 'TXN1011'),
(12, 1000.00, 'wallet', 'success', 'TXN1012'),
(13, 500.00, 'upi', 'success', 'TXN1013'),
(14, 700.00, 'netbanking', 'success', 'TXN1014'),
(15, 1100.00, 'card', 'success', 'TXN1015'),
(16, 1300.00, 'upi', 'success', 'TXN1016'),
(17, 4100.00, 'card', 'success', 'TXN1017'),
(18, 2200.00, 'wallet', 'success', 'TXN1018'),
(19, 1600.00, 'netbanking', 'success', 'TXN1019'),
(20, 900.00, 'upi', 'success', 'TXN1020');


---Train---
INSERT INTO routes (from_location, to_location, distance)
SELECT 
    c1.city,
    c2.city,
    (500 + FLOOR(RANDOM()*1500))::int
FROM 
    (VALUES 
        ('Mumbai'),('Delhi'),('Bangalore'),('Chennai'),
        ('Kolkata'),('Hyderabad'),('Pune'),('Ahmedabad'),
        ('Jaipur'),('Goa')
    ) AS c1(city),
    (VALUES 
        ('Mumbai'),('Delhi'),('Bangalore'),('Chennai'),
        ('Kolkata'),('Hyderabad'),('Pune'),('Ahmedabad'),
        ('Jaipur'),('Goa')
    ) AS c2(city)
WHERE c1.city <> c2.city
AND NOT EXISTS (
    SELECT 1 FROM routes r 
    WHERE r.from_location = c1.city 
    AND r.to_location = c2.city
);

INSERT INTO vehicles (type, name, number_code)
SELECT 
    'train',
    r.from_location || '-' || r.to_location || ' Express',
    'TR' || (3000 + ROW_NUMBER() OVER())
FROM routes r
WHERE NOT EXISTS (
    SELECT 1 FROM vehicles v 
    WHERE v.name = r.from_location || '-' || r.to_location || ' Express'
);

INSERT INTO trips (vehicle_id, route_id, departure_time, arrival_time, price)
SELECT 
    v.vehicle_id,
    r.route_id,
    TIMESTAMP '2026-04-01' + (d.day || ' days')::interval + (h.hour || ' hours')::interval,
    TIMESTAMP '2026-04-01' + (d.day || ' days')::interval + ((h.hour + 10) || ' hours')::interval,
    800 + (r.distance * 0.8)
FROM routes r
JOIN vehicles v 
    ON v.name LIKE r.from_location || '-' || r.to_location || '%'
CROSS JOIN generate_series(0,29) AS d(day)
CROSS JOIN generate_series(6,18,6) AS h(hour)
LIMIT 300;

-----


---flight

INSERT INTO routes (from_location, to_location, distance)
SELECT 
    a1.code,
    a2.code,
    (800 + FLOOR(RANDOM()*2000))::int
FROM 
    (VALUES 
        ('BOM'),('DEL'),('BLR'),('MAA'),
        ('CCU'),('HYD'),('PNQ'),('AMD'),
        ('JAI'),('GOI')
    ) AS a1(code),
    (VALUES 
        ('BOM'),('DEL'),('BLR'),('MAA'),
        ('CCU'),('HYD'),('PNQ'),('AMD'),
        ('JAI'),('GOI')
    ) AS a2(code)
WHERE a1.code <> a2.code
AND NOT EXISTS (
    SELECT 1 FROM routes r 
    WHERE r.from_location = a1.code 
    AND r.to_location = a2.code
);


INSERT INTO vehicles (type, name, number_code)
SELECT 
    'flight',
    airline || ' ' || r.from_location || r.to_location,
    'FL' || (7000 + ROW_NUMBER() OVER())
FROM routes r,
(VALUES ('AI'),('6E'),('SG'),('UK')) AS a(airline)
WHERE r.from_location ~ '^[A-Z]{3}$';

INSERT INTO trips (vehicle_id, route_id, departure_time, arrival_time, price)
SELECT 
    v.vehicle_id,
    r.route_id,
    TIMESTAMP '2026-04-01' 
        + (d.day || ' days')::interval 
        + (h.hour || ' hours')::interval,

    TIMESTAMP '2026-04-01' 
        + (d.day || ' days')::interval 
        + ((h.hour + 2) || ' hours')::interval,

    3000 + (r.distance * 1.5)

FROM routes r
JOIN vehicles v 
    ON v.name LIKE '%' || r.from_location || r.to_location

CROSS JOIN generate_series(0,29) AS d(day)
CROSS JOIN generate_series(5,23,3) AS h(hour)

LIMIT 300;

----

---ship

INSERT INTO routes (from_location, to_location, distance)
SELECT 
    p1.port,
    p2.port,
    (300 + FLOOR(RANDOM()*1200))::int
FROM 
    (VALUES 
        ('Mumbai Port'),('Chennai Port'),('Kochi Port'),
        ('Goa Port'),('Kolkata Port'),('Port Blair'),
        ('Visakhapatnam Port'),('Mangalore Port')
    ) AS p1(port),
    (VALUES 
        ('Mumbai Port'),('Chennai Port'),('Kochi Port'),
        ('Goa Port'),('Kolkata Port'),('Port Blair'),
        ('Visakhapatnam Port'),('Mangalore Port')
    ) AS p2(port)
WHERE p1.port <> p2.port
AND NOT EXISTS (
    SELECT 1 FROM routes r 
    WHERE r.from_location = p1.port 
    AND r.to_location = p2.port
);

INSERT INTO vehicles (type, name, number_code)
VALUES
('ship','Arabian Sea Voyager','SH8001'),
('ship','Bay of Bengal Queen','SH8002'),
('ship','Indian Ocean Explorer','SH8003'),
('ship','Coastal Paradise','SH8004'),
('ship','Island Hopper','SH8005'),
('ship','Sunset Cruiser','SH8006'),
('ship','Blue Horizon','SH8007'),
('ship','Coral Queen','SH8008'),
('ship','Ocean Majesty','SH8009'),
('ship','Sea Breeze','SH8010');


INSERT INTO trips (vehicle_id, route_id, departure_time, arrival_time, price)
SELECT 
    v.vehicle_id,
    r.route_id,

    TIMESTAMP '2026-04-01' 
        + (d.day || ' days')::interval 
        + (h.hour || ' hours')::interval,

    TIMESTAMP '2026-04-01' 
        + (d.day || ' days')::interval 
        + ((h.hour + 18) || ' hours')::interval,

    2000 + (r.distance * 1.2)

FROM routes r
JOIN vehicles v 
    ON v.type = 'ship'

CROSS JOIN generate_series(0,29) AS d(day)
CROSS JOIN generate_series(6,18,12) AS h(hour)

LIMIT 200;




INSERT INTO seats (trip_id, seat_number, status)
SELECT 
    t.trip_id,
    s.seat_no,
    CASE 
        WHEN RANDOM() < 0.2 THEN 'booked'
        ELSE 'available'
    END
FROM trips t
JOIN vehicles v ON t.vehicle_id = v.vehicle_id

JOIN LATERAL (
    SELECT generate_series(
        1,
        CASE 
            WHEN v.type = 'train' THEN 50
            WHEN v.type = 'flight' THEN 120
            WHEN v.type = 'ship' THEN 80
        END
    ) AS seat_no
) s ON TRUE

WHERE NOT EXISTS (
    SELECT 1 FROM seats s2
    WHERE s2.trip_id = t.trip_id
    AND s2.seat_number = s.seat_no
);





------------------------------------------------



