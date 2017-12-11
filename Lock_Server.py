import web
import os
import shelve
import Web_Changed
from cryptography.fernet import Fernet
import requests as req
import base64

urls = (
'/file/lock/(.*)', 'lock_server',
'/file/unlock/(.*)', 'unlock_server_class'
)

class lock_server:
    def GET(self,filename):
        # To check the file passed is locked or not. If the file is locked, return locked. If file is not locked, return filename.
        # If '*' is passed, it returns all files which are not locked.

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

        # To get the files which are not locked
        if filename == '*':
            file_locks = shelve.open("File_locks.dat")
            try:
                files_str = ""
                locks_keys = list(file_locks.keys())
                locks_keys.sort()
                count = 1
                for i in range(len(locks_keys)):
                    if file_locks[locks_keys[i]] == 0:
                        files_str = files_str + str(count) + " " + locks_keys[i] + "\n"
                        count = count + 1
            finally:
                file_locks.close()
            return encrypt_message(files_str,ticket)

        if not filename:
            return encrypt_message("No file name found",ticket)

        # when single filename is passed, this block of code returns filename if it is not locked. else if the file is locked, it returns "filename is locked"
        filename_not_locked = ""
        locks_keys = shelve.open("File_locks.dat")
        try:
            semaphore = locks_keys[filename]
            if semaphore == 0:
                filename_not_locked = filename
                #locks_keys[filename] = 1
            else:
                filename_not_locked = filename + " is locked"
        except KeyError:
            filename_not_locked = "file not found"
        finally:
            locks_keys.close()
        return encrypt_message(filename_not_locked,ticket)


    def POST(self,filename):
        # To lock the file if it is not locked.
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

        if not filename:
            return encrypt_message("Filename not given",ticket)
        else:
            lock_result = ""
            locks_keys = shelve.open("File_locks.dat")
            try:
                semaphore = locks_keys[filename]
                if semaphore == 0:
                    #filename_not_locked = filename
                    locks_keys[filename] = 1
                    lock_result = "Success locked"
            except KeyError:
                lock_result = "file not found"
            finally:
                locks_keys.close()
            return encrypt_message(lock_result,ticket)

class unlock_server_class:
    # To unlock the locked file. The semaphore value is changed from 1 to 0.
    def POST(self,filename):
        # To lock the file if it not filename_not_locked
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

        if not filename:
            return encrypt_message("Filename not given",ticket)
        else:
            unlock_result = ""
            locks_keys = shelve.open("File_locks.dat")
            try:
                semaphore = locks_keys[filename]
                if semaphore == 1:
                    #filename_not_locked = filename
                    locks_keys[filename] = 0
                    lock_result = "unlocked!"
            except KeyError:
                unlock_result = "file not found"
            finally:
                locks_keys.close()
            return encrypt_message(unlock_result,ticket)

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
    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=8082)
