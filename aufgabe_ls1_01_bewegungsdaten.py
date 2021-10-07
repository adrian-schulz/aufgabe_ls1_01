""" Nutzungsdatensystem für LS1 - Bewegungsdaten

    Nutzungsdatensystem für LS1 - Bewegungsdaten - Ausgangsversion
 
    Einordnung:         FISI-LF8-LS1-Nutzungsdatensystem

    Name:               Markus Breuer
    Organisaion:        BK-GuT

    Erstellt:           25.05.2021
    Letzte Änderung:    10.06.2021
    """

import random
import datetime

from numpy import NaN
import dblib
import os
import pandas as pd

# Klasse nds_stammdaten #######################################################


class nds_bewegungsdaten:
    def __init__(self):
        """ Konstruktor der Klasse bewegungsdaten """
        self.tabellenname = ""
        self.host = ""
        self.user = ""
        self.passwd = ""
        self.db = ""
        self.df = None
        self.ds_ok = 0
        self.ds_verworfen = 0
        self.setze_db_verbindungsparameter()

    def setze_tabellenname(self, tabellenname):
        self.tabellenname = tabellenname

    def setze_db_verbindungsparameter(self):
        self.host = "localhost"
        self.user = "root"
        self.passwd = ""
        self.db = "ndsdb"

    def loeschen_alle(self):
        """ loeschen einer Bewegungsdatentabelle """
        print(
            "--> Löschen aller Einträge der Bewegungsdatentabelle:",
            self.tabellenname,
            "\n",
        )
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        sqlStatement = "DELETE FROM " + self.tabellenname
        dblib.dbNichtAbfrageAnweisung(connection, sqlStatement)
        dblib.dbVerbindungAbbauen(connection)

    def loeschen_tag(self, datum):
        """ loeschen einer Bewegungsdatentabelle """
        print(
            "--> Löschen Tageseinträge der Bewegungsdatentabelle:",
            self.tabellenname,
            datum.strftime("%d.%m.%Y"),
            "\n",
        )
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        sqlStatement = (
            "DELETE FROM " + self.tabellenname + self.bestimme_where_bedingung(datum)
        )
        dblib.dbNichtAbfrageAnweisung(connection, sqlStatement)
        dblib.dbVerbindungAbbauen(connection)

    def bestimme_where_bedingung(self, datum):
        """ WHERE-Bedingung für Löschen Tageseinträge bestimmen """
        pass

    def importieren_tag(self, datum):
        """ importieren einer Bewegungsdatentabelle """
        print(
            "--> Importieren Tageseinträge der Bewegungsdatentabelle:",
            self.tabellenname,
            datum.strftime("%d.%m.%Y"),
            "\n",
        )
        self.einlesen_daten(datum)
        self.bereinigen_daten()
        self.ergaenze_fremdschluesel(datum)
        self.speichern_daten(datum)
        return self.ds_ok, self.ds_verworfen

    def einlesen_daten(self, datum):
        """ Einlesen einer Bewegungsdatendatei """
        dateiname = self.get_dateinamen_start() + datum.strftime("%Y%m%d") + ".csv"
        # keine Datei vorhanden -> leere Liste
        if os.path.isfile(dateiname) != True:
            return []
        # Dataframe aufbauen
        self.df = pd.read_csv(dateiname, header=None)
        self.df.columns = self.bestimme_spaltenliste()
        return

    def get_dateinamen_start(self):
        pass

    def bestimme_spaltenliste(self):
        pass

    def ergaenze_fremdschluesel(self, datum):
        pass

    def bereinigen_daten(self):
        """ Bereinigen der Bewegungsdaten """

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


    def speichern_daten(self, datum):
        """ Speichern in einer Bewegungsdatentabelle """
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        sql_statement = self.bestimme_insert_anfang()
        erster_wert = True
        for i in self.df.index:
            liste_werte = list(self.df.loc[i])
            sql_statement = sql_statement + self.bestimme_insert_werte(
                datum, liste_werte, erster_wert
            )
            erster_wert = False
        dblib.dbNichtAbfrageAnweisung(connection, sql_statement)
        dblib.dbVerbindungAbbauen(connection)
        self.ds_ok = self.ds_ok + len(self.df.index)

    def bestimme_insert_anfang(self):
        pass

    def bestimme_insert_werte(self, datum, liste_werte):
        pass

