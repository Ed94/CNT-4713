#!/usr/bin/env python3

import argparse;
import socket;
import sys;



Persist = True;

Hostname = str();
Port     = int();
Filename = None;

HostIP           = int();
SocketConnection = socket.socket;

File = None;
Data = bytes();



def WriteToFile() :

	global File;

	if (File == None) :

		File = open(Filename, "wb");

	try :

		global Data;

		File.write(Data);



def ProcessConnection() :

	deadline = 10.0;

	try :

		SocketConnection.settimeout(deadline);

		while Persist :

			global Data;

			Data = SocketConnection.recv(1024);

			if (Data) :
			
				print ("Recived: " + repr(Data));

				WriteToFile();

	except socket.error as what :

		sys.stderr.write("ERROR: Socket related..." + what.strerror + "\n");
		
		sys.exit(1);



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

		ProcessConnection();

	except OverflowError as what :

		sys.stderr.write("ERROR: Invalid Port. Info: " + repr(what) + "\n");

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



def EntryPoint() :

	ParseArguments();

	ConnectTCP();



if __name__ == '__main__':

	EntryPoint();

	sys.stderr.write("ERROR: client is not implemented yet\n")

	sys.exit(1);
