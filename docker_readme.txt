Follow these instructions for running tests in Docker on your machine:

1. Get the Docker Toolbox from https://www.docker.com/toolbox and install it.

2. Setup your Docker environment:
  $ docker-machine create --driver virtualbox default

3. Start up your Docker environment:
  $ docker-machine restart default

4. Configure your shell:
  $ eval "$(docker-machine env default)"

5. Go to the SeleniumBase home directory. (That's where "Dockerfile" is located)

6. Create your Docker image from your Dockerfile: (Get ready to wait awhile)
  $ docker build -t seleniumbase .

7. Run your Docker image: (The "-i" keeps you inside the Docker shell)
  $ docker run -i seleniumbase

8. Run the example test from inside your Docker shell: (Takes a few seconds)
  $ ./docker_test.sh

9. When you're satisfied, you may exit the Docker shell:
  $ exit

10. (Optional) Since Docker images and containers take up a lot of space, you may want to clean up your machine from time to time when they’re not being used:
http://stackoverflow.com/questions/17236796/how-to-remove-old-docker-containers
Here are a few of those cleanup commands:
$ docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi
$ docker rm 'docker ps --no-trunc -aq'

11. (Optional) More reading on Docker can be found here:
https://docs.docker.com/mac/started/
https://docs.docker.com/installation/mac/
https://docs.docker.com
