import shelve


def update_directory_names_file(filename):
    # To update the .dat file with new key data
    names = shelve.open("Directory_names_file.dat")
    try:
        filepath = "C:/Users/meenuneenu/Desktop/test/" + filename
        names[filename] = filepath
    finally:
        names.close()

    return "success"



if __name__ == "__main__":
    update_directory_names_file("test2.txt")
