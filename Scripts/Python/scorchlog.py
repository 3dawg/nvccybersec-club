from asyncio import sleep
import os
import re
import struct 
import argparse
import socket 

#//////------------------------------Import our utility functions----------------------------------

def check_string_in_file(file_path, target_string):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            if target_string in content:
                return f"'{target_string}' found in {file_path}"
            else:
                return f"'{target_string}' not found in {file_path}"
    except FileNotFoundError:
        return f"File {file_path} not found."

def valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

    
#//////------------------------------Analyze vsFTP log--------------------------------------------------

def vsftpAnalyze(file_path):
    print("Analyzing basic information about the log....")
    users = set()

# Dictionary to store user download information
    user_downloads = {}

    # Dictionary to store user upload information
    user_uploads = {}

    with open(file_path, 'r') as file:
        for line in file:
            username_match = re.search(r'\[(\w+)\]', line)  # Extract username enclosed within square brackets
            if username_match:
                username = username_match.group(1)
                users.add(username)  # Add the username to the set

    print("Users are now in the database, please query what you want")
    print("-----------------------------------------VSFTPD Analyis-------------------------------------------------------")
    print("print = Print the user database information")
    print("down = Print how many bytes of information the user has downloaded")
    print("up = Print how many bytes of information the user has uploaded")
    print("exit = Exit the program")

    with open(file_path, 'r') as file:
        for line in file:
            username_match = re.search(r'\[(\w+)\]', line)  # Extract username enclosed within square brackets
            if username_match:
                username = username_match.group(1)
                size_match = re.search(r'(\d+) bytes', line)  # Extract size information
                if size_match:
                    size = int(size_match.group(1))
                    if 'UPLOAD' in line:
                        user_uploads.setdefault(username, 0)
                        user_uploads[username] += size
                    elif 'DOWNLOAD' in line:
                        user_downloads.setdefault(username, 0)
                        user_downloads[username] += size

    while True:
        choice = input("scorchLog :: vsftpd> ")
        if choice == 'print':
            for i, user in enumerate(users):
                print("User {}: {}".format(i + 1, user))
        elif choice == 'exit':
            exit(0)
        elif choice == 'down':
            user = input("\tEnter the username to query: ")
            if user in user_downloads:
                print("\tBytes downloaded by {}: {} bytes".format(user, user_downloads[user]))
            else:
                print("\tUser '{}' not found in the database. Or they didn't download anything...".format(user))
        elif choice == 'up':
            user = input("\tEnter the username to query: ")
            if user in user_uploads:
                print("\tBytes uploaded by {}: {} bytes".format(user, user_uploads[user]))
            else:
                print("\tUser '{}' not found in the database. Or they didn't upload anything".format(user))
        else:
            print("Invalid choice. Please try again.")




if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(
                    prog='Scorchlog.py',
                    description='Makes log analysis a hell of a lot easier',
                    epilog='--------------written by chaossec--------------')
    parser.add_argument('-f', '--filename',  help='Path to the file taken as a string', type=str, required=True)   #file argument, need a exception if there is no such file.
    parser.add_argument('-t', '--type' , help='Type of log to process, current supported choices are VSFTP', type=str, required=True)   # specify type of log so that we can distinguish between them.
    args = parser.parse_args()

    # Now we go ahead and handle the logic of what type of log we are dealing with
    if args.type == "VSFTP":
        print("Now analyzing your vsftpd log file....")
        vsftpAnalyze(args.filename)
    else:
        print("Invalid or unsupported log type...please try again")
    
