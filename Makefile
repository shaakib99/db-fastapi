push_to_docker_hub:
	cd deployment && chmod +x push-to-docker-hub.sh && ./push-to-docker-hub.sh

deploy_to_koyeb:
	cd ./deployment && chmod +x deploy-to-koyeb.sh && ./deploy-to-koyeb.sh