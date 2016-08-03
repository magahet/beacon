all:
	ansible-playbook -K -i env.yml deployment.yml
