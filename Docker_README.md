## Docker setup instructions for SeleniumBase

#### 1. Get the Docker Toolbox from https://www.docker.com/toolbox and install it.

#### 2. Setup your Docker environment:

    docker-machine create --driver virtualbox default

#### 3. Start up your Docker environment:

    docker-machine restart default

#### 4. Configure your shell:

    eval "$(docker-machine env default)"

#### 5. Go to the SeleniumBase home directory. (That's where "Dockerfile" is located)

#### 6. Create your Docker image from your Dockerfile: (Get ready to wait awhile)

    docker build -t seleniumbase .

#### 7. Run a test inside your Docker: (Once the test completes after a few seconds, you'll automatically exit the Docker shell)

    docker run seleniumbase ./run_docker_test_in_firefox.sh

#### 8. You can also enter Docker and stay inside the shell:

    docker run -i -t seleniumbase

#### 9. Now you can run the example test from inside the Docker shell: (This time using PhantomJS)

    ./run_docker_test_in_phantomjs.sh

#### 10. When you're satisfied, you may exit the Docker shell:

    exit

#### 11. (Optional) Since Docker images and containers take up a lot of space, you may want to clean up your machine from time to time when they’re not being used:
http://stackoverflow.com/questions/17236796/how-to-remove-old-docker-containers
Here are a few of those cleanup commands:

    docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi
    docker rm 'docker ps --no-trunc -aq'

If you want to completely remove all of your docker containers and images, use these commands: (If there's nothing to delete, those commands will return an error.)

    docker rm $(docker ps -a -q)
    docker rmi $(docker images -q)

#### 12. (Optional) More reading on Docker can be found here:
* https://docs.docker.com
* https://docs.docker.com/mac/started/
* https://docs.docker.com/installation/mac/
