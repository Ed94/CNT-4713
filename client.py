#!/usr/bin/env python3

import argparse;
import socket;
import sys;



Persist = True;

Hostname = str();
Port     = int();
Filename = None;

HostIP           = int();
SocketConnection = None;



def ConnectTCP() :

	global HostIP;

	try:

		HostIP = socket.gethostbyname(Hostname);

		print("Host IP: " + HostIP);

	except socket.gaierror:

		sys.stderr.write("ERROR: Could not retieve host's address. \n");

		sys.exit(1);

	try:

		SocketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

		SocketConnection.connect( (HostIP, Port) );

		print("Sucessfuly connected.");

	except OverflowError as what :

		sys.stderr.write("ERROR: Invalid Port. Info: " + what + "\n");

	except socket.error as what :

		sys.stderr.write("ERROR: Could not establish socket connection: " + what.strerror + "\n");
		
		sys.exit(1);



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



def ProcessConnection() :

	deadline = 10.0;

	try :

		data = bytes();

		while Persist :
	
			SocketConnection.settimeout(deadline);

			data = SocketConnection.read();

			if (data) :
			
				print ("Recived: " + repr(data));

	except socket.error as what :

		sys.stderr.write("ERROR: Socket related..." + what.strerror + "\n");
		
		sys.exit(1);	



def EntryPoint() :

	ParseArguments();

	ConnectTCP();

	ProcessConnection();




if __name__ == '__main__':

	EntryPoint();

	sys.stderr.write("ERROR: client is not implemented yet\n")

	sys.exit(1);
