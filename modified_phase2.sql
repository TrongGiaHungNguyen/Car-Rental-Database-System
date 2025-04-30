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
    FOREIGN KEY (road_name, address_number, city) REFERENCES ADDRESS(road_name, address_number, city)
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

CREATE TABLE NM_CLIENT_ADDRESS (
    client_email VARCHAR(255) NOT NULL,
    road_name VARCHAR(255) NOT NULL,
    address_number INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    PRIMARY KEY (client_email, road_name, address_number, city),
    FOREIGN KEY (client_email) REFERENCES CLIENT(client_email),
    FOREIGN KEY (road_name, address_number, city) REFERENCES ADDRESS(road_name, address_number, city)
);

CREATE TABLE NM_MODEL_DRIVER (
    model_id INT NOT NULL,
    car_id INT NOT NULL,
    driver_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (model_id, car_id, driver_name),
    FOREIGN KEY (model_id, car_id) REFERENCES MODEL(model_id, car_id),
    FOREIGN KEY (driver_name) REFERENCES DRIVER(driver_name)
);