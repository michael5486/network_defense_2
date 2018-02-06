import sys
import getopt
import hashlib

######################################################################################################
#
#  print_DGA_domains.py
#    Copyright 2016 - Matthew Norris
#
#  Simple Python boilerplate to wrap the provide_generated_domain function in a calling program.
#    Please modify as need be, but describe all changes in your writeup.
#
#  Last Modified: 20160106 - MJN
#
######################################################################################################

def provide_generated_domain(date,iter):
	# create list of TLDs that will be chosen later
	tlds = ['com','net','org','ru','cn','tv']
	
	# iterate through the number of domains requested
	# create a string that is the date passed in and the interation number
	string_to_hash = date + "-" + str(iter)
	# create the MD5 hash
	hash = hashlib.md5()	
	hash.update(string_to_hash)
	hashed_string = hash.hexdigest()
	# determine the length of the domain 
	#   generated based on the numeric value of the first character (mod 10)
	length = ord(hashed_string[:1])%10 + 12
	# build the final domain 
	#   the first 'length' characters and the TLD determined on the first character (mod 6)
	return hashed_string[:length]+"."+tlds[ord(hashed_string[:1])%6]

def usage():
	print "\nprint_DGA_domains.py\n\tA wrapper program to run the DGA function\n\n\t-h | --help\tThis message\n\t--date\t\tThe date to generate for\n\t--count\t\tThe number of entries to generate (default: 10)\n"

def main(argv):

	try:
		opts,args = getopt.getopt(argv, "h", ["help", "date=", "count="])
	except getopt.GetoptError:
		usage()
		sys.exit()
	
	date = ''
	count = 10
	
	for opt,arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
	        elif opt in ("--date"):
			date = arg
	        elif opt in ("--count"):
			count = int(arg)
		else:
			assert False, "unhandled option"

	if date:
		for i in range(1,count):
			print provide_generated_domain(date,i)
	else:
		usage()
		sys.exit() 

if __name__ == "__main__":
	main(sys.argv[1:])
