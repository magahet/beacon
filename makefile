dev:
	ansible-playbook -e 'host_key_checking=False' -i deploy/env/dev deploy/main.yml --tags webapp
dev-full:
	ansible-playbook -e 'host_key_checking=False' -i deploy/env/dev deploy/main.yml
prod-full:
	ansible-playbook -i deploy/env/prod deploy/main.yml
