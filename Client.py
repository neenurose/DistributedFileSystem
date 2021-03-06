import requests as req
import json
from requests.auth import HTTPBasicAuth
import base64
from cryptography.fernet import Fernet

url = "http://localhost:8083/login"

'''
filepath = input("Enter the file name:")
url = url+filepath

response = req.post(url)
#print("File: ",response.json())
print("Response: ",response.text)
'''
def client_proxy(method, filename):
    # Calls the directory server.
    # The filename is encrypted. The ticket is appended with the filename and send.
    directory_service_url = "http://localhost:8080/file/"
    message_encrypted = encrypt_message(filename)
    print("------------")
    print("message encrypted: ",message_encrypted.decode())
    print("------------")
    print("Ticket: ",ticket.decode())
    print("--------------")
    message_to_be_send = str(len(str(len(message_encrypted)))) + str(len(message_encrypted)) + str(message_encrypted.decode()) + str(ticket.decode())
    directory_service_url = directory_service_url+message_to_be_send
    response = req.get(directory_service_url)
    print("Response: ",response.text)
    filepath = response.text
    (port_encr,filepath_encr) = get_filepath_port(filepath)
    filepath_decrypted = decrypt_message_from_server(filepath_encr).decode()
    if len(port_encr) > 0:
        port_decrypted = decrypt_message_from_server(port_encr).decode()
        print("----------")
        print("Port: ",port_decrypted)

    print("----------")
    print("Filepath: ",filepath_decrypted)
    print("----------")

    #Check if the method is read or write
    if len(port_encr) > 0:
        if method == "read":
            file_server_url = "http://localhost:"+port_decrypted+"/filepath/"
            filepath_encrypted = encrypt_message(filepath_decrypted)
            print("------------")
            print("filepath encrypted: ",filepath_encrypted.decode())
            print("------------")
            filepath_to_be_send = str(len(str(len(filepath_encrypted)))) + str(len(filepath_encrypted)) + str(filepath_encrypted.decode()) + str(ticket.decode())
            file_server_url = file_server_url+filepath_to_be_send
            response = req.get(file_server_url)
            print("Response: ",response.text)
            filecontent = response.text
            filecontent_decrypted = decrypt_message_from_server(filecontent).decode()
            print("----------")
            print("File content: ",filecontent_decrypted)
            print("----------")
        else:
            payload = input("Enter content to be written into file: ")

            lock_server_url = "http://localhost:8082/file/lock/"
            filename_encrypted = encrypt_message(filename)
            print("------------")
            print("filename encrypted: ",filename_encrypted.decode())
            print("------------")
            print("Ticket: ",ticket.decode())
            print("--------------")
            filename_to_be_send = str(len(str(len(filename_encrypted)))) + str(len(filename_encrypted)) + str(filename_encrypted.decode()) + str(ticket.decode())
            lock_server_url = lock_server_url+filename_to_be_send
            response = req.get(lock_server_url)
            print("Response: ",response.text)
            lock = response.text
            lock_decrypted = decrypt_message_from_server(lock).decode()
            print("----------")
            print("Lock: ",lock_decrypted)
            print("----------")

            if lock_decrypted == filename:
                # to lock the file
                lock_server_url = "http://localhost:8082/file/lock/"
                filename_encrypted = encrypt_message(filename)
                print("------------")
                print("filename encrypted: ",filename_encrypted.decode())
                print("------------")
                print("Ticket: ",ticket.decode())
                print("--------------")
                filename_to_be_send = str(len(str(len(filename_encrypted)))) + str(len(filename_encrypted)) + str(filename_encrypted.decode()) + str(ticket.decode())
                lock_server_url = lock_server_url+filename_to_be_send
                response = req.post(lock_server_url)
                print("Response: ",response.text)
                tolock = response.text
                tolock_decrypted = decrypt_message_from_server(tolock).decode()
                print("----------")
                print("Lock: ",tolock_decrypted)
                print("----------")


                # write into file
                file_server_url = "http://localhost:"+port_decrypted+"/filepath/"
                filepath_encrypted = encrypt_message(filepath_decrypted)
                print("------------")
                print("filepath encrypted: ",filepath_encrypted.decode())
                print("------------")
                filepath_to_be_send = str(len(str(len(filepath_encrypted)))) + str(len(filepath_encrypted)) + str(filepath_encrypted.decode()) + str(ticket.decode())
                file_server_url = file_server_url+filepath_to_be_send

                # encrypting payload to be written into file
                payload_encrypted = encrypt_message(payload)
                print("------------")
                print("payload encrypted: ",payload_encrypted.decode())
                print("------------")
                print("Ticket: ",ticket.decode())
                print("--------------")
                payload_to_be_send = str(len(str(len(payload_encrypted)))) + str(len(payload_encrypted)) + str(payload_encrypted.decode()) + str(ticket.decode())

                response = req.post(file_server_url,data=payload_to_be_send)
                print("Response: ",response.text)
                filecontent = response.text
                filecontent_decrypted = decrypt_message_from_server(filecontent).decode()
                print("----------")
                print("File write: ",filecontent_decrypted)
                print("----------")

                # to unlock lock
                lock_server_url = "http://localhost:8082/file/unlock/"
                filename_encrypted = encrypt_message(filename)
                print("------------")
                print("filename encrypted: ",filename_encrypted.decode())
                print("------------")
                print("Ticket: ",ticket.decode())
                print("--------------")
                filename_to_be_send = str(len(str(len(filename_encrypted)))) + str(len(filename_encrypted)) + str(filename_encrypted.decode()) + str(ticket.decode())
                lock_server_url = lock_server_url+filename_to_be_send
                response = req.post(lock_server_url)
                print("Response: ",response.text)
                unlock = response.text
                unlock_decrypted = decrypt_message_from_server(unlock).decode()
                print("----------")
                print("UnLock: ",unlock_decrypted)
                print("----------")

            '''
            # to unlock lock
            lock_server_url = "http://localhost:8082/file/unlock/"
            filename_encrypted = encrypt_message(filename)
            print("------------")
            print("filename encrypted: ",filename_encrypted.decode())
            print("------------")
            print("Ticket: ",ticket.decode())
            print("--------------")
            filename_to_be_send = str(len(str(len(filename_encrypted)))) + str(len(filename_encrypted)) + str(filename_encrypted.decode()) + str(ticket.decode())
            lock_server_url = lock_server_url+filename_to_be_send
            response = req.post(lock_server_url)
            print("Response: ",response.text)
            unlock = response.text
            unlock_decrypted = decrypt_message_from_server(unlock).decode()
            print("----------")
            print("UnLock: ",unlock_decrypted)
            print("----------")
            '''



    else:
        msg = method + " is not possible!"
        print("----------")
        print(msg)
        print("----------")



