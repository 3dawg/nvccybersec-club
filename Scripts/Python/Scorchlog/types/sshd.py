import scorchutils

def options(header):
    print(scorchutils.colors.fg.cyan, "-----------------------------------------SSHD Analysis-----------------------------------------", scorchutils.colors.reset)
    for k, i in header.items():
        print(scorchutils.colors.fg.lightblue, k, scorchutils.colors.reset, i,)

def analyze(file_path):
    header = {
       #title, options
       "print      ":" Print list of users attempted to authenticate",
       "success    ":" Print password accepts per ip user with ip address",
       "fail       ":" Print login fails per user with ip address",
       "port       ":" Print unique port numbers attempted to be connected on",
       "unique     ":" Print unique ip addresses",
       "exit       ":" Exit the program",
      }

    options(header)
    data = parse(file_path)
    while True:
        choice = input("scorchLog :: vsftpd> ")
        match choice:
            case 'print':
                getUsers(data, file_path)

            case 'success':
                getAccepted(data, file_path)

            case 'fail':
                getFailed(data, file_path)

            case 'port':
                getPorts(data, file_path)

            case 'unique':
                getUnique(data, file_path)

            case 'exit':
                exit(0)

            case _:
                print("Inavlid choice please try again")

def parse(file_path):
    ips, users, accepts, fails, ports = ([] for i in range(5))

    with open(file_path, 'r') as file:
        for line in file:

            #Failed and Accepted are lines with the only info I really need...
            if 'Failed' in line:
                if line.split(" ")[8] not in users:
                    users.append(line.split(" ")[8])

                if line.split(" ")[10] not in ips:
                    ips.append(line.split(" ")[10])

                if line.split(" ")[10] not in fails:
                    fails.append(line.split(" ")[10])
                
                if line.split(" ")[10] + ":" + line.split(" ")[12] not in ports:
                    ports.append(line.split(" ")[10] + ":" + line.split(" ")[12])

            if 'Accepted' in line:
                if line.split(" ")[10] not in ips:
                    ips.append(line.split(" ")[10])

                if line.split(" ")[10] not in accepts:
                    accepts.append(line.split(" ")[10])

    return [users, fails, accepts, ports, ips]
    

#All unique users 
def getUsers(data, file_path):
    print('Users:')
    for x in data[0]:
        print('\t', x)
   
#All failed attempts (ips) 
def getFailed(data, file_path):
    print('Fails:')
    for x in data[1]:
        print('\t', x)

#All successful attempts (ips)
def getAccepted(data, file_path):
    print('Successes:')
    for x in data[2]:
        print('\t', x)
   
#All connection attempts (ports per)
def getPorts(data, file_path):
    print('Ports:')
    for x in data[3]:
        print('\t', scorchutils.colors.fg.lightblue, x.split(":")[0], scorchutils.colors.reset, ":", scorchutils.colors.fg.green, x.split(":")[1], scorchutils.colors.reset)
    
#All unique ips
def getUnique(data, file_path):
    print('Unique IPs:')
    for x in data[4]:
        print('\t', x)
