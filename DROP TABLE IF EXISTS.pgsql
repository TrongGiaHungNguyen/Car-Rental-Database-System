DROP TABLE IF EXISTS 
    DRIVE,
    LIVE,
    REVIEW,
    RENT,
    DRIVER,
    MODEL,
    CAR,
    CREDIT_CARD,
    ADDRESS,
    CLIENT,
    MANAGER
CASCADE;

CREATE TABLE MANAGER (
    manager_name VARCHAR(255) NOT NULL,
    ssn CHAR(11) PRIMARY KEY NOT NULL,
    manager_email VARCHAR(255) NOT NULL
);

CREATE TABLE CLIENT (
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255) PRIMARY KEY NOT NULL
);

CREATE TABLE ADDRESS (
    road_name VARCHAR(255) NOT NULL,
    address_number INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    PRIMARY KEY(road_name, address_number, city)
);

CREATE TABLE CREDIT_CARD (
    credit_card_number VARCHAR(20) PRIMARY KEY NOT NULL,
    client_email VARCHAR(255) NOT NULL,
    road_name VARCHAR(255) NOT NULL,
    address_number INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    FOREIGN KEY (road_name, address_number, city) REFERENCES ADDRESS(road_name, address_number, city),
    FOREIGN KEY (client_email) REFERENCES CLIENT(client_email)
);

CREATE TABLE CAR (
    brand VARCHAR(255) NOT NULL,
    car_id INT PRIMARY KEY NOT NULL
);

CREATE TABLE MODEL (
    color VARCHAR(255) NOT NULL,
    construction_year INT NOT NULL,
    transmission_type VARCHAR(255) NOT NULL,
    model_id INT NOT NULL,
    car_id INT NOT NULL,
    PRIMARY KEY (model_id, car_id),
    FOREIGN KEY (car_id) REFERENCES CAR(car_id)
);  

CREATE TABLE DRIVER (
    driver_name VARCHAR(255) PRIMARY KEY NOT NULL,
    road_name VARCHAR(255) NOT NULL,
    address_number INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    FOREIGN KEY (road_name, address_number, city) REFERENCES ADDRESS(road_name, address_number, city)
);

CREATE TABLE RENT (
    rent_id INT PRIMARY KEY NOT NULL,
    rent_date DATE NOT NULL,
    client_email VARCHAR(255) NOT NULL,
    model_id INT NOT NULL,
    car_id INT NOT NULL,
    driver_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (client_email) REFERENCES CLIENT(client_email),
    FOREIGN KEY (model_id, car_id) REFERENCES MODEL(model_id, car_id),
    FOREIGN KEY (driver_name) REFERENCES DRIVER(driver_name)
);

CREATE TABLE REVIEW (
    review_message TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    review_id INT NOT NULL,
    driver_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255) NOT NULL,
    PRIMARY KEY (review_id, driver_name),
    FOREIGN KEY (driver_name) REFERENCES DRIVER(driver_name),
    FOREIGN KEY (client_email) REFERENCES CLIENT(client_email)
);

CREATE TABLE LIVE (
    client_email VARCHAR(255) NOT NULL,
    road_name VARCHAR(255) NOT NULL,
    address_number INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    PRIMARY KEY (client_email, road_name, address_number, city),
    FOREIGN KEY (client_email) REFERENCES CLIENT(client_email),
    FOREIGN KEY (road_name, address_number, city) REFERENCES ADDRESS(road_name, address_number, city)
);

CREATE TABLE DRIVE (
    model_id INT NOT NULL,
    car_id INT NOT NULL,
    driver_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (model_id, car_id, driver_name),
    FOREIGN KEY (model_id, car_id) REFERENCES MODEL(model_id, car_id),
    FOREIGN KEY (driver_name) REFERENCES DRIVER(driver_name)
);

-- Address
INSERT INTO ADDRESS (address_number, road_name, city) VALUES (1, 'Morning St', 'Chicago');
INSERT INTO ADDRESS (address_number, road_name, city) VALUES (2, 'Noon St', 'Chicago');
INSERT INTO ADDRESS (address_number, road_name, city) VALUES (3, 'Afternoon St', 'Chicago');
INSERT INTO ADDRESS (address_number, road_name, city) VALUES (4, 'Evening St', 'Chicago');

-- Manager
INSERT INTO MANAGER (manager_name, ssn, manager_email) VALUES ('Manager1', '111-11-1111', 'manager1@gmail.com');

-- Car
INSERT INTO CAR (car_id, brand) VALUES (1, 'Honda');
INSERT INTO CAR (car_id, brand) VALUES (2, 'Toyota');
INSERT INTO CAR (car_id, brand) VALUES (3, 'Kia');
INSERT INTO CAR (car_id, brand) VALUES (4, 'Tesla');

-- Model 
INSERT INTO MODEL (model_id, car_id, color, construction_year, transmission_type) VALUES (1, 1, 'red', 2023, 'auto');
INSERT INTO MODEL (model_id, car_id, color, construction_year, transmission_type) VALUES (2, 2, 'blue', 2024, 'auto');
INSERT INTO MODEL (model_id, car_id, color, construction_year, transmission_type) VALUES (3, 3, 'green', 2025, 'auto');

-- Driver
INSERT INTO DRIVER (driver_name, address_number, road_name, city) VALUES ('Driver1', '1', 'Morning St', 'Chicago');
INSERT INTO DRIVER (driver_name, address_number, road_name, city) VALUES ('Driver2', '2', 'Noon St', 'Chicago');

-- Drive
INSERT INTO DRIVE (driver_name, car_id, model_id) VALUES ('Driver1', 1, 1);
-- INSERT INTO DRIVE (driver_name, car_id, model_id) VALUES ('Driver2', 2, 2);

-- Client
INSERT INTO CLIENT (client_name, client_email) VALUES ('Client1', 'client1@gmail.com');
INSERT INTO CLIENT (client_name, client_email) VALUES ('Client2', 'client2@gmail.com');

-- Live
INSERT INTO LIVE (client_email, address_number, road_name, city) VALUES ('client1@gmail.com', 1, 'Morning St', 'Chicago');
INSERT INTO LIVE (client_email, address_number, road_name, city) VALUES ('client2@gmail.com', 1, 'Morning St', 'Chicago');

-- Rent
INSERT INTO RENT (rent_id, client_email, rent_date, driver_name, car_id, model_id) VALUES (1, 'client1@gmail.com', '2025-01-01', 'Driver1', 1, 1);
INSERT INTO RENT (rent_id, client_email, rent_date, driver_name, car_id, model_id) VALUES (2, 'client1@gmail.com', '2025-01-01', 'Driver1', 1, 1);

-- Rating
INSERT INTO REVIEW (review_id, client_email, driver_name, rating, review_message) VALUES (1, 'client1@gmail.com', 'Driver1', 5, 'Good');
INSERT INTO REVIEW (review_id, client_email, driver_name, rating, review_message) VALUES (2, 'client1@gmail.com', 'Driver1', 1, 'Bad');

