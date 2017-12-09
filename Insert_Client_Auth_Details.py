import shelve

def insert_client_auth_file():
    # To update the .dat file with username as key and password as value for client authentication
    username = input("Enter username: ")
    password = input("Enter password: ")

    client_auth_details = shelve.open("Client_Auth_Details.dat")
    try:
        client_auth_details[username] = password
    finally:
        client_auth_details.close()

    print("success")

if __name__ == "__main__":
    insert_client_auth_file()
