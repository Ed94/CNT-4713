from itertools import islice;

import socket;



class Assignment2:

	age = 0;


	def __init__(self, age) :
		
		self.age = age;


	def sayWelcome(self, name) :

		print("Welcome to the assignment, " + name + "! " + "Havent seen you for " + str(self.age) + " years!");


	def doubleList(self, input) :
	
		inputLength    = len(input);
		inputHalfPoint = int(inputLength / 2);

		doubledList = list();

		for element in islice(input, 0, inputHalfPoint) :
		
			doubleString = element + element;

			doubledList.append(doubleString);

		postHalfOdd  = inputHalfPoint    ;
		postHalfEven = inputHalfPoint + 1;

		# Step odd.
		for element in islice(input, postHalfOdd, inputLength, 2) :

			doubledList.append(element);

		# Step even.
		for element in islice(input, postHalfEven, inputLength, 2) :

			doubledList.append(element);

		print(doubledList);

		return doubledList;


	def modifyString(self, name) :

		nameList = list(name);

		nameLength = len(name);

		print(nameList);

		index = 1;

		for element in nameList :

			print("Index: " + str(index));

			if (index % 3) == 0 and index >= 3 :

				nameList[index - 1] = element.upper();

				print(nameList);

			if (index % 4) == 0 and index >= 4 :

				if (index % 3) != 0  :

					nameList[index - 1] = element.lower();	

					print(nameList);

			if (index % 5) == 0 and index >= 5 :

				if (index % 3) != 0 or (index % 4) != 0 :

					nameList[index - 1] = " ";

					print(nameList);

			index = index + 1;

		return ''.join(nameList);


	def isGoodPassword(self, password) :

		if len(password) < 9 : 
			return False;

		lowerChars     = 0;
		upperChars     = 0;
		specialChars   = 0;
		numRequirement = 0;

		specialSet = [ '.', ',', '#', '(' ];

		for element in password :

			if element.isalpha() :

				if element.islower() :

					lowerChars  = lowerChars + 1;

				if element.isupper() :

					upperChars = upperChars + 1;

			if specialSet.count(element) > 0 :

				specialChars = specialChars + 1;

			if element.isnumeric() :

				numRequirement = 1;

		if lowerChars >= 2 or upperChars >= 3  and specialChars >= 2 or numRequirement != 0 :

			return True;

		else:
			
			return True;


	def connectTcp(self, host, port) :

		hostIP = None;

		try:
			
			hostIP = socket.gethostbyname(host);

		except socket.gaierror:

			print("Error resolving the host address.");

			return False;

		try:

			socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

			socketConnection.connect( (hostIP, port) );

			return True;

		except socket.error as what :

			print("Failed to create socket: " %(what) );

			return False;

