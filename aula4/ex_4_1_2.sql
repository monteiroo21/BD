CREATE DATABASE FLIGHTSRESERVATIONS;
GO
USE FLIGHTSRESERVATIONS;
GO

CREATE TABLE Airport (
    code        VARCHAR NOT NULL,           
    [name]      VARCHAR NOT NULL,       
    city        VARCHAR NOT NULL,           
    [state]       VARCHAR,      

    PRIMARY KEY(code)
);

CREATE TABLE AirplaneType (
    [type_name]      VARCHAR NOT NULL,
    capacity       INT NOT NULL,
    company   VARCHAR NOT NULL,

    PRIMARY KEY([type_name])
);

CREATE TABLE CanLand (
    code_airport    VARCHAR NOT NULL,
    airplane_type_name VARCHAR NOT NULL,

	FOREIGN KEY(airplane_type_name) REFERENCES AirplaneType([type_name]),
	FOREIGN KEY(code_airport) REFERENCES Airport(code),
    PRIMARY KEY(code_airport, airplane_type_name),
);

CREATE TABLE Airplane (
    [id]            INT NOT NULL,
    [type_name]       VARCHAR NOT NULL,
    total_seats    INT NOT NULL,

    PRIMARY KEY([id]),
    FOREIGN KEY([type_name]) REFERENCES AirplaneType([type_name])
);

CREATE TABLE Flight (
    [number]        INT NOT NULL,
    airline         VARCHAR NOT NULL,
    weekdays        VARCHAR NOT NULL,

    PRIMARY KEY([number])
);

CREATE TABLE Fare (
    fare_code       INT NOT NULL,
    amount          INT NOT NULL,
    restrictions    VARCHAR,
    flight_number   INT NOT NULL,

    PRIMARY KEY(fare_code, flight_number),
    FOREIGN KEY(flight_number) REFERENCES Flight([number])
);

CREATE TABLE FlightLeg (
    flight_leg_no   INT NOT NULL,
    flight_number   INT NOT NULL,
    scheduled_departure_time DATETIME NOT NULL,
    scheduled_arrival_time DATETIME NOT NULL,
    airport_code VARCHAR NOT NULL,

    PRIMARY KEY(flight_leg_no, flight_number),
    FOREIGN KEY(flight_number) REFERENCES Flight([number]),
    FOREIGN KEY(airport_code) REFERENCES Airport(code)
);

CREATE TABLE LegInstance (
    flight_leg_num       INT NOT NULL,
    flight_number       INT NOT NULL,
    leg_instance_data   DATETIME NOT NULL,
    airplane_id         INT NOT NULL,
    airport_code        VARCHAR NOT NULL,
    no_of_seats         INT NOT NULL,
    dep_time    DATETIME NOT NULL,
    arr_time    DATETIME NOT NULL,

	PRIMARY KEY(flight_leg_num, flight_number, leg_instance_data),
	FOREIGN KEY(flight_leg_num, flight_number) REFERENCES FlightLeg(flight_leg_no, flight_number),
    FOREIGN KEY(airplane_id) REFERENCES Airplane([id]),
    FOREIGN KEY(airport_code) REFERENCES Airport(code)
);

CREATE TABLE Seat (
    seat_no         INT NOT NULL,
    customer_name   VARCHAR,
    cphone          VARCHAR,
    leg_instance_data DATETIME NOT NULL,
    flight_leg_num   INT NOT NULL,
    flight_number   INT NOT NULL,

	FOREIGN KEY(flight_leg_num, flight_number, leg_instance_data) REFERENCES LegInstance(flight_leg_num, flight_number, leg_instance_data),
    PRIMARY KEY(seat_no, leg_instance_data, flight_leg_num, flight_number)
);