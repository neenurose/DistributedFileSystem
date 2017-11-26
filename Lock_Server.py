import web
import os
import shelve
import Web_Changed

urls = (
'/file/lock/(.*)', 'lock_server'
)

class lock_server:
    def GET(self,filename):
        # To check the file passed is locked or not. If the file is locked, return locked. If file is not locked, return filename.
        # If '*' is passed, it returns all files which are not locked.

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
            return files_str

        if not filename:
            return "No file name found"

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
        return filename_not_locked


    def POST(self,filename):
        # To lock the file if it not filename_not_locked
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
        return lock_result


def get_file_path(filepath):
    print("filepath")


if __name__=="__main__":
    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=8082)
