# File cloud by @Fnerz.-
# gituhiub: https://github.com/Fnerz

def main():
    """
    Upcomming:
        -Step 2
            - adding fetures
                -renaming files

        
    Finished:
        -Step 1
            -basic setup
                -uploading and downloading from files
        -Step 2
            - adding fetures
                -securing files with a password
                -auto save
                -getting an overview wich files exsit
                -removing files from the server
    
    """

    import socket
    import os
    import sys
    import time
    import threading

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
    Files = []

    try:

        from Sever_Save_Dialog import Files
    
    except:
        with open("Sever_Save_Dialog.py", "w") as f:
            f.write(f'Files = {Files}')



    # creating TCP socket
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP, int(PORT)))
    SERVER.listen(10)

    def auto_save():
        while True:
            time.sleep(10)
            with open("Sever_Save_Dialog.py", "w") as f:
                f.write(f'Files = {Files}')

    # handeling thread
    def handel(conn, addr):
        while True:
            try:
                ERROR = False
                file_index = -1
                file_string = ""
                msg = conn.recv(1024)
                msg = str(msg, 'utf8')
                msg = msg.split("#=#")

                #                 0                1             2
                #msg = ["command(get,upload)", "Filename", "Filepassword"] 
                if msg[0] == "get":
                    # checking if the wannted file is uploaded
                    for index ,file_list in enumerate(Files):
                        #print(file_list[0])
                        if file_list[0] == msg[1]:
                            file_index = index
                        
                    
                    # chekcing if an error occured
                    if file_index == -1:
                        # if yes an error msg will be send back
                        conn.send(bytes("ERROR", 'utf8'))
                        ERROR = True

                    # if evrything went smoth, all the requierd date will be gaint and sent back to the user
                    if ERROR == False:
                        file_list = Files[file_index]
                        if file_list[1] == msg[2]:
                            for stringer in range(3):
                                file_string += f"{file_list[stringer]}#=#"
                            conn.send(bytes(file_string, "utf8"))
                            time.sleep(.01)
                            conn.send(file_list[3])
                            print(f'{addr} DOWNLOADED {file_list[0]}')
                
                elif msg[0] == "upload":
                    file_list = ["", "", "", ""]
                    #msg = ["command", "Filename", "Filepassword", "Filesize"]
                    file_bytes = conn.recv(int(msg[3]))
                    
                    print(msg)
                    file_list[0] = msg[1]
                    file_list[1] = msg[2]
                    file_list[2] = msg[3]
                    file_list[3] = file_bytes
                    
                    
                    Files.append(file_list)
                    print(f'{addr} UPLOADED {file_list[1]}')
                    

                elif msg[0] == "show":
                    all_items = ""
                    for file in Files:
                        all_items += f"{file[0]}/-/"
                    
                    
                    conn.send(bytes(all_items, 'utf8'))
                
                elif msg[0] == "remove":
                    # searching for the right file
                    for index ,file_list in enumerate(Files):
                        
                        if file_list[0] == msg[1]:
                            if file_list[1] == msg[2]:
                                Files.pop(index)

                elif msg[0] == "rename":
                    for index ,file_list in enumerate(Files):
                        
                        if file_list[0] == msg[1]:
                            if file_list[1] == msg[2]:
                                file_list[0] = msg[3]



            except:
                print(f'{addr} disconnected')
                return

    # accept thread
    def acp():
        while True:
            conn, addr = SERVER.accept()

            handel_thread = threading.Thread(target=handel, args=(conn, addr))
            print(f'{addr}connected')
            handel_thread.start()



    acp_thread = threading.Thread(target=acp)
    acp_thread.start()

    auto_save_thread = threading.Thread(target=auto_save)
    auto_save_thread.start()

if "__main__" == __name__:
    main()