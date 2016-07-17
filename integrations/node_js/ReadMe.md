## Creating a SeleniumBase Test Launcher using NodeJS

Great news: It's really easy to create a customized web app for kicking off SeleniumBase jobs using NodeJS. This tutorial will walk you through all the steps that you need. (I'll assume that you've already installed SeleniumBase by following the instructions from the [top-level ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md) file.) 

#### 1. Install NodeJS

* Navigate to [https://nodejs.org/en/](https://nodejs.org/en/)
* Click to download and install NodeJS

#### 2. Install Express for NodeJS

```bash
npm install -g express
```

#### 3. Install the Example Test Launcher for SeleniumBase from the ``integrations/node_js`` folder

```bash
npm install
```

(You should see a ``node_modules`` folder appear in your ``node_js`` folder.)

#### 4. Run the NodeJS server for your SeleniumBase Test Launcher web app

```bash
node server.js
```

(You can always stop the server by using ``CTRL-C``.)

#### 5. Open the SeleniumBase Test Launcher web app

* Navigate to [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

#### 6. Run an example test

Click on one of the buttons to run a SeleniumBase example test

#### 7. Enjoy your web app

Congratulations! You now have a web app for kicking off SeleniumBase tests! NodeJS makes it easy!
