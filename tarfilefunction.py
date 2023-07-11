import tarfile

# Declaring the filename
name_of_file = "framesclass2.tar"

# Opening the file in write mode
file = tarfile.open(name_of_file, "w")

# Adding other files to the tar file
file.add("frame&class")

# Closing the file
file.close()