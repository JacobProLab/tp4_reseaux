import argparse
import email.message
import re
import smtplib
import socket
import sys
from datetime import datetime, timezone
from typing import NoReturn, Sequence


def _get_port(argv: Sequence[str]) -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port",
                        action="store",
                        dest="port",
                        type=int,
                        default=1400)
    
    return parser.parse_args(argv).port

def _prepare_socket(port: int) -> socket.socket:
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", port))
    server_socket.listen()
    print(f"Listening on port {server_socket.getsockname()[1]}")
    
    return server_socket

def _server_loop(server_socket: socket.socket) -> NoReturn:
    
    address_request: bytes = "A qui dois-je envoyer un courriel ?\n".encode('utf-8')
    address_error: bytes = "Saisissez une adresse valide: ".encode('utf-8')
    
    email_username_catcher = r"[a-zA-Z0-9_\.+-]"
    domain_catcher = r"[a-zA-Z0-9_\.+-]"
    top_level_domain_catcher = r"[a-zA-Z0-9_\.]"

    pattern: re.Pattern = re.compile(
        rf"(^{email_username_catcher}+@{domain_catcher}+\.{top_level_domain_catcher}+$)"
    )

    while True:

        # Connexion d'un client
        client, _ = server_socket.accept()
        client.send(address_request)

        # Recuperation et verification de l'adresse de destination
        dest_address = client.recv(1024).decode().strip(" \n")
        while pattern.fullmatch(dest_address) is None:
            client.send(address_error)
            dest_address = client.recv(1024).decode().strip(" \n")

        # Creation du courriel
        message = email.message.EmailMessage()
        message["From"] = "exercice2@glo2000.ca"
        message["To"] = dest_address
        message["Subject"] = "Exercice 3"
        message["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
        message.set_content("Courriel envoye par le serveur")
        
        # Envoi du courriel
        try:
            with smtplib.SMTP(host="smtp.ulaval.ca", timeout=10) as connection:
                connection.send_message(message)
                reply = "Message envoye avec succes."
        except smtplib.SMTPException:
            reply = "Le message n'a pas pu etre envoye."
        except socket.timeout:
            reply = "Le serveur SMTP est injoignable."

        client.send(reply.encode('utf-8'))
        client.close()



def _main() -> NoReturn:
    port = _get_port(sys.argv[1:])
    server_socket = _prepare_socket(port)
    _server_loop(server_socket)



if __name__ == "__main__":
    _main()

