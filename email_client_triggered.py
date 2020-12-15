#import für Abrfage des Währungskurs
from forex_python.converter import CurrencyRates
#imports für Datum
from datetime import date
import datetime
#imports für E-Mail erstellen/versenden
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Funktion zum Versenden der Mail definieren
def send():
    #Email-Adressen und Passwort über input festlegen
    absender = input("Geben sie ihre Mail-Adresse ein: ")
    passwort = input("Geben sie ihr Passwort ein: ")
    empfänger = input("An welche Adresse soll die E-Mail versendet werden? ")
    #Betreff der Mail festlegen
    betreff = "Währungskurs"
    
    #mit vorherigen Eingaben (Absender,Empfänger,Betreff) Mail generieren
    mail = MIMEMultipart()
    #Text wird erst später festgelegt, da je nach Ereignis unterschiedlicher Inhalt notwendig
    mail.attach(MIMEText(text))
    mail['Subject'] = betreff
    mail['From'] = absender
    mail['To'] = empfänger

    #einloggen, hier: GMX SMTP-Server
    server = smtplib.SMTP('mail.gmx.net', 587)
    server.starttls()
    server.login(absender, passwort)
    #zuvor generierte Email versenden
    server.send_message(mail)
    server.quit()
    
    
#Datum auf heute setzten und Wechselkurs abfragen    
#heutigen Kurs in Variable Speichern
c = CurrencyRates()
heute = date.today()
kurstd = c.get_rate('EUR', 'CHF', heute)
print(kurstd)

#leeere Liste erstellen
#jeweils 1 Tag zurück im Datum und jeweiligen Kurs abfragen
#jeden abgefragten Tageskurs in der Liste abspeichern
vgl = []
i = 1
while i < 60:
    past = heute - datetime.timedelta(days=i)
    kurs = c.get_rate('EUR', 'CHF', past)
    vgl.append(kurs)
    i += 1
    
#Summe Kurse der letzten Tage berechnen
#alle Objekte der Liste addieren
x = 1
tot = vgl[0] + vgl[x]
while x < 58:
    x += 1
    tot = tot + vgl[x]
    
#Durchschnitt der vorangegenagen Kurse berechnen
#Summe der Objekte dividieren durch Anzahl der Objekte 
av = tot/(len(vgl))   
print(round(av,4))


#Bedingung, wann welche Nachricht verschickt wird, über if-Abfrage
#Vergleich, ob Kurs im Vegleich zum Durchschnitt um bestimmten Faktor verändert ist
if av*1.005 < kurstd:
    #ist der Kurs hoch, erhält man für 1 Euro mehr Franken
    #text für Email festlegen und send Funktion aufrufen
    text = """
    Heute ist es besonders günstig Euro in Franken zu tauschen
    
    Der heutige Kurs liegt bei:
    EUR 1 = CHF """ + str(kurstd)
    send()
elif av*0.995 > kurstd:
    #ist der Kurs niedrig, erhält man für 1 Franken mehr Euro
    #text für Email festlegen und send Funktion aufrufen
    text = """
    Heute ist es besonders günstig Franken in Euro zu tauschen
    
    Der heutige Kurs liegt bei:
    EUR 1 = CHF """ + str(kurstd)
    send()
else:
    #keine der beiden vorherigen Bedingungen trifft zu
    #Kurs ist weder besonders hoch, noch besonders niedrig
    #Programm beenden ohne Handlungsempfehlung, also keine Email
    quit()