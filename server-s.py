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
BlockSize = 10000;



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

		if ProcessConnection() == True :

			return;

		time.sleep(0.1);



def ProcessConnection() :

	global BlockSize, Data, Deadline, SocketConnection;

	connection, address = SocketConnection.accept();

	connection.settimeout(10);

	try:

		Data = bytes();

		connection.send("accio\r\n".encode());

		persist = True;

		timeTillCut = time.time() + 0.1;

		while persist :

			if time.time() > timeTillCut :

				break;

			recivedData = bytes();

			recivedData = connection.recv(BlockSize);

			if recivedData : 

				print ("Recieved: " + repr(Data));

				timeTillCut = time.time() + Deadline;

				Data += recivedData;

				if Data == signal.SIGINT or Data.decode("utf-8") == "quit":

					return True;

		print(len(Data.decode("utf-8")));

		connection.close();

		return False;

	except Exception  as what :

		if repr(what) == "timeout('timed out')" :

			sys.stderr.write("ERROR: " + repr(what) + "\n");

			connection.close();

			return False;

		sys.stderr.write("ERROR: " + repr(what) + "\n");

		return True;



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

	sys.exit(0);