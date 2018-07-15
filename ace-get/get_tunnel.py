def open_tunnel(uname,passwd,local_port,target_ip,target_port,jumphost_ip,jumphost_port):
	return SSHTunnelForwarder(
		(jumphost_ip, jumphost_port), # jumpserver
		ssh_username=uname,
		ssh_password=passwd,
		remote_bind_address=(target_ip, target_port), # target device
		local_bind_address=('0.0.0.0', local_port) # local port
	)