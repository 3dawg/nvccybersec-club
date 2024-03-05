import argparse, scorchutils, time, sys
sys.path.append('types')
import sky, vsftp, sshd

#------------------------------Main function------------------------------

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(
                    prog='Scorchlog.py',
                    description='Makes log analysis a hell of a lot easier',
                    epilog='--------------written by chaossec--------------')
    parser.add_argument('-f', '--filename',  help='Path to the file taken as a string', type=str, required=True)   #file argument, need a exception if there is no such file.
    parser.add_argument('-t', '--type' , help='Type of log to process, current supported choices are VSFTP, SKY', type=str, required=True)   # specify type of log so that we can distinguish between them.
    args = parser.parse_args()

    # Now we go ahead and handle the logic of what type of log we are dealing with, with a chill switch statement
    match (args.type):

        case 'VSFTP':
            print(scorchutils.colors.fg.lightred, "Now analyzing your vsftpd log file....", scorchutils.colors.reset)
            time.sleep(3)
            scorchutils.cls()
            vsftp.analyze(args.filename)

        case 'SKY':
            print(scorchutils.colors.fg.lightred, "Now analyzing your sky file....", scorchutils.colors.reset)
            time.sleep(3)
            scorchutils.cls()
            sky.analyze(args.filename)

        case 'SSHD':
            print(scorchutils.colors.fg.lightred, "Now analyzing your sshd file....", scorchutils.colors.reset)
            time.sleep(3)
            scorchutils.cls()
            sshd.analyze(args.filename)
            

            
        case _:
            print(scorchutils.colors.fg.lightred, "Invalid or unsupported log type...please try again", scorchutils.colors.reset)
