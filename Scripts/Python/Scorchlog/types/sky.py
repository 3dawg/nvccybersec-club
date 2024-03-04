import struct
import scorchutils
import time

#------------------------------Analyze .sky file------------------------------

def options(header):
    print(scorchutils.colors.fg.cyan, "-----------------------------------------Sky File Analysis-----------------------------------------", scorchutils.colors.reset)
    for k, i in header.items():
        print(scorchutils.colors.fg.lightblue, k, scorchutils.colors.reset, i,)

def skyAnalyze(file_path):
    header = {
         #title, options
        "magicbytes": "   Print the magic bytes of the file",
        "version":  "      Print the version of the file",
        "filecreation": " Print the creation date of the file",
        "hostname": "     Print the hostname that coresponds with the file",
        "flag": "         Print the flag of the log",
        "entries": "      Print the number of entries in the file",
        "exit": "         Exit the program",
        }
    

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

            # print(f'\nSource IP: {scorchutils.int_to_ip(source_ip)}')
            # print(f'Destination IP: {scorchutils.int_to_ip(destination_ip)}')
            # print(f'Timestamp: {scorchutils.timestamp_to_date(timestamp)}')
            # print(f'Bytes Transferred: {bytes_transferred}')
    options(header)     

    while True:
        choice = input("scorchLog :: sky> ")

        match (choice):
            case 'magicbytes':
                print(f'Magic Bytes: {magic_bytes}')

            case 'version':
                print(f'Version: {version}')

            case 'filecreation':
                print(f'Creation Timestamp: {scorchutils.timestamp_to_date(creation_timestamp)}')
                
            case 'hostname':
                print(f'Hostname: {hostname}')

            case 'flag':
                print(f'Flag: {flag}')
                
            case 'entries':
                print(f'Number of entries: {num_entries}')

            case 'exit':
                exit(0)

            case _:
                print("Invalid choice, please try again")

