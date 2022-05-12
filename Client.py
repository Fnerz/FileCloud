# File cloud by @Fnerz.-
# gituhiub: https://github.com/Fnerz

def main():
    import socket
    import os
    import sys
    import threading

    import colorama

    colorama.init(autoreset=True)

    # checking for console commands
    if len(sys.argv) == 1:
        # if no console commands are given IP and Port will receved as an input
        IP = input("IP: ")
        PORT = input("PORT: ")
    elif len(sys.argv) > 1:
        IP = sys.argv[1]
        PORT = sys.argv[2]

    #            0             1             2            3
    # Files[["Filename", "Filepassword", "Filesize", "Filebytes"]]

    #                 0                1             2
    #msg = ["command(get,upload)", "Filename", "Filepassword"] 


    # creating TCP socket
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT.connect((IP, int(PORT)))

    def show():
        CLIENT.send(bytes("show#=#", 'utf8'))
        all_items = CLIENT.recv(2048)
        all_items = str(all_items, 'utf8')
        all_items = all_items.split("/-/")
        for item in all_items:
            print(item)

    def cmd():
        while True:
            cmd = input(":")
            cmd = cmd.lower()
            if cmd  == "cls":
                os.system('cls')
            elif cmd == "q":
                sys.exit()

            elif cmd == "get" or cmd == "download":
                path = ""
                file_name = input("Filename: ")
                file_password = input("Filepassword: ")
                send_command = f'get#=#{file_name}#=#{file_password}'

                CLIENT.send(bytes(send_command, 'utf8'))
                print("waiting for file data...")

                file_string = CLIENT.recv(8192)
                print("Data recved")
                
                file_string = str(file_string,'utf8')
                file_string = file_string.split("#=#")
                
                if file_string[0] != "ERROR":

                    file_bytes = CLIENT.recv(int(file_string[2]))
        
                    print(colorama.Fore.GREEN + "File data succselfully receved") # butiffull

                    
                    path = input("Path(without filename): ")
                    name = input("Filename(including fileextention):")

                    if os.path.exists(path):
                        with open(f'{path}//{name}', "wb") as f:
                            print(type(file_bytes))
                            f.write(file_bytes)
                            print( colorama.Fore.GREEN + "File data has been writen to the selected file")

                elif file_string[0] == "ERROR":
                    print(colorama.Fore.RED + "ERROR\n")
                    print("An error occurred, check if the the name and password are right")
                    print('Hint: Use "Show" to see all the current uploaded files...')

            elif cmd == "upload":
                path = ""
                _ERROR = False
                path = input("Path(including filename and fileextantion): ")
                if os.path.exists(path) == True:
                    with open(path, "rb") as f:
                        file_bytes = f.read()
                        _ERROR = False
                
                elif os.path.exists != True:
                    _ERROR = True
                    print(colorama.Fore.RED + "ERROR\nPath does not exist")

                if _ERROR != True:
                    upload_name = input("Uploaded name: ")
                    file_password = input("File password: ")
                    file_size = os.path.getsize(path)

                    file_info = f'upload#=#{upload_name}#=#{file_password}#=#{int(file_size)}'
                    CLIENT.send(bytes(file_info, 'utf8'))
                    CLIENT.send(file_bytes)


            elif cmd == "show":
                show()

            elif cmd == "help" or cmd == "?":
                print("get/download = Download file from the server")
                print("upload       = Upload file to the server")
                print("show         = Shows all current uploaded files on the server")
                print("q            = quit")

            elif cmd == "rename":
                #show()
                print('"-" to cancel the removing proces')
                file_name = input("Name: ")
                file_password = input("Password: ")
                replace_name = input("New Name: ")

                if file_name != "-":
                    rename_string = f'rename#=#{file_name}{file_password}{replace_name}'
                    CLIENT.send(bytes(rename_string, 'utf8'))


            elif cmd == "remove" or cmd == "delete":
                #show()
                print('"-" to cancel the removing proces')
                remove_name = input("Name: ")
                file_password = input("Password: ")

                if remove_name != "-":
                    remove_string = f'remove#=#{remove_name}#=#{file_password}'
                    CLIENT.send(bytes(remove_string, 'utf8'))

    cmd_thread = threading.Thread(target=cmd)
    cmd_thread.start()

if'__main__' == __name__:
    main()