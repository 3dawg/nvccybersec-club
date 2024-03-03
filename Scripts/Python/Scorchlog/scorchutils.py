import os, socket, struct, time


#//////------------------------------Import our utility functions----------------------------------
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

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

def int_to_ip(int_ip):
    return socket.inet_ntoa(struct.pack('!I', int_ip))

def timestamp_to_date(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
