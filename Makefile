push_to_docker_hub:
	cd deployment && chmod +x push-to-docker-hub.sh && ./push-to-docker-hub.sh

deploy_to_render:
	cd ./deployment && chmod +x deploy.sh && ./deploy.sh