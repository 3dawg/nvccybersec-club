import struct
import scorchutils

#//////------------------------------Analyze .sky file--------------------------------------------------
def skyAnalyze(file_path):
    with open(file_path, 'rb') as f:
        # Parse header
        magic_bytes = f.read(8)
        version = struct.unpack('>B', f.read(1))[0]
        creation_timestamp = struct.unpack('>I', f.read(4))[0]
        hostname_length = struct.unpack('>I', f.read(4))[0]
        hostname = f.read(hostname_length).decode()
        flag_length = struct.unpack('>I', f.read(4))[0]
        flag = f.read(flag_length).decode()
        num_entries = struct.unpack('>I', f.read(4))[0]
        # Parse body
        print("Parsing host information...")
        for _ in range(num_entries):
            source_ip = struct.unpack('>I', f.read(4))[0]
            destination_ip = struct.unpack('>I', f.read(4))[0]
            timestamp = struct.unpack('>I', f.read(4))[0]
            bytes_transferred = struct.unpack('>I', f.read(4))[0]

            print(f'\nSource IP: {scorchutils.int_to_ip(source_ip)}')
            print(f'Destination IP: {scorchutils.int_to_ip(destination_ip)}')
            print(f'Timestamp: {scorchutils.timestamp_to_date(timestamp)}')
            print(f'Bytes Transferred: {bytes_transferred}')
           

        print("-----------------------------------------Sky File Analysis-------------------------------------------------------")
        print("magicbytes = Print the magic bytes of the file")
        print("version = Print the version of the file")
        print("filecreation = Print the creation date of the file")
        print("hostname = Print the hostname that coresponds with the file")
        print("flag = Print the flag of the log")
        print("entries = Print the number of entries in the file")
        print("exit = Exit the program")

    while True:
        choice = input("scorchLog :: sky> ")
        if choice == 'magicbytes':
            print(f'Magic Bytes: {magic_bytes}')
        elif choice == 'version':
            print(f'Version: {version}')
        elif choice == 'filecreation':
            print(f'Creation Timestamp: {timestamp_to_date(creation_timestamp)}')
        elif choice == 'hostname':
            print(f'Hostname: {hostname}')
        elif choice == 'flag':
            print(f'Flag: {flag}')
        elif choice == 'entries':
            print(f'Number of entries: {num_entries}')
        elif choice == 'exit':
            exit(0)
        else:
            print("Invalid choice, please try again")

