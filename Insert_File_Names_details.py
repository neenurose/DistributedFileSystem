import shelve

def update_directory_names_file():
    # To update the .dat file with new key data
    filename = input("Enter filename:")
    filepath = input("Enter file path:")
    port = input("Enter port:")
    names = shelve.open("Directory_names_file.dat")
    try:
        filepath = filepath + filename
        names[filename] = (port,filepath)
    finally:
        names.close()

    return "success"


if __name__ == "__main__":
    update_directory_names_file()