# Klasse nds_rechnernutzungen ##########################################################


class nds_rechnernutzungen(nds_bewegungsdaten):
    def __init__(self):
        """ Konstruktor der Klasse Rechnernutzungen """
        nds_bewegungsdaten.__init__(self)
        self.tabellenname = "rechnernutzungen"
        self.fkdf_rechner = None
        self.fkdf_benutzer = None

    def bestimme_where_bedingung(self, datum):
        """ WHERE-Bedingung für Löschen Tageseinträge bestimmen """
        where_bedingung = (
            " WHERE "
            + datum.strftime("'%Y-%m-%d 00:00:00'")
            + " <= anmeldezeit AND abmeldezeit <= "
            + datum.strftime("'%Y-%m-%d 23:59:59'")
        )
        return where_bedingung

    def get_dateinamen_start(self):
        return "daten_ls1_rechnernutzung_"

    def bestimme_spaltenliste(self):
        return ["Nr", "Rechnername", "Benutzername", "Anmeldezeit", "Abmeldezeit"]

    def ergaenze_fremdschluesel(self, datum):
        # Dataframes mit Rechner und Benutzern für Fremdschlüssel laden
        if self.fkdf_rechner == None:
            connection = dblib.dbVerbindungAufbauen(
                self.host, self.user, self.passwd, self.db
            )
            self.fkdf_rechner = pd.read_sql("SELECT * FROM rechner", connection)
            self.fkdf_rechner.columns = ["RechnerID", "Rechnername"]
            self.fkdf_benutzer = pd.read_sql(
                "SELECT benutzerID, benutzername FROM benutzer", connection
            )
            self.fkdf_benutzer.columns = ["BenutzerID", "Benutzername"]
        dblib.dbVerbindungAbbauen(connection)
        # Fremdschlüssel für Rechner und Benutzer dazumergen
        self.df = pd.merge(self.df, self.fkdf_rechner, on="Rechnername", how="left")
        self.df = pd.merge(self.df, self.fkdf_benutzer, on="Benutzername", how="left")
        # Zeilen mit fehlenden Einträgen löschen
        zeilen_vorher = len(self.df.index)
        self.df.dropna(inplace=True)
        zeilen_nachher = len(self.df.index)
        if zeilen_nachher < zeilen_vorher:
            self.ds_verworfen = self.ds_verworfen + zeilen_vorher - zeilen_nachher
            print(
                "!!! Zeilen mit fehlenden Fremdschlüsseln gelöscht:",
                zeilen_vorher - zeilen_nachher,
                "\n",
            )

    def bestimme_insert_anfang(self):
        return "INSERT INTO rechnernutzungen ( rechnerID, benutzerID, anmeldezeit, abmeldezeit) VALUES "

    def bestimme_insert_werte(self, datum, liste_werte, erster_wert):
        if erster_wert == True:
            werte_statement = ""
        else:
            werte_statement = ","
        werte_statement = werte_statement + (
            " ( "
            + str(liste_werte[5])
            + ","
            + str(liste_werte[6])
            + ",'"
            + datum.strftime("%Y-%m-%d ")
            + str(liste_werte[3])
            + "','"
            + datum.strftime("%Y-%m-%d ")
            + str(liste_werte[4])
            + "')"
        )
        return werte_statement

# Klasse nds_anwendungsnutzungen ##########################################################


