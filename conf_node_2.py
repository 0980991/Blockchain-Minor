import os
import shutil
import re

# Define source and destination directories
source_dir = "./final-assignment"
dest_dir = "./node 2"

# Copy the folder
shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)

# Define file paths
server_file_final = os.path.join(source_dir, "src", "server.py")
client_file_final = os.path.join(source_dir, "src", "client.py")
server_file_node2 = os.path.join(dest_dir, "src", "server.py")
client_file_node2 = os.path.join(dest_dir, "src", "client.py")

# Function to replace port numbers in a file using regex
def replace_port_in_file(file_path, port_regex, new_port):
    with open(file_path, "r") as file:
        filedata = file.read()

    newdata = re.sub(port_regex, new_port, filedata)
    
    with open(file_path, "w") as file:
        file.write(newdata)

# Define regex patterns and new port values
server_port_regex = r"port=\d+"
client_port_regex = r"host, port = 'localhost', \d+"

# Replace text in final-assignment files
replace_port_in_file(server_file_final, server_port_regex, "port=5006")
replace_port_in_file(client_file_final, client_port_regex, "host, port = 'localhost', 5005")

# Replace text in node 2 files with opposite port numbers
replace_port_in_file(server_file_node2, server_port_regex, "port=5005")
replace_port_in_file(client_file_node2, client_port_regex, "host, port = 'localhost', 5006")

print("Files copied and modified successfully.")
