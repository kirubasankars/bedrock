IMAGE="dbman"
JENKINS=192.168.1.124

build:
	docker build -t $(IMAGE) ./src/main

cleanup:
	yes | docker container prune
	docker run --rm --privileged -e OPERATION=cleanup -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

download_artifacts:
	docker run --rm --privileged -e OPERATION=download_artifacts -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

bootstrap:
	docker run --rm --privileged -e OPERATION=bootstrap -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

update:
	docker run --rm --privileged -e OPERATION=update -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

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

run_command:
	docker run --rm --privileged -e OPERATION=run_command -e WORKSPACE=$(PWD)/workspace -e MAX_CONCURRENCY=1 -e IGNORE_ERROR=0 -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

setup_jenkins:
	docker run --rm --privileged -e OPERATION=jenkins -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

push:
	rsync -a -r $(PWD)/workspace root@$(JENKINS):/
	ssh root@$(JENKINS) "chown -R agent:agent /workspace"
	git remote rm jenkins || true
	git remote add jenkins root@$(JENKINS):/build.git || true
	git push -f jenkins -f main:master || true

publish:
	docker tag $(IMAGE) $(JENKINS):5000/$(IMAGE):1.0
	docker push $(JENKINS):5000/$(IMAGE):1.0