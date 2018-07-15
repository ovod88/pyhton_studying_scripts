from sshtunnel import SSHTunnelForwarder
import time
import paramiko
import sys
import subprocess as s
import os

def open_tunnel(uname,passwd,local_port,target_ip,target_port,jumphost_ip,jumphost_port):
		return SSHTunnelForwarder(
			(jumphost_ip, jumphost_port), # jumpserver
			ssh_username=uname,
			ssh_password=passwd,
			remote_bind_address=(target_ip, target_port), # target device
			local_bind_address=('0.0.0.0', local_port) # local port
		)
try:
	tunnel_to_stepping_stone = open_tunnel('a592344', 'salutation20!8', 60000,
																	'srvnssdalkia', 22, '193.56.47.104', 22)

	tunnel_to_srvn = open_tunnel('a592344', 't@0N19@1@@',60001,
															'10.128.168.29', 22, 'localhost', 60000)

	tunnel_to_stepping_stone.start()
	tunnel_to_srvn.start()

	session = paramiko.SSHClient()
	session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	session.connect('localhost', port=60001, username = 'adminatos', password = 'yJ5IbJg6eq')
	connection = session.invoke_shell()	

	connection.send("terminal length 0\n")
	time.sleep(1)
	connection.send('show closk\n')
	output = connection.recv(65535)
	print(output)

	session.close()
	tunnel_to_stepping_stone.stop()
	tunnel_to_srvn.stop()
except paramiko.AuthenticationException as e:
	print('Authenetication to device failed')
	print(e)
	s.Popen('taskkill /F /PID {0}'.format(os.getpid()), shell=True)