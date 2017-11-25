import web
import os
import Web_Changed

urls = (
'/filepath/(.*)', 'file_server'
)

class file_server:
    def GET(self,filepath):
        return os.path.getsize(filepath)

def get_file_path(filepath):
    print("filepath")


if __name__=="__main__":
    #app = web.application(urls,globals())
    #app.run()
    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=8081)
