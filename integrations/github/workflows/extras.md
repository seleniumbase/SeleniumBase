<h3><img src="https://seleniumbase.github.io/img/logo3a.png" title="SeleniumBase" width="32" /> Integrations for GitHub Actions:</h3>

### Uploading Artifacts:
* Here's an example using [upload-artifact@v4](https://github.com/actions/upload-artifact) to push up a SeleniumBase-generated artifact.

```yml
    - uses: actions/upload-artifact@v4
      with:
        name: Click to download the presentation
        path: saved_presentations/my_presentation.html
```

### Slack Notifications - [rtCamp/action-slack-notify](https://github.com/rtCamp/action-slack-notify) can be used to send notifications to Slack.

**Usage:**
* Create a slack integration webhook if you don't have one already.
* Create a ``SLACK_WEBHOOK`` secret on your repository with the webhook token value.
* For this particular action, ``SLACK_CHANNEL`` is an optional environment variable that defaults to the webhook token channel if not specified.
* The following example shows how to put a link to your workflow as the ``SLACK_MESSAGE`` (Lets you see artifacts pushed up, such as from the SeleniumBase Presenter feature!):

```yml
    - name: Slack notification
      uses: rtCamp/action-slack-notify@master
      env:
        SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        SLACK_CHANNEL: general
        SLACK_ICON_EMOJI: rocket
        SLACK_USERNAME: SeleniumBase
        SLACK_MESSAGE: 'Actions workflow completed successful! :tada:  https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}'
```
