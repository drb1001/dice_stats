# Docker notes:


## Terms

- Image is the configuration of os, libraries, packages, etc (like a template or blueprint)
- Container is the process created when running a specific image
- Volume is a directory outside of a container to persist data (either mounted, or controlled by docker)


## Dockerfile

Dockerfile is the source code to build an image:
- Installs the os, configures the packages, copies project files etc
- Dockerfile is usually version controlled in github
- Built image is usually hosted on Docker Hub
- Dockerfile reference https://docs.docker.com/engine/reference/builder/

#### Syntax:
- Start from a base image (that has already been built): using `FROM` keyword - eg: `FROM python:3.7`
- Can copy files : using `COPY` keyword - eg: `COPY src/ /var/src/`
- Set the working directory using `WORKDIR` keyword
- Set a default command to run using `CMD` keyword
- Might need to expose ports using `EXPOSE` keyword - eg: `EXPOSE 8080`


## Build Image

- Create / Build an image from a Dockerfile:
  - `docker build -t <tags> <Dockerfile location>`


## Run an image

- `docker run <image name>:<tag>`
- eg `docker run ubuntu:latest`
- options:
  - to map/forward ports between host and container: `-p <host_port>:<container_port>`
  - to mount a directory between host and container (generally for dev only): `-v <host_directory>:<container_directory>`
  - to run in detached mode `--detach` or `-d`
Note: tries to find and installs if it's not available


# Docker compose

Docker compose is a config file to setup containers (so you don't have to type build, run etc each time)
Particularly useful for complex or multi-container apps

#### Syntax:
- `version` is the version of docker compose file syntax
- `services` starts the list of services that need to be started (ie images that need be run)
  - `build` is the directory containing the Dockerfile
  - `volumes` is the list of volumes (directories) to map
  - `ports` is the list of ports to forward
  - `image` if you don't need to build an image eg using something prebuilt, can use this instead
  - `environment` pass in environmental vars (eg from .env file)
- `volumes` is the list of 

#### Commands:
To run the docker-compose: `docker-compose up`
  - to force build use flag `--build`
  - to ensure no rebuild use flag `--no-build`
  - to run detached use flag `--detach`

To stop services: `docker-compose stop`

To stop and remove services: `docker-compose down`


# Managing things

- List running containers: `docker ps`
- Execute on a running container: `docker exec <container id> <command>``
- Stop a container `docker stop <container id>`
- Remove all stopped containers: `docker container prune`
- Remove all unused images: `docker image prune`
- Remove all unused local volumes: `docker volume prune`


## .dockerignore
Similar to git ignore, you can specify files etc that should not be included in build:
- secrets
- large files
- temporary files, caches, etc  



# Useful links:
 - Learn Docker in 12 Minutes - https://www.youtube.com/watch?v=YFl2mCHdv24
 - Docker Compose in 12 Minutes - https://www.youtube.com/watch?v=Qw9zlE3t8Ko
