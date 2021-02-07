#!/usr/bin/env python3

import signal;
import socket;
import sys;
import time;



HostIP = "0.0.0.0";
Port   = int();
Data   = None;

SocketConnection = socket.socket;

Deadline  = 10.0;
BlockSize = 1024;



def Connect() :

	global Deadline, HostIP, Port;

	SocketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

	SocketConnection.settimeout(Deadline);

	SocketConnection.bind(HostIP, Port);



def ListenForConnections() :

	persist = True;

	while persist :

		socket.listen();

		print("Listening for incoming connections on: " + str(Port));

		ProcessConnection();

		time.sleep(1);



def ProcessConnection() :

	global BlockSize, Deadline;

	connection, address = SocketConnection.accept();

	print("Connection established with: ", address);

	connection.send("accio\r\n");

	timeTillCut = time.time() + Deadline;

	persist = True;

	while persist :

		if (time.time() >= timeTillCut) :

			raise Exception("Connection timed out.");

		global Data; Data =+ connection.recv(BlockSize);

		if Data : 

			print("Recieved: " + repr(Data));

			if Data == signal.SIGQUIT :

				print("SIGQUIT recieved, exiting gracefully...");

				exit(0);

			if Data == signal.SIGTERM :

				print("SIGTERM recieved, exiting gracefully...");

				exit(0);

			if Data == signal.SIGINT :

				print("SIGINT recieved, exiting gracefully...");

				exit(0);

	connection.close();



def Entrypoint() :

	try: 

		Port = sys.argv[1];

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