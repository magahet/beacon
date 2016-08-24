dev:
	ansible-playbook -i dev.yml deployment.yml
prod:
	ansible-playbook -i prod.yml deployment.yml
