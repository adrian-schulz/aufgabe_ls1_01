""" Nutzungsdatensystem für LS1 - Stammdaten

    Nutzungsdatensystem für LS1 - Stammdaten - Ausgangsversion
 
    Einordnung:         FISI-LF8-LS1-Nutzungsdatensystem

    Name:               Markus Breuer
    Organisaion:        BK-GuT

    Erstellt:           24.05.2021
    Letzte Änderung:    
    """

import random
import datetime
import dblib
import os
import pandas as pd

# Klasse nds_stammdaten #######################################################


class nds_stammdaten:
    def __init__(self):
        """ Konstruktor der Klasse Stammdaten """
        self.tabellenname = ""
        self.host = ""
        self.user = ""
        self.passwd = ""
        self.db = ""
        self.df = None
        self.setze_db_verbindungsparameter()

    def setze_tabellenname(self, tabellenname):
        self.tabellenname = tabellenname

    def setze_db_verbindungsparameter(self):
        self.host = "localhost"
        self.user = "root"
        self.passwd = ""
        self.db = "ndsdb"

    def loeschen(self):
        """ loeschen einer Stammdatentabelle """
        print(
            "--> Löschen aller Einträge der Stammdatentabelle:", self.tabellenname, "\n"
        )
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        sqlStatement = "DELETE FROM " + self.tabellenname
        dblib.dbNichtAbfrageAnweisung(connection, sqlStatement)
        dblib.dbVerbindungAbbauen(connection)

    def importieren(self):
        """ Importieren einer Stammdatentabelle """
        print("--> Importieren in Stammdatentabelle:", self.tabellenname, "\n")
        self.loeschen()
        print("--> Neueintragungen vornehmen", "\n")
        self.einlesen_daten()
        self.bereinigen_daten()
        self.ergaenze_fremdschluesel()
        self.speichern_daten()

    def einlesen_daten(self):
        """ Einlesen einer Stammdatendatei """
        dateiname = "daten_ls1_" + self.tabellenname + ".csv"
        # keine Datei vorhanden -> leere Liste
        if os.path.isfile(dateiname) != True:
            return []
        # Dataframe aufbauen
        self.df = pd.read_csv(dateiname, header=None)
        self.df.columns = self.bestimme_spaltenliste()
        return

    def bereinigen_daten(self):
        """ Bereinigen der Stammdaten """

        # Zeilen mit fehlenden Einträgen löschen
        zeilen_vorher = len(self.df.index)
        self.df.dropna(inplace=True)
        zeilen_nachher = len(self.df.index)
        if zeilen_nachher < zeilen_vorher:
            print(
                "!!! Unvollständige Zeilen gelöscht:",
                zeilen_vorher - zeilen_nachher,
                "\n",
            )

    def ergaenze_fremdschluesel(self):
        pass

    def speichern_daten(self):
        """ Speichern in einer Stammdatentabelle """
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        for i in self.df.index:
            liste_werte = list(self.df.loc[i])
            sqlStatement = self.bestimme_insert_statement(liste_werte)
            dblib.dbNichtAbfrageAnweisung(connection, sqlStatement)
        dblib.dbVerbindungAbbauen(connection)

    def bestimme_spaltenliste(self):
        pass

    def bestimme_insert_statement(self, liste_werte):
        pass

    def statistik(self):
        """ Statistik Stammdaten """
        print("Statistik Stammdaten")  
        print("--------------------")

        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )

        result = dblib.dbAbfrageAnweisung(connection, "SELECT COUNT(*) FROM benutzer")
        anzahl_benutzer = int(result[0][0])
        print("Anzahl Benutzer:", anzahl_benutzer)

        result = dblib.dbAbfrageAnweisung(connection, "SELECT COUNT(*) FROM rechner")
        anzahl_rechner = int(result[0][0])
        print("Anzahl Rechner:", anzahl_rechner)

        result = dblib.dbAbfrageAnweisung(
            connection, "SELECT COUNT(*) FROM anwendungen"
        )
        anzahl_anwendungen = int(result[0][0])
        print("Anzahl Anwendungen:", anzahl_anwendungen)

        result = dblib.dbAbfrageAnweisung(
            connection, "SELECT COUNT(*) FROM anwendungskategorien"
        )
        anzahl_anwendungskategorien = int(result[0][0])
        print("Anzahl Anwendungskategorien:", anzahl_anwendungskategorien)

        result = dblib.dbAbfrageAnweisung(
            connection, "SELECT COUNT(*) FROM rechnerkategorien"
        )
        anzahl_rechnerkategorien = int(result[0][0])
        print("Anzahl Rechnerkategorien:", anzahl_rechnerkategorien)

        print("")
        dblib.dbVerbindungAbbauen(connection)


