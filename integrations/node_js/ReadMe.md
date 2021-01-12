<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Creating a Test Runner with NodeJS + Express</h2>

You can create a customized web app for running SeleniumBase tests by using NodeJS and Express. (This tutorial assumes that you've already installed SeleniumBase by following the instructions from the [top-level ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md) file.)

<img src="https://seleniumbase.io/other/node_runner.png" title="Node Runner" />

#### 1. Install NodeJS

* Navigate to [https://nodejs.org/en/](https://nodejs.org/en/)
* Click to download and install NodeJS

#### 2. Install Express for NodeJS

```bash
npm install -g express
```

#### 3. Install the Example Test Runner for SeleniumBase from the ``integrations/node_js`` folder

```bash
npm install
```

(You should see a ``node_modules`` folder appear in your ``node_js`` folder.)

#### 4. Run the NodeJS server for your SeleniumBase Test Runner web app

```bash
node server.js
```

(You can always stop the server by using ``CTRL-C``.)

#### 5. Open the SeleniumBase Test Runner web app

* Navigate to [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

#### 6. Run an example test

Click on a button to run a SeleniumBase example test.

#### 7. Expand your web app

Now that you have a web app for running SeleniumBase tests, you can expand it to run any script that you want after pressing a button.
