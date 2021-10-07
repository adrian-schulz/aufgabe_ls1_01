/*
 Das SQL-Skript erzeugt die Datenbank für das Nutzungsdaten-System.
 
 Einordnung:		FISI-LF8-LS1 - ndsdb - Ausgangsversion
 Aufgabe: 			aufgabe_ls1_01.sql
 
 Name:				Markus Breuer
 Organisaion:		BK-GuT
 
 Erstellt:			18.05.2021
 Letzte Änderung:	25.05.2021
 
 */
# Evtl. vorhandene Datenbank löschen und neue Datenbank anlegen
DROP DATABASE IF EXISTS ndsdb;

CREATE DATABASE ndsdb DEFAULT CHARACTER SET utf8;

USE ndsdb;

# Tabellen für Stammdaten anlegen
CREATE TABLE anwendungskategorien (
    anwendungskategorieID int(11) NOT NULL AUTO_INCREMENT,
    anwendungskategoriename VARCHAR(50) NOT NULL,
    PRIMARY KEY (anwendungskategorieID),
    UNIQUE KEY (anwendungskategoriename)
);

CREATE TABLE rechnerkategorien (
    rechnerkategorieID int(11) NOT NULL Auto_INCREMENT,
    rechnerkategoriename VARCHAR(50) NOT NULL,
    PRIMARY KEY (rechnerkategorieID),
    UNIQUE KEY (rechnerkategoriename)
);

CREATE TABLE anwendungen (
    anwendungsID int(11) NOT NULL AUTO_INCREMENT,
    anwendungsname VARCHAR(50) NOT NULL,
    anwendungskategorieID int(11) NOT NULL,
    PRIMARY KEY (anwendungsID),
    UNIQUE KEY (anwendungsname),
    FOREIGN KEY (anwendungskategorieID) REFERENCES anwendungskategorien (anwendungskategorieID)
);

CREATE TABLE benutzer (
    # Neue Tabelle  anlegen
    benutzerID int(11) NOT NULL AUTO_INCREMENT,
    benutzername VARCHAR(50) NOT NULL,
    nachname VARCHAR(50) NOT NULL,
    vorname VARCHAR(50) NOT NULL,
    PRIMARY KEY (benutzerID),
    UNIQUE KEY (benutzername)
);

CREATE TABLE rechner (
    rechnerID int(11) NOT NULL AUTO_INCREMENT,
    rechnername VARCHAR(50) NOT NULL,
    PRIMARY KEY (rechnerID),
    UNIQUE KEY (rechnername)
);

# Tabellen für Bewegungsdaten anlegen
CREATE TABLE rechnernutzungen (
    rechnernutzungsID int(11) NOT NULL AUTO_INCREMENT,
    rechnerID int(11) NOT NULL,
    benutzerID int(11) NOT NULL,
    anmeldezeit DATETIME NOT NULL,
    abmeldezeit DATETIME NULL NULL,
    PRIMARY KEY (rechnernutzungsID),
    FOREIGN KEY (rechnerID) REFERENCES rechner (rechnerID),
    FOREIGN KEY (benutzerID) REFERENCES benutzer (benutzerID)
);

CREATE TABLE anwendungsnutzungen (
    anwendungsnutzungsID int(11) NOT NULL AUTO_INCREMENT,
    anwendungsID int(11) NOT NULL,
    rechnernutzungsID int(11) NOT NULL,
    startzeit DATETIME NOT NULL,
    endzeit DATETIME NULL NULL,
    PRIMARY KEY (anwendungsnutzungsID),
    FOREIGN KEY (anwendungsID) REFERENCES anwendungen (anwendungsID),
    FOREIGN KEY (rechnernutzungsID) REFERENCES rechnernutzungen (rechnernutzungsID)
);

CREATE TABLE ndsimporte (
    importID int(11) NOT NULL AUTO_INCREMENT,
    importTag DATETIME DEFAULT NOW(),
    datenTag DATETIME NOT NULL,
    rdsOK int(11) DEFAULT 0,
    rdsVerworfen int(11) DEFAULT 0,
    adsOK int(11) DEFAULT 0,
    adsVerworfen int(11) DEFAULT 0,
    PRIMARY KEY (importID)
);