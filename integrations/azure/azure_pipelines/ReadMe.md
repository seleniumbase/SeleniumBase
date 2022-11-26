### Running browser-based test automation with [Azure Pipelines](https://dev.azure.com/seleniumbase/seleniumbase/_build?definitionId=1&_a=summary) by using [SeleniumBase](https://github.com/seleniumbase/SeleniumBase)

----------

### Step 0. Fork the [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) repo on GitHub to get started quickly.

* **(You'll be using your own repository eventually.)**


### Step 1. Get Azure Pipelines from the GitHub Marketplace

#### Navigate to [https://github.com/marketplace/azure-pipelines](https://github.com/marketplace/azure-pipelines)

* **Set up a new plan (it's free) and follow the steps...**

![](https://seleniumbase.github.io/cdn/img/azure/github_azure_pipelines_1.png "GitHub Azure Pipelines")

----------

![](https://seleniumbase.github.io/cdn/img/azure/github_azure_pipelines_2.png "GitHub Azure Pipelines")

----------

![](https://seleniumbase.github.io/cdn/img/azure/github_azure_pipelines_3.png "GitHub Azure Pipelines")

----------

### Step 2. Go to Microsoft Azure DevOps to set up your environment

* **Navigate to [https://azure.microsoft.com/en-us/services/devops/?nav=min](https://azure.microsoft.com/en-us/services/devops/?nav=min)**

* **Follow the steps...**

#### Select "Start free with GitHub >":

![](https://seleniumbase.github.io/cdn/img/azure/azure_devops_1a.png "Azure DevOps")

----------

#### Give your new project a name and set visibility to public (for your SeleniumBase fork):

![](https://seleniumbase.github.io/cdn/img/azure/azure_devops_2.png "Azure DevOps")

----------

#### Select that your code is hosted on GitHub:

![](https://seleniumbase.github.io/cdn/img/azure/azure_devops_3.png "Azure DevOps")

----------

#### Select your fork of SeleniumBase as your repository:

![](https://seleniumbase.github.io/cdn/img/azure/azure_devops_4.png "Azure DevOps")

----------

#### Copy the [azure-pipelines.yml](https://github.com/seleniumbase/SeleniumBase/blob/master/azure-pipelines.yml) file from SeleniumBase into the azure-pipelines.yml box to create your new pipeline:

![](https://seleniumbase.github.io/cdn/img/azure/azure_devops_5.png "Azure DevOps")

#### When you're done copying, click "Run".

----------

### Step 3. Congratulations! Your browser tests are now running!

* **Here's what a SeleniumBase sample run in Azure Pipelines may look like:**

[https://dev.azure.com/seleniumbase/seleniumbase/\_build/results?buildId=234](https://dev.azure.com/seleniumbase/seleniumbase/_build/results?buildId=234)

![](https://seleniumbase.github.io/cdn/img/azure/azure_devops_6.png "Azure DevOps")

----------

#### Every time you create a pull request now, Azure Pipelines will run your tests automatically.

**To learn more, study [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) and see how the [azure-pipelines.yml](https://github.com/seleniumbase/SeleniumBase/blob/master/azure-pipelines.yml) file works.**
