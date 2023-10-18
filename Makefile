IMAGE="dbman"
JENKINS=192.168.1.177

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
	rsync -r $(PWD)/src/main/distro root@$(JENKINS):/
	rsync -r $(PWD)/workspace/nodes.txt root@$(JENKINS):/
	docker run --rm --privileged -e OPERATION=setup_jenkins -e WORKSPACE=$(PWD)/workspace -v $(PWD)/workspace:/workspace -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)
	git remote rm jenkins || true
	git remote add jenkins root@$(JENKINS):/build.git || true
	git push jenkins main:master || true

push:
	git push jenkins main:master || true

publish:
	docker tag $(IMAGE) $(JENKINS):5000/$(IMAGE):1.0
	docker push $(JENKINS):5000/$(IMAGE):1.0