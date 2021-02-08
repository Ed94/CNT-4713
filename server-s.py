#!/usr/bin/env python3

import signal;
import socket;
import sys;
import time;



HostIP = "0.0.0.0";
Port   = int();
Data   = bytes();

SocketConnection = socket.socket;



Deadline  = 10.0;
BlockSize = 1024;



def Connect() :

	global Deadline, HostIP, Port, SocketConnection;

	SocketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

	SocketConnection.settimeout(Deadline);

	SocketConnection.bind( (HostIP, Port) );



def ListenForConnections() :

	global SocketConnection;

	persist = True;

	SocketConnection.listen(10);


	while persist :

		try :
			code = ProcessConnection();

			if code == 0 : 
				
				return;

			elif code == 2 : 
				
				raise RuntimeError("Timed out");

			time.sleep(0.1);

		except RuntimeError  as what : 

			sys.stderr.write("ERROR: " + repr(what) + "\n");	

			time.sleep(0.1);

		except Exception as what :

			sys.stderr.write("ERROR: " + repr(what) + "\n");		

			return;



def ProcessConnection() :

	global BlockSize, Data, Deadline, SocketConnection;

	connection, address = SocketConnection.accept();

	# print("Connection established with: ", address);

	Data = bytes();

	connection.send("accio\r\n".encode());

	timeTillCut = 0.0;

	deadlineForFirstMessage = time.time() + Deadline;

	persist = True;

	while persist :

		recivedData = bytes();

		recivedData = connection.recv(BlockSize);

		if recivedData : 

			deadlineForFirstMessage = 0.0;
			
			timeTillCut = time.time() + 0.1;

			# print("Recived: " + recivedData.decode("utf-8"));

			Data += recivedData;

			if Data == signal.SIGINT or Data.decode("utf-8") == "quit":

				# print("SIGINT recieved, exiting gracefully...");

				return 0;

		if (deadlineForFirstMessage > 0.0 and time.time() >= deadlineForFirstMessage) :

			# print("No more data recived within time, exiting gracefully");

			connection.close();

			return 2;

		elif (timeTillCut > 0.0 and time.time() >= timeTillCut) :

			persist = False;

	print(len(Data.decode("utf-8")));

	connection.close();

	return 1;



def Entrypoint() :

	global Port, SocketConnection;

	try: 

		Port = int(sys.argv[1]);

		Connect();	

		ListenForConnections();

		SocketConnection.close();

	except OverflowError as what :

		sys.stderr.write("ERROR: Invalid Port. Info: " + repr(what) + "\n");

		sys.exit(1);

	except socket.error as what :

		sys.stderr.write("ERROR: Could not establish socket connection: " + repr(what) + "\n");
		
		sys.exit(1);

	except Exception  as what :

		sys.stderr.write("ERROR: " + repr(what) + "\n");

		sys.exit(1);



if __name__ == '__main__':

	Entrypoint();

	sys.stdout.flush();