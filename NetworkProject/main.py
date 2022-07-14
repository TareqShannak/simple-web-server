from socket import *

data = []


def readfile():
    """Read the data of smartphones from the txtfile.txt"""
    file = open("txtfile.txt", "r")  # create file that read from input
    info = file.readlines()  # read line by line from file and put the data in info
    for line in info:  # split the data from file and append it in another list
        li = line.split(";")
        li[1] = str(li[1]).replace("\n", "")  # Remove the newline signal
        li[1] = int(li[1])
        data.append(li)


readfile()
serverPort = 9000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    print("IP: " + addr[0] + ", Port: " + str(addr[1]))
    print(sentence)
    ip = addr[0]
    port = addr[1]
    string_list = sentence.split(' ')  # Split request from spaces
    method = string_list[0]
    requestFile = string_list[1]
    connectionSocket.send(f"HTTP/1.1 200 OK\r\n".encode())
    myfile = requestFile.split('?')[0]  # After the "?" symbol not relevent here
    myfile = myfile.lstrip('/')
    try:
        if myfile == '':
            myfile = 'index.html'  # Default File
        elif myfile == 'sortName' or myfile == 'sortPrice':
            # if the user requests to sort the smartphones, it will enter this IF condition
            if myfile == 'sortName':
                # Sort the data according to the names of the smartphones ascending
                data.sort()
                outstring = '<html><head><style>#phones {font-family: Arial, Helvetica, sans-serif;text-align:center;border-collapse: collapse;width: 50%;}  #phones td, #phones th {border: 1px solid #ddd;padding: 8px;}  #phones tr:nth-child(even){background-color: #f2f2f2;}  #phones tr:hover {background-color: #ddd;}  #phones th {padding-top: 12px;padding-bottom: 12px;text-align: left;text-align:center;color: white;}</style></head><body><center><h1>Sort By Name</h1><table id="phones"><tr style="background-color: #4CAF50;"><th>Logo</th><th>Name</th><th>Price</th></tr>'
            else:
                # Sort the data according to the prices of the smartphones ascending
                data.sort(key=lambda data: data[1])
                outstring = '<html><head><style>#phones {font-family: Arial, Helvetica, sans-serif;text-align:center;border-collapse: collapse;width: 50%;}  #phones td, #phones th {border: 1px solid #ddd;padding: 8px;}  #phones tr:nth-child(even){background-color: #f2f2f2;}  #phones tr:hover {background-color: #ddd;}  #phones th {padding-top: 12px;padding-bottom: 12px;text-align: left;text-align:center;color: white;}</style></head><body><center><h1>Sort By Price</h1><table id="phones"><tr style="background-color: #4CAF50;"><th>Logo</th><th>Name</th><th>Price</th></tr>'

            # We will use sorted.html to show our sorted data
            myfile = 'sorted.html'
            for smartphone in data:
                # FOR loop used to check every smartphone in data list
                # and the next IF condition used to put a company logo for each smartphone in html file
                if str(smartphone[0]).startswith("Nokia"):
                    outstring += '<tr><th style="width: 10%"><img src="Nokia.png" style="width: 50px"></th>'
                elif str(smartphone[0]).startswith("IPhone"):
                    outstring += '<tr><th style="width: 10%"><img src="IPhone.png" style="width: 50px"></th>'
                elif str(smartphone[0]).startswith("Samsung"):
                    outstring += '<tr><th style="width: 10%"><img src="Samsung.png" style="width: 50px"></th>'
                else:
                    outstring += '<tr><th style="width: 10%"><img src="Huawei.png" style="width: 50px"></th>'
                outstring += '<td>' + smartphone[0] + '</td><td>$' + str(smartphone[1]) + '</td></tr>'
            outstring += "</table></center></body></html>"
            # sorted.html will be opened and overwritten by the string 'outstring'
            f = open("sorted.html", "w")
            f.write(outstring)
            f.close()
        # Now we will open and read the requested file in byte format
        requestFile = open(myfile, 'rb')
        response = requestFile.read()
        requestFile.close()
        # The following IF condition is to specify the type of the requested file
        if myfile.endswith(".jpg"):
            connectionSocket.send(f"Content-Type: image/jpeg \r\n".encode())
        elif myfile.endswith(".png"):
            connectionSocket.send(f"Content-Type: image/png \r\n".encode())
        elif myfile.endswith(".css"):
            connectionSocket.send(f"Content-Type: text/css \r\n".encode())
        else:
            connectionSocket.send(f"Content-Type: text/html \r\n".encode())
    except Exception as e:
        # When an exception handled, it will return a simple HTML with our IDs
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = (
                '<html><title>Error</title><body><center><h1>Error 404: Not found</h1><hr><p style= "font-weight: bold;">Waseem Sayara - 1182733</p><p style= "font-weight: bold;">Tareq Shannak - 1181404</p><p style= "font-weight: bold;">Manal Abuelouf - 1173359</p><hr><h2>IP: ' + str(
            ip) + ', Port: ' + str(port) + '</h2></center></body></html>').encode('utf-8')
    connectionSocket.send(f"\r\n".encode())
    connectionSocket.send(response)
    connectionSocket.close()
