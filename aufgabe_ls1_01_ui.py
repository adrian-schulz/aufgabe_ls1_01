""" Nutzungsdatensystem für LS1 - Benutzerschnittstelle

    Nutzungsdatensystem für LS1 - Benutzerschnittstelle - Ausgangsversion
 
    Einordnung:         FISI-LF8-LS1-Nutzungsdatensystem

    Name:               Markus Breuer
    Organisaion:        BK-GuT

    Erstellt:           24.05.2021
    Letzte Änderung:    10.06.2021
    """

from aufgabe_ls1_01_stammdaten import nds_rechnerkategorien, nds_stammdaten
from aufgabe_ls1_01_stammdaten import nds_benutzer
from aufgabe_ls1_01_stammdaten import nds_rechner
from aufgabe_ls1_01_stammdaten import nds_anwendungen, nds_anwendungskategorien
from aufgabe_ls1_01_nutzungsdaten import nds_nutzungsdaten
import datetime


class nds_ui:
    def __init__(self):
        """ Konstruktor der Klasse ui """
        pass

    def auswahl_menue(self):
        """ Auswahlmenü und Benutzerauswahl """
        print("Nutzungsdatensystem Datenmanagement")  # Überschrift
        print("-----------------------------------")
        print("1. Stammdatenmagement")
        print("   (10) Benutzerdaten importieren")  # Auswahlmenü
        print("   (11) Benutzerdaten löschen")
        print("   (12) Rechnerdaten importieren")
        print("   (13) Rechnerdaten löschen")
        print("   (14) Anwendungsdaten importieren")
        print("   (15) Anwendungsdaten löschen")
        print("   (16) Anwendungskategorien importieren")
        print("   (17) Anwendungskategorien löschen")
        print("   (18) Rechnerkategorien importieren")
        print("   (19) Rechnerkategorien löschen")
        print("2. Bewegungsdatenmagement")
        print("   (20) Bewegungsdaten eines Tages importieren")
        print("   (21) Bewegungsdaten eines Tages löschen")
        print("   (22) Alle Bewegungsdaten löschen")
        print("3. Datenbestandsinformationen")
        print("   (30) Statistik Stammdaten")
        print("   (31) Statistik Bewegungsdaten")
        print("   (32) Datengüte Bewegungsdaten")
        print("(0) Beenden")

        befehl = int(input("Auswahl: "))  # Benutzerauswahl
        print("")
        return befehl

    def start(self):
        """ Hauptprogramm des Nutzungsdatensystem für LS1 """

        while True:
            befehl = self.auswahl_menue()
            if befehl == 10:
                benutzer = nds_benutzer()
                benutzer.importieren()
            elif befehl == 11:
                benutzer = nds_benutzer()
                benutzer.loeschen()
            elif befehl == 12:
                rechner = nds_rechner()
                rechner.importieren()
            elif befehl == 13:
                rechner = nds_rechner()
                rechner.loeschen()
            elif befehl == 14:
                anwendungen = nds_anwendungen()
                anwendungen.importieren()
            elif befehl == 15:
                anwendungen = nds_anwendungen()
                anwendungen.loeschen()
            elif befehl == 16:
                anwendungskategorien = nds_anwendungskategorien()
                anwendungskategorien.importieren()
            elif befehl == 17:
                anwendungskategorien = nds_anwendungskategorien()
                anwendungskategorien.loeschen()
            elif befehl == 18:
                rechnerkategorien = nds_rechnerkategorien()
                rechnerkategorien.importieren()
            elif befehl == 19:
                rechnerkategorien = nds_rechnerkategorien()
                rechnerkategorien.loeschen()
            elif befehl == 20:
                datums_string = input('Datum "TT.MM.JJJJ": ')
                tag, monat, jahr = map(int, datums_string.split("."))
                datum = datetime.date(jahr, monat, tag)
                nutzungsdaten = nds_nutzungsdaten()
                nutzungsdaten.importieren_tag(datum)
            elif befehl == 21:
                datums_string = input('Datum "TT.MM.JJJJ": ')
                tag, monat, jahr = map(int, datums_string.split("."))
                datum = datetime.date(jahr, monat, tag)
                nutzungsdaten = nds_nutzungsdaten()
                nutzungsdaten.loeschen_tag(datum)
            elif befehl == 22:
                nutzungsdaten = nds_nutzungsdaten()
                nutzungsdaten.loeschen_alle()
            elif befehl == 30:
                stammdaten = nds_stammdaten()
                stammdaten.statistik()
            elif befehl == 0:  # Beenden
                break
            else:
                print("Unbekannter Befehl " + str(befehl))
                print("")


if __name__ == "__main__":
    nds_ui = nds_ui()
    nds_ui.start()
