--
-- File generated with SQLiteStudio v3.1.1 on Thu Jun 14 16:48:25 2018
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: concept
DROP TABLE IF EXISTS concept;

CREATE TABLE concept (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT    NOT NULL
                        UNIQUE,
    status      BOOLEAN DEFAULT (1) 
);

INSERT INTO concept (id, description, status) VALUES (1, 'Mantenimiento Enero', 1);
INSERT INTO concept (id, description, status) VALUES (2, 'Mantenimiento Febrero', 1);
INSERT INTO concept (id, description, status) VALUES (3, 'Mantenimiento Marzo', 1);
INSERT INTO concept (id, description, status) VALUES (4, 'Mantenimiento Abril', 1);
INSERT INTO concept (id, description, status) VALUES (5, 'Mantenimiento Mayo', 1);
INSERT INTO concept (id, description, status) VALUES (6, 'Mantenimiento Junio', 1);
INSERT INTO concept (id, description, status) VALUES (7, 'Mantenimiento Julio', 1);
INSERT INTO concept (id, description, status) VALUES (8, 'Mantenimiento Agosto', 1);
INSERT INTO concept (id, description, status) VALUES (9, 'Mantenimiento Setiembre', 1);
INSERT INTO concept (id, description, status) VALUES (10, 'Mantenimiento Octubre', 1);
INSERT INTO concept (id, description, status) VALUES (11, 'Mantenimiento Noviembre', 1);
INSERT INTO concept (id, description, status) VALUES (12, 'Mantenimiento Diciembre', 1);
INSERT INTO concept (id, description, status) VALUES (13, 'Cuota mantenimiento', 1);

-- Table: owner
DROP TABLE IF EXISTS owner;

CREATE TABLE owner (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id   INTEGER REFERENCES person (id),
    property_id INTEGER REFERENCES property (id) 
);

INSERT INTO owner (id, person_id, property_id) VALUES (1, 1, 12);
INSERT INTO owner (id, person_id, property_id) VALUES (2, 2, 12);
INSERT INTO owner (id, person_id, property_id) VALUES (3, 3, 13);
INSERT INTO owner (id, person_id, property_id) VALUES (4, 4, 11);
INSERT INTO owner (id, person_id, property_id) VALUES (5, 5, 1);
INSERT INTO owner (id, person_id, property_id) VALUES (6, 6, 2);
INSERT INTO owner (id, person_id, property_id) VALUES (7, 7, 6);
INSERT INTO owner (id, person_id, property_id) VALUES (8, 8, 7);
INSERT INTO owner (id, person_id, property_id) VALUES (9, 9, 3);
INSERT INTO owner (id, person_id, property_id) VALUES (10, 10, 8);
INSERT INTO owner (id, person_id, property_id) VALUES (11, 11, 4);
INSERT INTO owner (id, person_id, property_id) VALUES (12, 12, 5);
INSERT INTO owner (id, person_id, property_id) VALUES (13, 13, 9);
INSERT INTO owner (id, person_id, property_id) VALUES (14, 14, 10);
INSERT INTO owner (id, person_id, property_id) VALUES (15, 16, 14);
INSERT INTO owner (id, person_id, property_id) VALUES (16, 15, 15);

-- Table: person
DROP TABLE IF EXISTS person;

CREATE TABLE person (
    id          INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL,
    last_name   TEXT    NOT NULL,
    first_name  TEXT    NOT NULL,
    id_document TEXT    UNIQUE
);