def encrypt_message(message):
    # The message is encrypted using the session key that is passed from Authentication Server.
    session_key_32bytes = session_key+session_key
    session_key_32bytes_encoded = base64.urlsafe_b64encode(session_key_32bytes)
    cipher_session_key = Fernet(session_key_32bytes_encoded)
    message_encrypted = cipher_session_key.encrypt(message.encode())
    return message_encrypted

def decrypt_message_from_server(message):
    # The message that is encrypted and send from server is decrypted using the session key at the client side.
    session_key_32bytes = session_key+session_key
    session_key_32bytes_encoded = base64.urlsafe_b64encode(session_key_32bytes)
    cipher_session_key = Fernet(session_key_32bytes_encoded)
    message_decrypted = cipher_session_key.decrypt(message.encode())
    return message_decrypted

def get_filepath_port(message):
    # get the filename and ticket from the encrypted message.
    print("----------")
    print("message: ",message)
    print("-----------")
    number_of_digits_of_port_length = int(message[0])
    encrypted_port_length = int(message[1:number_of_digits_of_port_length+1])
    encrypted_port = message[number_of_digits_of_port_length+1:(number_of_digits_of_port_length+encrypted_port_length)+1]
    encrypted_filepath = message[number_of_digits_of_port_length+encrypted_port_length+1:len(message)]
    print("----------")
    print("number of digits: ",number_of_digits_of_port_length)
    print("-----------")
    print("port length: ",encrypted_port_length)
    print("----------")
    print("encrypted port: ",encrypted_port)
    print("-----------")
    print("Encrypted filepath:", encrypted_filepath)

    return (encrypted_port,encrypted_filepath)


# HTTP_AUTHORIZATION
username = input("Enter the user name: ")
password = input("Enter password: ")

response = req.get(url, auth=HTTPBasicAuth(username,password))
#print("File: ",response.json())
print("Response: ",response.text)
if response.text == "Not Authorized!":
    print("Username and password are incorrect!")
else:
    token = response.text

    # Decrypt the token received from authentication server with client password before sending to client
    # If the length of the password greater that 32 bytes, only the first 32 bytes are taken as encrypt key
    # If the length of the password is less that 32 bytes, password is appended with '0's. So that the length is 32 bytes
    if len(password) >= 32:
        password_32bytes = password[:32]
    else:
        letter_count = 32-len(password)
        password_32bytes = ''.join(('0') for i in range(letter_count))
    encryption_key_with_password = password+password_32bytes
    encryption_key_with_password_encoded =  base64.urlsafe_b64encode(encryption_key_with_password.encode())
    cipher = Fernet(encryption_key_with_password_encoded)
    token_decrypted = cipher.decrypt(token.encode())
    print("Token Received: ",token_decrypted)
    print("----------")
    session_key = token_decrypted[:16]
    ticket = token_decrypted[16:]
    print("------------")
    print("Session_key: ",session_key)
    print("------------")
    print("Ticket: ",ticket)

    method = input("Enter method: ")
    filename = input("Enter filename: ")
    client_proxy(method, filename)
