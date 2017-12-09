import shelve
from cryptography.fernet import Fernet



def Save_Encryption_Key():
    # To save the encrytion_key that is shared between Authentication server and Server
    encrytion_key_file = shelve.open("Encrytion_Key_File.dat")
    secret_key = Fernet.generate_key()
    try:
        encrytion_key_file['1'] = secret_key
    finally:
        encrytion_key_file.close()

    print("success")


if __name__ == "__main__":
    Save_Encryption_Key()
