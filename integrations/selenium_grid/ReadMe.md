## Notes on using the Selenium Grid Hub

The Selenium Grid Hub allows you to distribute tests to run in parallel across multiple machines. Each machine can then run its own allocation of tests in parallel. This allows you to run an entire test suite quickly, which may be important if you have a lot of tests to run. Machines can be personal computers, data centers, or virtual machines in the cloud. You can also create your own virtual machine by using a tool such as Docker (see the [Docker ReadMe](https://github.com/mdmintz/SeleniumBase/blob/master/integrations/docker/ReadMe.md)).

### Running the Selenium Grid Hub

You may need to download selenium-server-standalone-2.48.2.jar (or the latest version) separately. That file is not present with this repository to save space. You can download that file from here:
* http://docs.seleniumhq.org/download/
or here:
* http://selenium-release.storage.googleapis.com/index.html?path=2.48/
Once you have downloaded the jar file, put it in this folder (the "grid_files" folder).

More detailed info about connecting to the Selenium Grid Hub can be found here:
* https://theintern.github.io/intern/#selenium-grid
and here:
* https://github.com/SeleniumHQ/selenium/wiki/Grid2
For even more information, look here:
* https://github.com/SeleniumHQ/selenium/wiki
