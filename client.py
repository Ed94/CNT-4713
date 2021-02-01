#!/usr/bin/env python3

import argparse;
import io;
import socket;
import sys;
import time;



Hostname = str();
Port     = int();
Filename = None;

SocketConnection = socket.socket;

File = io.TextIOWrapper;
Data = bytes();



def ProcessConnection() :

	deadline = 10.0;

	SocketConnection.settimeout(deadline);

	Persist = True;

	timeTillCut = time.time() + deadline;

	while Persist :

		if (time.time() >= timeTillCut) :

			raise Exception("Timed out");

		global Data;

		Data += SocketConnection.recv(1024);

		if (Data) :
		
			print ("Recived: " + repr(Data));
			
			if (Data.decode("utf-8") == "accio\r\n") :

				global File;

				SocketConnection.send( File.read() );

				Persist = False;

			if (len(Data.decode("utf-8")) > len("accio\r\n")) :

				Data = bytes();



def ConnectTCP() :

	global SocketConnection;

	HostIP = socket.gethostbyname(Hostname);

	print("Host IP: " + HostIP);

	SocketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

	SocketConnection.settimeout(10);

	SocketConnection.connect( (HostIP, Port) );



def ParseArguments() :

	global Hostname;
	global Port;
	global Filename;

	Hostname = sys.argv[1];
	Port     = int(sys.argv[2]);
	Filename = sys.argv[3];

	print("HostName: " + Hostname );
	print("Port    : " + str(Port));
	print("Filename: " + Filename );



def EntryPoint() :

	ParseArguments();

	try : 

		global File;

		File = open(Filename, "rb");

		ConnectTCP();

		print("Sucessfuly connected.");

		ProcessConnection();

		File.close();

		sys.exit(0);

	except socket.gaierror:

		sys.stderr.write("ERROR: Could not retieve host's address. \n");

		sys.exit(1)

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

	EntryPoint();

	sys.stderr.write("ERROR: client is not implemented yet\n")

	sys.exit(1);
