import web
import os
import Web_Changed
from cryptography.fernet import Fernet
import requests as req
import base64

urls = (
'/filepath/(.*)', 'file_server'
)

class file_server:
    def GET(self,filepath):
        # To open and read the requested file (filepath is passed).
        secret_key = get_server_encryption_key()
        print("-----------")
        print("secret_key: ",secret_key)
        print("-----------")
        (encrypted_filepath, encrypted_ticket) = get_filename_ticket(filepath)
        print("tuple: ",encrypted_filepath,"hehe:",encrypted_ticket)
        ticket = decrypt_ticket_from_client(encrypted_ticket,secret_key)
        filepath = decrypt_filename_from_client(encrypted_filepath,ticket).decode()
        print("------------")
        print("filepath after decryption: ",filepath)
        print("------------")

        if not filepath:
            return encrypt_message("Filepath not given",ticket)
        else:
            if os.path.isfile(filepath):
                with open(filepath) as f:
                    return encrypt_message(f.read(),ticket)
            else:
                return encrypt_message("File not found",ticket)

    def POST(self,filepath):
        # To open and write the requested file (filepath is passed).
        secret_key = get_server_encryption_key()
        print("-----------")
        print("secret_key: ",secret_key)
        print("-----------")
        (encrypted_filepath, encrypted_ticket) = get_filename_ticket(filepath)
        print("tuple: ",encrypted_filepath,"hehe:",encrypted_ticket)
        ticket = decrypt_ticket_from_client(encrypted_ticket,secret_key)
        filepath = decrypt_filename_from_client(encrypted_filepath,ticket).decode()
        print("------------")
        print("filepath after decryption: ",filepath)
        print("------------")

        if not filepath:
            return encrypt_message("Filepath not given",ticket)
        else:
            if os.path.isfile(filepath):
                with open(filepath, 'w') as f:
                    f.write(web.data().decode())
                    return encrypt_message("Success",ticket)
            else:
                return encrypt_message("File not found",ticket)


def get_server_encryption_key():
    auth_server_url = "http://localhost:8083/getkey"
    response = req.get(auth_server_url)
    print("encryption key: ",response.text)
    encryption_key = response.text.encode()
    return encryption_key

def get_filename_ticket(message):
    # get the filename and ticket from the encrypted message.
    print("----------")
    print("message: ",message)
    print("-----------")
    number_of_digits_of_filelength = int(message[0])
    encrypted_file_length = int(message[1:number_of_digits_of_filelength+1])
    encrypted_filename = message[number_of_digits_of_filelength+1:(number_of_digits_of_filelength+encrypted_file_length)+1]
    encrypted_ticket = message[number_of_digits_of_filelength+encrypted_file_length+1:len(message)]
    print("----------")
    print("number of digits: ",number_of_digits_of_filelength)
    print("-----------")
    print("file length: ",encrypted_file_length)
    print("----------")
    print("encrypted file: ",encrypted_filename)
    print("-----------")
    print("Encrypted ticket:", encrypted_ticket)

    return (encrypted_filename,encrypted_ticket)

def decrypt_ticket_from_client(encrypted_ticket,secret_key):
    # The encrypted ticket from client is decrypted.
    #secret_key = get_server_encryption_key()
    cipher = Fernet(secret_key)
    ticket_decrypted = cipher.decrypt(encrypted_ticket.encode())
    print("########")
    return ticket_decrypted

def decrypt_filename_from_client(encrypted_filename,ticket):
    # The encrypted filename from client is decrypted.
    #secret_key = get_server_encryption_key()
    # The message that is encrypted and send from server is decrypted using the session key at the client side.
    session_key = ticket
    session_key_32bytes = session_key+session_key
    session_key_32bytes_encoded = base64.urlsafe_b64encode(session_key_32bytes)
    cipher_session_key = Fernet(session_key_32bytes_encoded)
    filename_decrypted = cipher_session_key.decrypt(encrypted_filename.encode())
    return filename_decrypted


def encrypt_message(message,ticket):
    # The message is encrypted using the session key in ticket.
    session_key = ticket
    session_key_32bytes = session_key+session_key
    session_key_32bytes_encoded = base64.urlsafe_b64encode(session_key_32bytes)
    cipher_session_key = Fernet(session_key_32bytes_encoded)
    message_encrypted = cipher_session_key.encrypt(message.encode())
    print("---------")
    print("Encrypted message: ",message_encrypted)
    print("---------")
    return message_encrypted
def get_file_path(filepath):
    print("filepath")


if __name__=="__main__":
    #app = web.application(urls,globals())
    #app.run()
    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=8081)
