import shelve


def update_directory_names_file():
    # To update the .dat file with new key data
    filename = input("Enter filename:")
    filepath = input("Enter file path:")
    names = shelve.open("Directory_names_file.dat")
    try:
        filepath = filepath + filename
        names[filename] = filepath
    finally:
        names.close()

    return "success"

def insert_semaphore_file():
    # To update the .dat file with new key (filename) and semaphore value 0 - not locked, 1- locked
    filename = input("Enter filename:")
    lock = shelve.open("File_locks.dat")
    try:
        lock[filename] = 0
    finally:
        lock.close()

    print("success")



if __name__ == "__main__":
    update_directory_names_file()
    insert_semaphore_file()
