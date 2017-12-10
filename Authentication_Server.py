import web
import re
import base64
import Web_Changed
import shelve
import os
from cryptography.fernet import Fernet

# The Authentication Server

urls = (
    '/','Index_Auth_Class',
    '/login','Login_Auth_Class',
    '/getkey','Server_AS_SecretKey_Class'
)


'''
class Index_Auth_Class:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            return 'Authorized!'
        else:
            raise web.seeother('/login')
'''
class Login_Auth_Class:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        #print("Auth: ",auth)
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ','',auth)
            #print("auth:", auth)
            username,password = base64.decodestring(auth.encode()).decode().split(':')

            # Check the username and password in the persistant dictionary
            try:
                client_auth_details = shelve.open("Client_Auth_Details.dat")
                #print(list(client_auth_details.keys()))
                if username in list(client_auth_details.keys()):
                    if password == client_auth_details[username]:
                        #raise web.seeother('/')
                        session_key = os.urandom(16)
                        ticket = session_key
                        ticket_encrypted = Encrypt_Session_Key(ticket)
                        print("Encrypted Ticket: ",ticket_encrypted)
                        token = session_key+ticket_encrypted
                        print("------------------------")
                        print("Session key: ", session_key)
                        print("-----------------------")
                        print("Token: ", token)

                        # Encrypt the token with client password before sending to client
                        # If the length of the password greater that 32 bytes, only the first 32 bytes are taken as encrypt key
                        # If the length of the password is less that 32 bytes, password is appended with '0's. So that the length is 32 bytes
                        if len(password) >= 32:
                            password_32bytes = password[:32]
                        else:
                            letter_count = 32-len(password)
                            password_32bytes = ''.join(('0') for i in range(letter_count))
                        encrypt_key_with_password = password+password_32bytes
                        encrypt_key_with_password_encoded =  base64.urlsafe_b64encode(encrypt_key_with_password.encode())
                        cipher = Fernet(encrypt_key_with_password_encoded)
                        token_encrypted = cipher.encrypt(token)
                        print("Token Encrypted: ",token_encrypted)
                        return token_encrypted
                    else:
                        authreq = True
                else:
                    authreq = True
            except KeyError as error:
                authreq = True
            finally:
                client_auth_details.close()

        if authreq:
            web.header('WWW-Authenticate','Basic realm="Authentication of client"')
            web.ctx.status = '401 Unauthorized'
            return "Not Authorized!"

class Server_AS_SecretKey_Class:
    # Get method that is called by other servers to get the secret key that is shared between Authetication Server and other servers.
    def GET(self):
        encryption_key_file = shelve.open("Encrytion_Key_File.dat")
        try:
            secret_key = encryption_key_file['1']
        finally:
            encryption_key_file.close()
        return secret_key

def Encrypt_Session_Key(ticket):
    # To encrypt the ticket using a randomly generated key
    # The method takes the secret_key or encryption_key saved in the file. Using this encryption key the ticket which has session key is encrypted.
    encryption_key_file = shelve.open("Encrytion_Key_File.dat")
    try:
        secret_key = encryption_key_file['1']
    finally:
        encryption_key_file.close()

    cipher = Fernet(secret_key)
    ticket_encrypted = cipher.encrypt(ticket)
    return ticket_encrypted




if __name__=='__main__':
    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=8083)
