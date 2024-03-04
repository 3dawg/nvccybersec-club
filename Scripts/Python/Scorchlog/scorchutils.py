import os, socket, struct, time

#------------------------------Global Utils----------------------------------

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



#------------------------------COLORS----------------------------------
class colors:
 
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
 
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
 
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
