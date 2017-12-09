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
