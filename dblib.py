"""dblib - Bibliothek für Datenbankzugriff

    Bibliothek mit 5 einfach zu nutzenden Funktionen zum Arbeiten
    mit einer MySQL/Mariadb Datenkank

    Einordnung:			FISI-LF5-LS3
    Aufgabe: 			

    Name:			    Markus Breuer
    Organisaion:		BK-GuT

    Erstellt:			14.04.2020
    Letzte Änderung:	31.12.2020     
    """

import mysql.connector


def dbVerbindungAufbauen(host, user, passwd, db):
    """ Funktion zum Verbindungsaufbau mit einer MySQL-Datenbank """
    verbindung = mysql.connector.connect(
        host=host, port=3306, user=user, passwd=passwd, db=db
    )
    return verbindung


def dbVerbindungAbbauen(verbindung):
    """ Funktion zum Verbindungsabbau bei einer MySQL-Datenbank """
    verbindung.close()


def dbNichtAbfrageAnweisung(verbindung, anweisung):
    """ Funktion zur Ausführung einer Nicht-Abfrage-Anweisung bei MySQL-Datenbank """
    cursor = verbindung.cursor()  # Cursor öffnen
    cursor.execute(anweisung)  # Anweisung ausführen
    cursor.close()  # Cursor schliessen
    verbindung.commit()  # Bestättigen


def dbAbfrageAnweisung(verbindung, anweisung):
    """ Funktion zur Ausführung einer Nicht-Abfrage-Anweisung bei MySQL-Datenbank """
    verbindung.commit()  # Offene Aktionen bestättigen;
    cursor = verbindung.cursor()  # Cursor öffnen
    cursor.execute(anweisung)  # Anweisung ausführen
    ergebnisMenge = cursor.fetchall()  # Ergebnismenge abholen
    cursor.close()  # Cursor schliessen
    return ergebnisMenge
