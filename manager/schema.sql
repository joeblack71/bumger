--
-- File generated with SQLiteStudio v3.1.1 on Sat Jun 9 22:19:18 2018
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


-- Table: expense
DROP TABLE IF EXISTS expense;

CREATE TABLE expense (
    id             INTEGER        PRIMARY KEY AUTOINCREMENT,
    provider_id    INTEGER        NOT NULL
                                  REFERENCES provider (id),
    receipt_number TEXT,
    product_id     INTEGER        NOT NULL
                                  REFERENCES product (id),
    quantity       INTEGER        NOT NULL,
    amount         DECIMAL (5, 2) NOT NULL,
    expense_date   DATE           NOT NULL
);


-- Table: owner
DROP TABLE IF EXISTS owner;

CREATE TABLE owner (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id   INTEGER REFERENCES person (id),
    property_id INTEGER REFERENCES property (id) 
);


-- Table: payment
DROP TABLE IF EXISTS payment;

CREATE TABLE payment (
    id           INTEGER        PRIMARY KEY AUTOINCREMENT,
    receipt_id   INTEGER        REFERENCES receipt (id) 
                                NOT NULL,
    amount       DECIMAL (5, 2) NOT NULL,
    payment_date DATE           NOT NULL
);


-- Table: payment_note
DROP TABLE IF EXISTS payment_note;

CREATE TABLE payment_note (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    text       VARCHAR (255) NOT NULL,
    payment_id INTEGER       REFERENCES payment (id) ON DELETE CASCADE
);


-- Table: person
DROP TABLE IF EXISTS person;

CREATE TABLE person (
    id          INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL,
    last_name   TEXT    NOT NULL,
    first_name  TEXT    NOT NULL,
    id_document TEXT    UNIQUE
);


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
    alias              TEXT    UNIQUE,
    sunarp_certificate INTEGER
);


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


-- Table: receipt
DROP TABLE IF EXISTS receipt;

CREATE TABLE receipt (
    id         INTEGER        PRIMARY KEY AUTOINCREMENT,
    number     TEXT           UNIQUE
                              NOT NULL,
    concept_id INTEGER        NOT NULL
                              REFERENCES concept (id),
    person_id  INTEGER        NOT NULL
                              REFERENCES person (id),
    amount     DECIMAL (5, 2) NOT NULL,
    issue_date DATE           NOT NULL,
    status     CHAR           DEFAULT P
);


-- Table: tenant
DROP TABLE IF EXISTS tenant;

CREATE TABLE tenant (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id   INTEGER REFERENCES person (id),
    property_id INTEGER REFERENCES property (id),
    status      CHAR    DEFAULT ('A') 
);


-- Table: user
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE
                     NOT NULL,
    password TEXT    NOT NULL
);


-- View: occupant
DROP VIEW IF EXISTS occupant;
CREATE VIEW occupant AS
    SELECT p.id,
           first_name || ' ' || last_name AS name,
           pp.description AS property,
           pp.alias AS prop_alias
      FROM owner o
           LEFT JOIN
           person p ON o.person_id = p.id
           LEFT JOIN
           property pp ON o.property_id = pp.id
    UNION
    SELECT p.id,
           first_name || ' ' || last_name AS name,
           pp.description AS property,
           pp.alias AS prop_alias
      FROM tenant t
           LEFT JOIN
           person p ON t.person_id = p.id
           LEFT JOIN
           property pp ON t.property_id = pp.id;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
