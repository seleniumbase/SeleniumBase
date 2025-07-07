<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Creating a Test Runner with NodeJS + Express</h2>

You can create a customized web app for running SeleniumBase tests by using NodeJS and Express. (This tutorial assumes that you've already installed [SeleniumBase](https://github.com/seleniumbase/SeleniumBase).

<img src="https://seleniumbase.github.io/other/node_runner.png" title="Node Runner" />

#### 0. Clone SeleniumBase from GitHub

* You'll need to work with the files located in the [integrations/node_js](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/node_js) folder.

#### 1. Install NodeJS (if not installed)

* Navigate to [https://nodejs.org/en/](https://nodejs.org/en/)
* Click to download and install NodeJS

#### 2. Upgrade NodeJS (if using an older version)

```zsh
npm install -g npm@latest
```

#### 3. Install the example Test Runner for SeleniumBase from [integrations/node_js](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/node_js). (If dependencies were already installed, you can use `npm ci` for a speed improvement over `npm i` / `npm install` because `npm ci` uses `npm-shrinkwrap.json`, which is generated via ``npm shrinkwrap``.)

```zsh
npm install
```

(You should see a `node_modules` folder appear in your `node_js` folder.)

#### 4. Run the NodeJS server for your SeleniumBase Test Runner web app

```zsh
node server.js
```

(You can stop the server by using <kbd>Ctrl+C</kbd>)

#### 5. Open the SeleniumBase Test Runner web app

* Navigate to [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

#### 6. Run an example test

Click on a button to run a SeleniumBase example test.

#### 7. Expand your web app

Now that you have a web app for running SeleniumBase tests, you can expand it to run any script that you want after pressing a button.
