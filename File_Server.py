import web
import os
import Web_Changed

urls = (
'/filepath/(.*)', 'file_server'
)

class file_server:
    def GET(self,filepath):
        # To open and read the requested file (filepath is passed).
        if not filepath:
            return "Filepath not given"
        else:
            if os.path.isfile(filepath):
                with open(filepath) as f:
                    return f.read()
            else:
                return "File not found"

    def POST(self,filepath):
        # To open and write the requested file (filepath is passed).
        if not filepath:
            return "Filepath not given"
        else:
            if os.path.isfile(filepath):
                with open(filepath, 'w') as f:
                    f.write(web.data().decode())
                    return "Success"
            else:
                return "File not found"



def get_file_path(filepath):
    print("filepath")


if __name__=="__main__":
    #app = web.application(urls,globals())
    #app.run()
    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=8081)
