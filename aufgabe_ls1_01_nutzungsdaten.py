""" Nutzungsdatensystem für LS1 - Nutzungssdaten

    Nutzungsdatensystem für LS1 - Nutzungssdaten - Ausgangsversion
 
    Einordnung:         FISI-LF8-LS1-Nutzungsdatensystem

    Name:               Markus Breuer
    Organisaion:        BK-GuT

    Erstellt:           25.05.2021
    Letzte Änderung:    10.06.2021
    """

from aufgabe_ls1_01_bewegungsdaten import nds_rechnernutzungen
from aufgabe_ls1_01_bewegungsdaten import nds_anwendungsnutzungen
import dblib

# Klasse nds_nutzungsdaten ###################################################


class nds_nutzungsdaten:
    def __init__(self):
        """ Konstruktor der Klasse Nutzungsdaten """
        pass

    def loeschen_alle(self):
        """ loeschen aller Bewegungsdaten """
        print(
            "--> Löschen aller aller Bewegungsdaten:",
            "\n"
        )
        anwendungsnutzungen = nds_anwendungsnutzungen()
        anwendungsnutzungen.loeschen_alle()
        rechnernutzungen = nds_rechnernutzungen()
        rechnernutzungen.loeschen_alle()
        imp = ndsimporte()
        imp.loeschen_alle()

    def loeschen_tag(self, datum):
        """ loeschen der Bewegungsdaten eines Tages"""
        print(
            "--> Löschen der Bewegungsdaten eines Tages:",
            datum.strftime("%d.%m.%Y"),
            "\n"
        )
        anwendungsnutzungen = nds_anwendungsnutzungen()
        anwendungsnutzungen.loeschen_tag( datum)
        rechnernutzungen = nds_rechnernutzungen()
        rechnernutzungen.loeschen_tag(datum)
        imp = ndsimporte()
        imp.loeschen_tag(datum)

    def importieren_tag(self, datum):
        """ importieren der Bewegungsdaten eines Tages"""
        print(
            "--> Löschen der Bewegungsdaten eines Tages:",
            datum.strftime("%d.%m.%Y"),
            "\n"
        )
        anwendungsnutzungen = nds_anwendungsnutzungen()
        rechnernutzungen = nds_rechnernutzungen()
        anwendungsnutzungen.loeschen_tag( datum)
        rechnernutzungen.loeschen_tag(datum)
        rdsOK, rdsVerworfen = rechnernutzungen.importieren_tag(datum)
        adsOK, adsVerworfen = anwendungsnutzungen.importieren_tag( datum)
        imp = ndsimporte()
        imp.loeschen_tag(datum)
        imp.einfuegen_tag(datum, rdsOK, rdsVerworfen, adsOK, adsVerworfen)


class ndsimporte:
    def __init__(self):
        """ Konstruktor der Klasse ndsimporte """
        self.host = ""
        self.user = ""
        self.passwd = ""
        self.db = ""
        self.setze_db_verbindungsparameter()

    def setze_db_verbindungsparameter(self):
        self.host = "localhost"
        self.user = "root"
        self.passwd = ""
        self.db = "ndsdb"

    def loeschen_alle(self):
        """ loeschen aller Einträge in der Tabelle ndsimporte """
        print(
            "--> Löschen aller Einträge in der Tabelle ndsimporte",
            "\n"
        )
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        sqlStatement = "DELETE FROM ndsimporte"
        dblib.dbNichtAbfrageAnweisung(connection, sqlStatement)
        dblib.dbVerbindungAbbauen(connection)
        
    def loeschen_tag(self, datum):
        """ loeschen der Einträge in der Tabelle ndsimporte eines Tages"""
        print(
            "--> Löschen der Einträge in der Tabelle ndsimporte eines Tages:",
            datum.strftime("%d.%m.%Y"),
            "\n"
        )
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        sqlStatement = (
            "DELETE FROM ndsimporte WHERE "
            + datum.strftime("'%Y-%m-%d'")
            + " = datentag "
        )
        dblib.dbNichtAbfrageAnweisung(connection, sqlStatement)
        dblib.dbVerbindungAbbauen(connection)

    def einfuegen_tag(self, datentag, rdsOK, rdsVerworfen, adsOK, adsVerworfen):
        """ einfügen der Einträge in der Tabelle ndsimporte eines Tages"""
        print(
            "--> Einfügen eines Eintrags in die Tabelle ndsimporte:",
            datentag.strftime("%d.%m.%Y"),
            "\n"
        )
        connection = dblib.dbVerbindungAufbauen(
            self.host, self.user, self.passwd, self.db
        )
        sql_statement =  (
            "INSERT INTO ndsimporte ( datenTag, rdsOK, rdsVerworfen, adsOK, adsVerworfen) VALUES ( "
            + datentag.strftime("'%Y-%m-%d'")
            + ","
            + str(rdsOK)
            + ","
            + str(rdsVerworfen)
            + ","
            + str(adsOK)
            + ","
            + str(adsVerworfen)
            + ")"
        )
        dblib.dbNichtAbfrageAnweisung(connection, sql_statement)
        dblib.dbVerbindungAbbauen(connection)     
