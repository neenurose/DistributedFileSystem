import shelve

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
    insert_semaphore_file()
