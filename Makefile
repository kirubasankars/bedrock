IMAGE="bedrock"

cleanup:
	yes | docker container prune
	docker run --rm --privileged -e OPERATION=cleanup -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

download_artifacts:
	docker run --privileged -e OPERATION=download_artifacts -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

bootstrap:
	docker run --rm --privileged -e OPERATION=bootstrap -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

update:
	docker run --rm --privileged -e OPERATION=update -e WORKSPACE=$(PWD)/workspace -e MAX_CONCURRENCY=2 -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

os_patching:
	docker run --rm --privileged -e OPERATION=os_patching -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

up:
	docker run --rm --privileged -e OPERATION=up -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

down:
	docker run --rm --privileged -e OPERATION=down -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

restart:
	docker run --rm --privileged -e OPERATION=restart -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

validate:
	docker run --rm --privileged -e OPERATION=validate -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

unseal:
	docker run --rm --privileged -e OPERATION=unseal -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

generate_session_token:
	@docker run --rm --privileged -e OPERATION=generate_session_token -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

run_command:
	docker run --rm --privileged -e OPERATION=run_command -e WORKSPACE=$(PWD)/workspace -e MAX_CONCURRENCY=1 -e IGNORE_ERROR=0 -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

setup_jenkins:
	docker run --rm --privileged -e OPERATION=jenkins -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)