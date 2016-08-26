dev:
	ansible-playbook -e 'host_key_checking=False' -i deploy/env/dev deploy/main.yml
prod:
	ansible-playbook -i deploy/env/prod deploy/main.yml
