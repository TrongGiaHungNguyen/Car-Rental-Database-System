CREATE TABLE MANAGER (
    manager_name VARCHAR(255) NOT NULL,
    SSN CHAR(11) PRIMARY KEY NOT NULL,
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
    PRIMARY KEY (road_name, address_number, city)
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

CREATE TABLE CREDIT_CARD (
    credit_card_number INT PRIMARY KEY NOT NULL,
    client_email VARCHAR(255) REFERENCES CLIENT(client_email) NOT NULL,
    road_name VARCHAR(255) NOT NULL,
    address_number INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    FOREIGN KEY (road_name, address_number, city) REFERENCES ADDRESS(road_name, address_number, city)
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
    car_id INT REFERENCES CAR(car_id) NOT NULL,
    PRIMARY KEY (model_id, car_id)
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
    client_email VARCHAR(255) REFERENCES CLIENT(client_email) NOT NULL,
    model_id INT REFERENCES MODEL(model_id) NOT NULL,
    driver_name VARCHAR(255) REFERENCES DRIVER(driver_name) NOT NULL
);

CREATE TABLE NM_DRIVER_MODEL (
    model_id INT REFERENCES MODEL(model_id) NOT NULL,
    driver_name VARCHAR(255) REFERENCES DRIVER(driver_name) NOT NULL,
    PRIMARY KEY (model_id, driver_name)
);

CREATE TABLE REVIEW (
    review_message TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    review_id INT NOT NULL,
    driver_name VARCHAR(255) REFERENCES DRIVER(driver_name) NOT NULL,
    client_email VARCHAR(255) REFERENCES CLIENT(client_email) NOT NULL,
    PRIMARY KEY (review_id, driver_name)
);

-- INSERT INTO MANAGER VALUES ('Jim', '111-11-1111', 'abc@gmail.com')