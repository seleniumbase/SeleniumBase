### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Running browser tests from [GitHub Actions/Workflows](https://github.com/seleniumbase/SeleniumBase/actions) with [SeleniumBase](https://github.com/seleniumbase/SeleniumBase)

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_7.png "GitHub Actions/Workflows")

----------

### Step 0. Create a fork of [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) on GitHub to help you get started.

* **(You'll be using your own repo eventually.)**

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_2.png "Create a fork of SeleniumBase")

----------

### Step 1. From the GitHub Actions tab, choose to set up a Python package Workflow.

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_1.png "GitHub Actions/Workflows")

----------

### Step 2. Add your workflow ``.yml`` script.

* **(If using a SeleniumBase fork, the script from https://github.com/seleniumbase/SeleniumBase/blob/master/.github/workflows/python-package.yml already exists to help guide you.)**

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_9.png "GitHub Actions/Workflows")

### Step 3. Commit your changes to GitHub.

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_4.png "GitHub Actions/Workflows")

----------

### Step 4. Your tests will now run on every pull request and on every commit to the ``master`` branch.

* **(See https://github.com/seleniumbase/SeleniumBase/actions for the SeleniumBase example.)**

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_5.png "GitHub Actions/Workflows")

* **(You can click inside each build for more details.)**

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_6.png "GitHub Actions/Workflows")

* **(You can also see the specific steps being performed by each command.)**

![](https://cdn2.hubspot.net/hubfs/100006/images/github_workflows_7.png "GitHub Actions/Workflows")

* **(You'll notice that web browsers such as Chrome and Firefox get installed for tests to use. SeleniumBase uses pytest for running tests while using Selenium to interact with web browsers.)**

----------

### Step 5. Congratulations! You now know how to create and run browser tests with GitHub Actions/Workflows!

### **Study [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) to learn more!**


### Slack notifications:
* the action [rtCamp/action-slack-notify](https://github.com/rtCamp/action-slack-notify) is just one of the many slack notification actions available
* create a slack integration webhook if you don't have one already
* create a `SLACK_WEBHOOK` secret on your repository with the webhook token value
* for this particular action, `SLACK_CHANNEL` is optional environment variable and will default to the webhook token channel if not specified
* this example shows how you can put a link to your github action workflow as the `SLACK_MESSAGE` (good for people to see artifacts you can push up such as the SeleniumBase Presenter)
```
    - name: Slack notification
      uses: rtCamp/action-slack-notify@master
      env:
        SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        SLACK_CHANNEL: general
        SLACK_ICON_EMOJI: rocket
        SLACK_USERNAME: SeleniumBase
        SLACK_MESSAGE: 'Actions workflow completed successful! :tada:  https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}'
```

### Upload a SeleniumBase presentation as an artifact
* Here is an example how to use [upload-artifact@v2](https://github.com/actions/upload-artifact) to push up a SeleniumBase generated presentation as an artifact. (You can use this in conjunction with the Slack notification to grab and or view the presentation directly from github)
```
    - uses: actions/upload-artifact@v2
      with:
        name: Click here to download SeleniumBase presentation!
        path: saved_presentations/my_presentation.html
```
