#!/usr/bin/env python3

import argparse;
import io;
import socket;
import sys;



Persist = True;

Hostname = str();
Port     = int();
Filename = None;

HostIP           = int();
SocketConnection = socket.socket;

File = io.TextIOWrapper;
Data = bytes();



def ProcessConnection() :

	deadline = 10.0;

	SocketConnection.settimeout(deadline);

	while Persist :

		global Data;

		Data = SocketConnection.recv(1024);

		if (Data) :
		
			print ("Recived: " + repr(Data));

			if (Data == "accio\r\n") :

				SocketConnection.send( File.read() );



def ConnectTCP() :

	global HostIP;
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

		File = open(Filename, "rb");

		ConnectTCP();

		print("Sucessfuly connected.");

		ProcessConnection();

		File.close();

	except socket.gaierror:

		sys.stderr.write("ERROR: Could not retieve host's address. \n");

		sys.exit(1)

	except OverflowError as what :

		sys.stderr.write("ERROR: Invalid Port. Info: " + repr(what) + "\n");

		sys.exit(1);

	except socket.error as what :

		sys.stderr.write("ERROR: Could not establish socket connection: " + what.strerror + "\n");
		
		sys.exit(1);

	except Exception  as what :

		sys.stderr.write("ERROR: " + repr(what) + "\n");

		sys.exit(1);



if __name__ == '__main__':

	EntryPoint();

	sys.stderr.write("ERROR: client is not implemented yet\n")

	sys.exit(1);
