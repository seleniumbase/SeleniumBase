## Running browser tests on [GitHub Actions](https://github.com/seleniumbase/SeleniumBase/actions) with [SeleniumBase](https://github.com/seleniumbase/SeleniumBase)

![](https://seleniumbase.io/cdn/img/gha/github_workflows_7.png "GitHub Actions")

----------

### Step 0. Create a fork of [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) on GitHub to help you get started.

* **(You'll be using your own repo eventually.)**

![](https://seleniumbase.io/cdn/img/gha/github_workflows_2.png "Create a fork of SeleniumBase")

----------

### Step 1. From the GitHub Actions tab, choose to set up a Python package Workflow.

![](https://seleniumbase.io/cdn/img/gha/github_workflows_1.png "GitHub Actions")

----------

### Step 2. Add your workflow ``.yml`` script.

* **(If using a SeleniumBase fork, the script from https://github.com/seleniumbase/SeleniumBase/blob/master/.github/workflows/python-package.yml already exists to help guide you.)**

![](https://seleniumbase.io/cdn/img/gha/github_workflows_9.png "GitHub Actions")

### Step 3. Commit your changes to GitHub.

![](https://seleniumbase.io/cdn/img/gha/github_workflows_4.png "GitHub Actions")

----------

### Step 4. Your tests will now run on every pull request and on every commit to the ``master`` branch.

* **(See https://github.com/seleniumbase/SeleniumBase/actions for the SeleniumBase example.)**

![](https://seleniumbase.io/cdn/img/gha/github_workflows_5.png "GitHub Actions")

* **(You can click inside each build for more details.)**

![](https://seleniumbase.io/cdn/img/gha/github_workflows_6.png "GitHub Actions")

* **(You can also see the specific steps being performed by each command.)**

![](https://seleniumbase.io/cdn/img/gha/github_workflows_7.png "GitHub Actions")

* **(You'll notice that web browsers such as Chrome and Firefox get installed for tests to use. SeleniumBase uses pytest for running tests while using Selenium to interact with web browsers.)**

----------

### Congratulations! You now know how to create and run browser tests with GitHub Actions!

### **Study [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) to learn more!**
