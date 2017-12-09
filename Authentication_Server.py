import web
import re
import base64
import Web_Changed
import shelve

urls = (
    '/','Index_Auth_Class',
    '/login','Login_Auth_Class'
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
                        return "Authorized!"
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

if __name__=='__main__':
    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=8083)
