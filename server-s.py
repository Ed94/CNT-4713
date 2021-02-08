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

	# SocketConnection.setblocking(False);

	while persist :

		# SocketConnection.listen(10);

		print("Listening for incoming connections on: " + str(Port));

		ProcessConnection();

		# time.sleep(1);



def ProcessConnection() :

	global BlockSize, Data, Deadline, SocketConnection;

	connection, address = SocketConnection.accept();

	print("Connection established with: ", address);

	Data = bytes();

	connection.send("accio\r\n".encode());

	timeTillCut = time.time() + Deadline;

	persist = True;

	while persist :

		recivedData = bytes();

		recivedData = connection.recv(BlockSize);

		if recivedData : 

			print("Recived: " + recivedData.decode("utf-8"));

			timeTillCut += 0.1;

			Data += recivedData;

			if Data == signal.SIGINT :

				print("SIGINT recieved, exiting gracefully...");

				exit(0);

		if (time.time() >= timeTillCut) :

			print("Exiting persist loop.");

			persist = False;

	print(Data.decode("utf-8"));

	connection.close();



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

	exit(0);