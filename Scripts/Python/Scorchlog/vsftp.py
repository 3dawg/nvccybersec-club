import re

#//////------------------------------Analyze VSFTPD log--------------------------------------------------
def vsftpAnalyze(file_path):
    users = set()
    ips = set()
    user_downloads = {}
    user_downloads_info = {}
    user_uploads = {}  # Updated to store uploaded bytes
    user_uploads_info = {}
    user_directories = {}
    user_ip_map = {}
    username = None
    
    with open(file_path, 'r') as file:
        for line in file:
            username_match = re.search(r'\[(\w+)\]', line)
            if username_match:
                username = username_match.group(1)
                users.add(username)
            ip_matches = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)  # Extract IP addresses
            for ip in ip_matches:
                ips.add(ip)
                user_ip_map.setdefault(username, set()).add(ip)
            size_match = re.search(r'(\d+) bytes', line)
            if size_match:
                size = int(size_match.group(1))
                if 'UPLOAD' in line:
                    user_uploads.setdefault(username, 0)  # Initialize the uploaded bytes for the user
                    user_uploads[username] += size  # Accumulate the uploaded bytes for the user
                    upload_file = re.search(r'OK UPLOAD: Client ".*", "(.*)"', line)
                    if upload_file:
                        upload_filename = upload_file.group(1)
                        user_uploads_info.setdefault(username, []).append(upload_filename)  # Store uploaded file for the user
                elif 'DOWNLOAD' in line:
                    user_downloads.setdefault(username, 0)  # Initialize the uploaded bytes for the user
                    user_downloads[username] += size  # Accumulate the uploaded bytes for the user
                    download_file = re.search(r'OK DOWNLOAD: Client ".*", "(.*)"', line)
                    if download_file:
                        download_filename = download_file.group(1)
                        user_downloads_info.setdefault(username, []).append(download_filename)

            mkdir_match = re.search(r'OK MKDIR: Client "(.*?)", "(.*?)"', line)
            if mkdir_match:
                client_ip = mkdir_match.group(1)
                directory_path = mkdir_match.group(2)
                user_directories.setdefault(username, []).append(directory_path)
    print("-----------------------------------------VSFTPD Analysis-------------------------------------------------------")
    print("print = Print the user database information")
    print("down = Print how many bytes of information the user has downloaded")
    print("up = Print how many bytes of information the user has uploaded")
    print("uploads = Print the files that were uploaded by users in the log file")
    print("downloads = Print the files that were downloaded by users in the log file")
    print("directories = Print the directories that were created by users in the log file")
    print("unique = Print how many unique IP addresses were in the log file and corespond them with users")
    print("exit = Exit the program")

    while True:
        choice = input("scorchLog :: vsftpd> ")
        if choice == 'print':
            print("\tUsers:")
            for i, user in enumerate(users):
                print(f"\t{i + 1}. {user}")
        elif choice == 'exit':
            exit(0)
        elif choice == 'down':
          user = input("\tEnter the username to query: ")
          total_bytes_downloaded = user_downloads.get(user, 0)  # Retrieve the total bytes uploaded by the user
          print(f"\tTotal bytes downloaded by {user}: {total_bytes_downloaded} bytes")
        elif choice == 'up':
            user = input("\tEnter the username to query: ")
            total_bytes_uploaded = user_uploads.get(user, 0)  # Retrieve the total bytes uploaded by the user
            print(f"\tTotal bytes uploaded by {user}: {total_bytes_uploaded} bytes")
        elif choice == 'uploads':
            print("Files uploaded by users:")
            for user, files in user_uploads_info.items():
                print(f"User: {user}")
                for file in files:
                    print(f"\t- {file}")
        elif choice == 'downloads':
            print("Files downloaded by users:")
            for user, files in user_downloads_info.items():
                print(f"User: {user}")
                for file in files:
                    print(f"\t- {file}")
        elif choice == 'directories':
            print("Directories created by users:")
            for user, directories in user_directories.items():
                print(f"User: {user}")
                for directory in directories:
                    print(f"\t- {directory}")
        elif choice == "unique":
            for user, ips in user_ip_map.items():
                ip_list = ", ".join(ips)
                print(f"User: {user} IP Addresses: {ip_list}")
        else:
            print("Invalid choice. Please try again.")
