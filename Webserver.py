from socket import *  # Import socket module
import sys            # In order to terminate the program



# Create a TCP server socket, AF_INET is used for IPv4 protocols, SOCK_STREAM is used for TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
ServerPort = 80
# Bind the socket to server address and server port
serverSocket.bind(('',ServerPort))
# Listen to at most 1 connection at a time
serverSocket.listen(1)

done = False
# Server should be up and running and listening to the incoming connections
while done != True:
	print('The server is ready to receive')
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	
	#If an exception occurs during the execution of try clause, the rest of the clause is skipped
	#If the exception type matches the word after except, the except clause is executed
	try:
		# Receives the request message from the client
		message = connectionSocket.recv(1000)
		#print(message)

		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filename = message.split()[1].decode()
		
		# Because the extracted path of the HTTP request includes 
		# a character '\', we read the path from the second character 
		filename = filename[1 : len(filename)]
		#print("opening " + filename) 

		# Store the entire contenet of the requested file in a temporary buffer
		f = open(filename, "r")
		text = f.read()

  
		# Send the HTTP response header line to the connection socket
		response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
		connectionSocket.sendall(response.encode())

		# Send the content of the requested file to the connection socket
		connectionSocket.sendall(str(text).encode())		
		# Close the client connection socket
		connectionSocket.close()
		done = True
		
	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.sendall("HTTP/1.1 404 Not Found\n\nError 404: File not found :0".encode())          
		# Close the client connection socket
		connectionSocket.close()
		done = True
	

serverSocket.close()  
sys.exit() #Terminate the program after sending the corresponding data
