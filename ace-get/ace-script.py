from get_keepass import get_keepass as get_pass
import time
import paramiko
import subprocess as s
import os
from concurrent.futures import ThreadPoolExecutor
from sshtunnel import SSHTunnelForwarder
from paramiko.ssh_exception import SSHException
import traceback
import json

def enumerate2(xs, start=0, step=1):
    for x in xs:
        yield (start, x)
        start += step

def get_credentials():
	passwords = []
	with open('keepass_names.txt', 'r') as file:
		lines = file.readlines()

		parsed_keepass_file = {key.strip():value.strip() for (key, value) in list(map(lambda x: x.split(":"), lines))}

		stepping_stone_pass = get_pass(parsed_keepass_file['stepping_stone_password'])
		srvn_pass = get_pass(parsed_keepass_file['srvn_password'])
		device_username = parsed_keepass_file['device_username']
		device_pass = get_pass(parsed_keepass_file['device_password'])



	return {
		'username'                : parsed_keepass_file['username'],
		'stepping_stone_password' : stepping_stone_pass,
		'srvn_password'           : srvn_pass,
		'device_username'         : device_username,  
		'device_password'         : device_pass 
	}

def devices():
	devices = []
	with open('devices.txt', 'r') as file:
		lines = file.readlines()

	# print(lines)
	for line in lines:
		device = {}
		device['ip'] = line.split(';')[0].strip()
		device['name'] = line.split(';')[1].strip()
			
		devices.append(device)	

	return devices

def commands():
	with open('commands.txt', 'r') as file:
		lines = file.readlines()

	return lines

def contexts():
	with open('contexts.txt', 'r') as file:
		lines = file.readlines()
		lines = list(map(lambda x: x.strip(), lines))

	return lines

def open_tunnel(uname, passwd, local_port, target_ip, target_port, jumphost_ip, jumphost_port):
		return SSHTunnelForwarder(
			(jumphost_ip, jumphost_port), # jumpserver
			ssh_username=uname,
			ssh_password=passwd,
			remote_bind_address=(target_ip, target_port), # target device
			local_bind_address=('0.0.0.0', local_port) # local port
		)

def tunnel_connect(device, port):
	result =  ''

	with open_tunnel(device['credentials']['username'], device['credentials']['stepping_stone_password'], 
											device['LOCAL_PORT'], 'srvnssdalkia', 22, '193.56.47.104', 22) as tunnel1:

		with open_tunnel(device['credentials']['username'], device['credentials']['srvn_password'],
											device['LOCAL_PORT'] + 1, device['ip'], port, 'localhost', device['LOCAL_PORT']) as tunnel2:

			session = paramiko.SSHClient()
			session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			session.connect('localhost', port=device['LOCAL_PORT'] + 1, username = device['credentials']['device_username'], 
															password = device['credentials']['device_password'])

			connection = session.invoke_shell()
			stdin = connection.makefile('wb')
			stdout = connection.makefile('rb')

			stdin.write("terminal length 0\n")
			time.sleep(1)

			def execute_commands(context='Admin'):
				for command in device['commands']:
					stdin.write(command + '\n')
					time.sleep(5)
					print('Executing command ' + command + ' inside ' + context + ' for ' + device['name'] + '\n')
					print('-----------------------------')
			
			execute_commands()

			for context in device['contexts']:
				stdin.write('changeto ' + context + '\n')
				time.sleep(1)
				execute_commands(context)

			stdin.write("exit\n")

			result = stdout.read().decode("utf-8")

			stdout.close()
			stdin.close()
			session.close()

			# print(result)
			print('Ramasse pour ' + device['name'])

	result = result.replace('\r', '')
	with open(device['name'] + '.txt', 'w') as file:
		print('Saving output for ' + device['name'])
		file.write(result)

def connect(device):
	try:
		return tunnel_connect(device, 22)
	except SSHException:
		try:
			return tunnel_connect(device, 23)
		except Exception as e:
			traceback.print_tb(e.__traceback__)
			return 'SSH and telnet refused'
	except Exception as e:
		traceback.print_tb(e.__traceback__)
		return e

def threads_conn(function, devices):
	with ThreadPoolExecutor(max_workers=5) as executor:
		result = executor.map(function, devices)
	return list(result)


if __name__ == '__main__':
	credentials = get_credentials()

	# credentials = {'username': 'a592344', 'stepping_stone_password': 'salutation20!8', 
	# 				'srvn_password': 't@0N19@1@@', 'device_username': 'adminatos', 
	# 				'device_password': 'yJ5IbJg6eq'}
	try:
		devices = devices()
		commands = commands()
		contexts = contexts()


		for index, device in enumerate2(devices, 60000, 2):
			device['LOCAL_PORT']  = index
			device['commands']    = commands
			device['contexts']    = contexts
			device['credentials'] = credentials

		threads_conn(connect, devices)

	except Exception as e:
		traceback.print_tb(e.__traceback__)
		print(e)
		print('Something wrong happened with tunnels')
		s.Popen('taskkill /F /PID {0}'.format(os.getpid()), shell=True)