class nds_anwendungsnutzungen(nds_bewegungsdaten):
    def __init__(self):
        """ Konstruktor der Klasse Anwendungsnutzungen """
        nds_bewegungsdaten.__init__(self)
        self.tabellenname = "anwendungsnutzungen"
        self.fkdf_anwendungen = None
        self.fkdf_rechner = None
        self.fkdf_benutzer = None
        self.fkdf_rechnernutzungen = None

    def bestimme_where_bedingung(self, datum):
        """ WHERE-Bedingung für Löschen Tageseinträge bestimmen """
        where_bedingung = (
            " WHERE "
            + datum.strftime("'%Y-%m-%d 00:00:00'")
            + " <= startzeit AND endzeit <= "
            + datum.strftime("'%Y-%m-%d 23:59:59'")
        )
        return where_bedingung

    def get_dateinamen_start(self):
        return "daten_ls1_anwendungsnutzung_"

    def bestimme_spaltenliste(self):
        return [
            "Nr",
            "Anwendungsname",
            "Rechnername",
            "Benutzername",
            "Startzeit",
            "Endzeit",
        ]

    def ergaenze_fremdschluesel(self, datum):
        # Dataframes mit Anwendungen und Rechnernutzungen für Fremdschlüssel laden
        if self.fkdf_rechner == None:
            connection = dblib.dbVerbindungAufbauen(
                self.host, self.user, self.passwd, self.db
            )
            self.fkdf_anwendungen = pd.read_sql(
                "SELECT anwendungsID, anwendungsname FROM anwendungen", connection
            )
            self.fkdf_anwendungen.columns = ["AnwendungsID", "Anwendungsname"]
            self.fkdf_rechner = pd.read_sql("SELECT * FROM rechner", connection)
            self.fkdf_rechner.columns = ["RechnerID", "Rechnername"]
            self.fkdf_benutzer = pd.read_sql(
                "SELECT benutzerID, benutzername FROM benutzer", connection
            )
            self.fkdf_benutzer.columns = ["BenutzerID", "Benutzername"]
            sql_statement = (
                "SELECT rechnernutzungsID,  rechnerID, benutzerID, anmeldezeit, abmeldezeit FROM rechnernutzungen WHERE "
                + datum.strftime("'%Y-%m-%d 00:00:00'")
                + " <= anmeldezeit AND abmeldezeit <= "
                + datum.strftime("'%Y-%m-%d 23:59:59'")
            )
            self.fkdf_rechnernutzungen = pd.read_sql(sql_statement, connection)
            self.fkdf_rechnernutzungen.columns = [
                "RechnernutzungsID",
                "RechnerID",
                "BenutzerID",
                "Anmeldezeit",
                "Abmeldezeit",
            ]
            dblib.dbVerbindungAbbauen(connection)
        # Fremdschlüssel für Anwendungen, Rechner, Benutzer und Rechnernutzung dazumergen
        self.df = pd.merge(
            self.df, self.fkdf_anwendungen, on="Anwendungsname", how="left"
        )
        self.df = pd.merge(self.df, self.fkdf_rechner, on="Rechnername", how="left")
        self.df = pd.merge(self.df, self.fkdf_benutzer, on="Benutzername", how="left")
        self.df = pd.merge(
            self.df,
            self.fkdf_rechnernutzungen,
            on=["RechnerID", "BenutzerID"],
            how="left",
        )
        # evtl. durch Join entstandene Fehleinträge wieder entfernen
        self.df['Anmeldezeit'] = pd.to_datetime(self.df['Anmeldezeit']).dt.time
        self.df['Abmeldezeit'] = pd.to_datetime(self.df['Abmeldezeit']).dt.time
        self.df['Startzeit'] = pd.to_datetime(self.df['Startzeit']).dt.time
        self.df['Endzeit'] = pd.to_datetime(self.df['Endzeit']).dt.time
        self.df.drop(self.df.loc[self.df['Startzeit']<self.df['Anmeldezeit']].index, inplace=True)
        self.df.drop(self.df.loc[self.df['Endzeit']>self.df['Abmeldezeit']].index, inplace=True)

        # Zeilen mit fehlenden Einträgen löschen
        zeilen_vorher = len(self.df.index)
        self.df.dropna(inplace=True)
        zeilen_nachher = len(self.df.index)
        if zeilen_nachher < zeilen_vorher:
            self.ds_verworfen = self.ds_verworfen + zeilen_vorher - zeilen_nachher
            print(
                "!!! Zeilen mit fehlenden Fremdschlüsseln gelöscht:",
                zeilen_vorher - zeilen_nachher,
                "\n",
            )

    def bestimme_insert_anfang(self):
        return "INSERT INTO anwendungsnutzungen ( anwendungsID, rechnernutzungsID, startzeit, endzeit) VALUES "

    def bestimme_insert_werte(self, datum, liste_werte, erster_wert):
        if erster_wert == True:
            werte_statement = ""
        else:
            werte_statement = ","
        werte_statement = werte_statement + (
            " ( "
            + str(liste_werte[6])
            + ","
            + str(liste_werte[9])
            + ",'"
            + datum.strftime("%Y-%m-%d ")
            + str(liste_werte[4])
            + "','"
            + datum.strftime("%Y-%m-%d ")
            + str(liste_werte[5])
            + "')"
        )
        return werte_statement
