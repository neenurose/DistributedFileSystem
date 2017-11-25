import web
import os
import shelve

urls = (
'/file/(.*)', 'directory_server'
)

class directory_server:
    def GET(self,filename):
        # To get the absolute path of the file passed if filename is passed. If '*' is passed, get function should return list of filenames

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
            return names_str

        if not filename:
            return "No file name found"

        # when single filename is passed
        names = shelve.open("Directory_names_file.dat")
        try:
            filepath = names[filename]
        except KeyError:
            filepath = "file not found"
        finally:
            names.close()
        return filepath



def get_file_path(filepath):
    print("filepath")


if __name__=="__main__":
    app = web.application(urls,globals())
    app.run()
