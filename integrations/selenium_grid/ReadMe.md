## Notes on using the Selenium Grid Hub

The Selenium Grid Hub allows you to distribute tests to run in parallel across multiple machines. Each machine can then run its own allocation of tests in parallel. This allows you to run an entire test suite quickly, which may be important if you have a lot of tests to run. Machines can be personal computers, data centers, or virtual machines in the cloud. You can also create your own virtual machine by using a tool such as Docker (see the [Docker ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/docker/ReadMe.md)).

### Running the Selenium Grid Hub

First, download the latest selenium-server-standalone jar file to this folder (integrations/selenium_grid):
```bash
python download_selenium.py
```
Now you can start up the Grid Hub:
```bash
./grid-hub start
```
Now you can add a Grid Node to the Grid Hub:
```bash
./grid-node start
```
(NOTE: If the Grid Node is not running on the same machine as the Grid Hub, update the address listed for WEBDRIVER_NODE_PARAMS in the [grid-node](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/selenium_grid/grid-node) script.)
You should be able to see the Grid Console up and running from here: [http://0.0.0.0:4444/grid/console](http://0.0.0.0:4444/grid/console) (NOTE: That's the address if you're running locally from localhost.)

You can remove a Grid Node from the Grid Hub with:
```bash
./grid-node stop
```
You can stop the Grid Hub at anytime with:
```bash
./grid-hub stop
```

When running with nosetests, configure a "``setup.cfg``" file with your grid hub info. (See the example [selenium_server_config_example.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/selenium_grid/selenium_server_config_example.cfg) file.)

When running with pytest, add the server and port info to a "``pytest.ini``" file. (Or add that data directly on the command line when you run your tests.)

#### More detailed info about connecting to the Selenium Grid Hub can be found here:
* [https://theintern.github.io/intern/#selenium-grid](https://theintern.github.io/intern/#selenium-grid)
* [https://github.com/SeleniumHQ/selenium/wiki/Grid2](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
* [https://github.com/SeleniumHQ/selenium/wiki](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
