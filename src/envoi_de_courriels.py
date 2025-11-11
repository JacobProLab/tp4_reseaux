import email.message
import smtplib
import socket

# Recuperation des donnees pour les champs du courriel
mail_from: str = "japro72@ulaval.ca"
mail_to: str = "japro72@ulaval.ca"
subject: str = "Test pour TP4"

print("Body: (enter '.' on a single line to finish typing)")
body = ""
buffer = ""
while (buffer != ".\n"):
    body += buffer
    buffer = input() + '\n'

# Creation de l'objet courriel avec EmailMessage
message = email.message.EmailMessage()
message["From"] = mail_from
message["To"] = mail_to
message["Subject"] = subject
message.set_content(body)

# Envoi du courriel avec le protocole SMTP par le server de l'universite Laval
try:
    with smtplib.SMTP(host="smtp.ulaval.ca", timeout=10) as connection:
        connection.send_message(message)
        print("Message envoye avec succes.")
except smtplib.SMTPException:
    print("Le message n'a pas pu etre envoye.")
except socket.timeout:
    print("La connexion au serveur SMTP n'a pas pu etre etablie")


