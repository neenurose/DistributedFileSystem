import web
import os
import shelve
from cryptography.fernet import Fernet
import requests as req
import base64

urls = (
'/file/(.*)', 'directory_server'
)

class directory_server:
    def GET(self,filename):
        # To get the absolute path of the file passed if filename is passed. If '*' is passed, get function should return list of filenames
        secret_key = get_server_encryption_key()
        print("-----------")
        print("secret_key: ",secret_key)
        print("-----------")
        (encrypted_filename, encrypted_ticket) = get_filename_ticket(filename)
        print("tuple: ",encrypted_filename,"hehe:",encrypted_ticket)
        ticket = decrypt_ticket_from_client(encrypted_ticket,secret_key)
        filename = decrypt_filename_from_client(encrypted_filename,ticket).decode()
        print("------------")
        print("filename after decryption: ",filename)
        print("------------")

        filepath = ""
        # to return a list of filepaths
        if filename == '*':
            names = shelve.open("Directory_names_file.dat")
            try:
                names_str = ""
                names_keys = list(names.keys())
                names_keys.sort()
                for i in range(len(names_keys)):
                    names_str = names_str + str(i+1) + " " + names_keys[i] + "\n"
            finally:
                names.close()
            names_str = encrypt_message(names_str,ticket)
            return names_str

        if not filename:
            return encrypt_message("No file name found",ticket)

        # when single filename is passed
        names = shelve.open("Directory_names_file.dat")
        try:
            filepath = names[filename]
        except KeyError:
            filepath = "file not found"
        finally:
            names.close()
        return encrypt_message(filepath,ticket)


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
    app = web.application(urls,globals())
    app.run()