# Klasse nds_benutzer #########################################################


class nds_benutzer(nds_stammdaten):
    def __init__(self):
        """ Konstruktor der Klasse Benutzer """
        nds_stammdaten.__init__(self)
        self.setze_tabellenname("benutzer")

    def bestimme_spaltenliste(self):
        return ["Nr", "Benutzername", "Nachname", "Vorname"]

    def bestimme_insert_statement(self, liste_werte):
        return (
            "INSERT INTO benutzer ( benutzername, nachname, vorname) VALUES ( '"
            + str(liste_werte[1])
            + "','"
            + str(liste_werte[2])
            + "','"
            + str(liste_werte[3])
            + "')"
        )


# Klasse nds_rechner ##########################################################


class nds_rechner(nds_stammdaten):
    def __init__(self):
        """ Konstruktor der Klasse Rechner """
        nds_stammdaten.__init__(self)
        self.tabellenname = "rechner"

    def bestimme_spaltenliste(self):
        return ["Rechner", "Kategorie"]

    def bestimme_insert_statement(self, liste_werte):
        return (
            "INSERT INTO rechner ( rechnername) VALUES ( '" + str(liste_werte[0]) + "')"
        )


# Klasse nds_rechner_kategorien ##########################################################


class nds_rechnerkategorien(nds_stammdaten):
    def __init__(self):
        """ Konstruktor der Klasse Rechner """
        nds_stammdaten.__init__(self)
        self.tabellenname = "rechnerkategorien"

    def bestimme_spaltenliste(self):
        return ["Kategorie"]

    def bestimme_insert_statement(self, liste_werte):
        return (
            "INSERT INTO rechnerkategorien ( rechnerkategoriename) VALUES ( '" + str(liste_werte[0]) + "')"
        )


# Klasse nds_anwendungen ######################################################


class nds_anwendungen(nds_stammdaten):
    def __init__(self):
        """ Konstruktor der Klasse Anwendungen """
        nds_stammdaten.__init__(self)
        self.tabellenname = "anwendungen"
        self.fkdf_anwendungskategorien = None

    def bestimme_spaltenliste(self):
        return ["Anwendung", "Kategorie"]

    def bestimme_insert_statement(self, liste_werte):
        return (
            "INSERT INTO anwendungen ( anwendungsname, anwendungskategorieID) VALUES ( '"
            + str(liste_werte[0]) 
            + "','" 
            + str(liste_werte[2])
            + "')" 
        )

    def ergaenze_fremdschluesel(self):
        # Dataframe mit Anwendungskategorien für Fremdschlüssel laden
        if( self.fkdf_anwendungskategorien == None):
            connection = dblib.dbVerbindungAufbauen(
                self.host, self.user, self.passwd, self.db
            )
            self.fkdf_anwendungskategorien = pd.read_sql("SELECT * FROM anwendungskategorien", connection)
            self.fkdf_anwendungskategorien.columns = ["KategorieID","Kategorie" ]
            dblib.dbVerbindungAbbauen(connection)
            # Fremdschlüssel dazumergen
        self.df = pd.merge(self.df, self.fkdf_anwendungskategorien, on="Kategorie", how="left")
        # Zeilen mit fehlenden Einträgen löschen
        zeilen_vorher = len(self.df.index)
        self.df.dropna(inplace=True)
        zeilen_nachher = len(self.df.index)
        if zeilen_nachher < zeilen_vorher:
            print(
                "!!! Zeilen mit fehlenden Fremdschlüsseln gelöscht:",
                zeilen_vorher - zeilen_nachher,
                "\n",
            )


# Klasse nds_anwendungenskategorien ###########################################


class nds_anwendungskategorien(nds_stammdaten):
    def __init__(self):
        """ Konstruktor der Klasse Anwendungen """
        nds_stammdaten.__init__(self)
        self.tabellenname = "anwendungskategorien"

    def bestimme_spaltenliste(self):
        return ["Kategorie"]

    def bestimme_insert_statement(self, liste_werte):
        return (
            "INSERT INTO anwendungskategorien ( anwendungskategoriename) VALUES ( '"
            + str(liste_werte[0])
            + "')"
        )
