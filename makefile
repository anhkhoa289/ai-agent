PROJECT_ID=enspara
PROJECT_NUMBER=288271283983
REGION=asia-southeast1

REPOSITORY=apps
IMAGE_NAME=sm-agent
VERSION=0.0.1
ARTIFACT_REGISTRY_NAME=$(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)

PACK_BUILDER=paketobuildpacks/builder:base
PACK_BUILDER_JAMMY=paketobuildpacks/builder-jammy-base

GOOGLE_BUILDER=gcr.io/buildpacks/builder:latest

create:
	gcloud artifacts repositories create $(REPOSITORY) \
		--repository-format=docker \
    --location=$(REGION) \
    --project=$(PROJECT_ID)

pack-load:
	pack build \
		$(ARTIFACT_REGISTRY_NAME) \
		--builder $(PACK_BUILDER_JAMMY)

gcloud-build:
	gcloud builds submit \
		--async \
		--tag $(ARTIFACT_REGISTRY_NAME)
