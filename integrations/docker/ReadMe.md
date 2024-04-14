## Docker setup instructions for SeleniumBase

#### 1. Install the Docker Desktop:

You can get that from here:
https://www.docker.com/products/docker-desktop/

You might also want to install the Docker Engine:
https://docs.docker.com/engine/install/

#### 2. Go to the SeleniumBase home directory on the command line, which is where [Dockerfile](https://github.com/seleniumbase/SeleniumBase/blob/master/Dockerfile) is located. (This assumes you've already cloned the SeleniumBase repo.)

#### 3. Create your Docker image from your Dockerfile: (Get ready to wait awhile)

    docker build -t seleniumbase .

If running on an Apple M1/M2 Mac, use this instead:

    docker build --platform linux/amd64 -t seleniumbase .

M1/M2 Mac users should also see [StackOverflow.com/a/76586216/7058266](https://stackoverflow.com/a/76586216/7058266) to **Enable Rosetta in Docker Desktop**. (Otherwise **you will** encounter errors like this when Chrome tries to launch: `"Chrome failed to start: crashed."`)

#### 4. Run [the example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) with Chrome inside your Docker: (Once the test completes after a few seconds, you'll automatically exit the Docker shell)

    docker run seleniumbase ./run_docker_test_in_chrome.sh

#### 5. You can also enter Docker and stay inside the shell:

    docker run -i -t seleniumbase

#### 6. Now you can run the example test from inside the Docker shell:

    ./run_docker_test_in_chrome.sh

#### 7. When you're satisfied, you may exit the Docker shell:

    exit

#### 8. (Optional) Since Docker images and containers take up a lot of space, you may want to clean up your machine from time to time when they’re not being used:

Details on that can be found here:
http://stackoverflow.com/questions/17236796/how-to-remove-old-docker-containers

Here are a few of those cleanup commands:

    docker container prune
    docker system prune
    docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi
    docker rm 'docker ps --no-trunc -aq'

If you want to completely remove all of your Docker containers and images, use these commands: (If there's nothing to delete, those commands will return an error.)

    docker rm -f $(docker ps -a -q)
    docker rmi -f $(docker images -q)

For more cleanup commands, check out:
https://codefresh.io/blog/everyday-hacks-docker/

#### 9. (Optional) More reading on Docker can be found here:
* https://docs.docker.com
* https://docs.docker.com/get-started/
* https://docs.docker.com/docker-for-mac/