INSERT INTO person (id, last_name, first_name, id_document) VALUES (1, 'Olivas', 'Johnny', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (2, 'Abdel Hamid', 'Halima', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (3, 'Velarde', 'Hugo', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (4, 'Maldonado', 'Ruth', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (5, 'Abusada', 'Carlos', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (6, 'Tejada', 'Ivanna', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (7, 'Cerron', 'Alejandro', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (8, 'Anampa', 'Nancy', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (9, 'Ordoñez', 'Dwight', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (10, 'Rodriguez', 'Rosana', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (11, 'Ascencion', 'Oscar', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (12, 'Vasques', 'Carlos', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (13, 'Cardenas', 'Jose', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (14, 'Hidalgo', 'Darwin', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (15, 'Molina', 'Victor', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (16, 'Sardon', 'Alejandra', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (17, 'Rodriguez', 'Gustavo', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (18, 'Narrea', 'Ivonne', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (19, 'De La Rosa', 'Mylenn', NULL);
INSERT INTO person (id, last_name, first_name, id_document) VALUES (20, 'Pluck', 'Michelle', NULL);

-- Table: product
DROP TABLE IF EXISTS product;

CREATE TABLE product (
    id          INTEGER PRIMARY KEY,
    type        INTEGER,
    description TEXT    UNIQUE
                        NOT NULL,
    status      BOOLEAN DEFAULT (1) 
);


-- Table: property
DROP TABLE IF EXISTS property;

CREATE TABLE property (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT
                               NOT NULL,
    description        TEXT    NOT NULL,
    sunarp_certificate INTEGER,
    alias              TEXT
);

INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (1, 'Dpto. 101', NULL, 'D101');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (2, 'Dpto. 102', NULL, 'D102');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (3, 'Dpto. 103', NULL, 'D103');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (4, 'Dpto. 104', NULL, 'D104');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (5, 'Dpto. 105', NULL, 'D105');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (6, 'Dpto. 201', NULL, 'D201');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (7, 'Dpto. 202', NULL, 'D202');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (8, 'Dpto. 203', NULL, 'D203');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (9, 'Dpto. 204', NULL, 'D204');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (10, 'Dpto. 205', NULL, 'D205');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (11, 'Dpto. 301', NULL, 'D301');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (12, 'Dpto. 302', NULL, 'D302');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (13, 'Dpto. 303', NULL, 'D303');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (14, 'Dpto. 304', NULL, 'D304');
INSERT INTO property (id, description, sunarp_certificate, alias) VALUES (15, 'Dpto. 305', NULL, 'D305');

-- Table: provider
DROP TABLE IF EXISTS provider;

CREATE TABLE provider (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    type          INTEGER NOT NULL,
    name          TEXT    NOT NULL
                          UNIQUE,
    document      TEXT    UNIQUE
                          NOT NULL,
    register_date DATE    NOT NULL,
    status        BOOLEAN DEFAULT (1) 
);


-- Table: tenant
DROP TABLE IF EXISTS tenant;

CREATE TABLE tenant (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id   INTEGER REFERENCES person (id),
    property_id INTEGER REFERENCES property (id),
    status      CHAR    DEFAULT ('A') 
);

INSERT INTO tenant (id, person_id, property_id, status) VALUES (1, 20, 14, NULL);
INSERT INTO tenant (id, person_id, property_id, status) VALUES (2, 19, 3, NULL);
INSERT INTO tenant (id, person_id, property_id, status) VALUES (3, 18, 4, NULL);
INSERT INTO tenant (id, person_id, property_id, status) VALUES (4, 17, 7, NULL);

-- Table: user
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE
                     NOT NULL,
    password TEXT    NOT NULL
);


-- View: property_occupant
DROP VIEW IF EXISTS property_occupant;
CREATE VIEW property_occupant AS
    SELECT p.id AS occupant_id,
           first_name || ' ' || last_name AS occupant_name,
           pp.id AS property_id,
           pp.description AS property_description,
           pp.alias AS property_alias
      FROM owner o
           LEFT JOIN
           person p ON o.person_id = p.id
           LEFT JOIN
           property pp ON o.property_id = pp.id
    UNION
    SELECT p.id AS occupant_id,
           first_name || ' ' || last_name AS occupant_name,
           pp.id AS property_id,
           pp.description AS property_description,
           pp.alias AS property_alias
      FROM tenant t
           LEFT JOIN
           person p ON t.person_id = p.id
           LEFT JOIN
           property pp ON t.property_id = pp.id;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
