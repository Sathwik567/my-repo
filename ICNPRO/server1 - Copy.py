import socket
import pickle
import time

s = socket.socket()
host = ""
port = 9999
matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# print(matrix)

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()
playerName = list()         


def validate_input(x, y, conn):
    if x > 3 or y > 3:
        print("\nOut of bound! Enter again...\n")
        conn.send("Error")
        return False
    elif matrix[x][y] != 0:
        print("\nAlready entered! Try again...\n")
        conn.send("Error")
        return False
    return True

def get_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "Player One's Turn"
        conn = playerConn[0]
    else:
        player = "Player Two's Turn"
        conn = playerConn[1]
    print(player)
    send_common_msg(player)
    failed = 1
    while failed:
        try:
            conn.send("Input")
            data = conn.recv(2048 * 10)
            conn.settimeout(20)
            dataDecoded = data.split(",")
            x = int(dataDecoded[0])
            y = int(dataDecoded[1])
            if validate_input(x, y, conn):
                matrix[x][y] = currentPlayer
                failed = 0  
                send_common_msg("Matrix")
                send_common_msg(str(matrix))
        except:
            conn.send("Error")
            print("Error occured! Try again..")

        

def check_rows():
    # print("Checking rows")
    result = 0
    for i in range(3):
        if matrix[i][0] == matrix[i][1] and matrix[i][1] == matrix[i][2]:
            result = matrix[i][0]
            if result != 0:
                break
    return result

def check_columns():
    # print("Checking cols")
    result = 0
    for i in range(3):
        if matrix[0][i] == matrix[1][i] and matrix[1][i] == matrix[2][i]:
            result = matrix[0][i]
            if result != 0:
                break
    return result

def check_diagonals():
    # print("Checking diagonals")
    result = 0
    if matrix[0][0] == matrix[1][1] and matrix[1][1] == matrix[2][2]:
        result = matrix[0][0]
    elif matrix[0][2] == matrix[1][1] and matrix[1][1] == matrix[2][0]:
        result = matrix[0][2]
    return result

def check_winner():
    result = 0
    result = check_rows()
    if result == 0:
        result = check_columns()
    if result == 0:
        result = check_diagonals()
    return result

#Socket program
def start_server():
    #Binding to port 9999
    #Only two clients can connect 
    try:
        s.bind((host, port))
        print("Tic Tac Toe server started \nBinding to port", port)
        s.listen(2) 
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)
    

#Accept player
#Send welcome msg
#Receive name
def accept_players():
    try:
        welcome = "Welcome to Tic Tac Toe Server"
        for i in range(2):
            conn, addr = s.accept()
            conn.send(welcome)
            name = conn.recv(2048 * 10)

            playerConn.append(conn)
            playerAddr.append(addr)
            playerName.append(name)
            print("Player {} - {} [{}:{}]".format(i+1, name, addr[0], str(addr[1])))
            conn.send("Hi {}, you are player {}".format(name, str(i+1)))
        
        start_game()
        s.close()
    except socket.error as e:
        print("Player connection error", e)   
    except:
        print("Error occurred")

def start_game():
    result = 0
    i = 0
    while result == 0 and i < 9 :
        if (i%2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        result = check_winner()
        i = i + 1
        # print("Current count", i ,result == 0 and i < 9, "Result = ", result)
    
    if result == 1:
        lastmsg = "Player one - {} is the winner".format(playerName[0])
    elif result == 2:
        lastmsg = "Player two - {} is the winner".format(playerName[1])
    else:
        lastmsg = "Draw"

    send_common_msg(lastmsg)
    time.sleep(10)
    for conn in playerConn:
        conn.close()
    

def send_common_msg(text):
    playerConn[0].send(text)
    playerConn[1].send(text)
    time.sleep(1)

start_server()
