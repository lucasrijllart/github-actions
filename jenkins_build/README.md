# Jenkins build action

To use this action, please follow these two steps:

1. Github action workflow file

    ``` yml
    name: Daily Build

    on:  # Controls when the action will run. 
      schedule:  # Runs workflow on a cron schedule
        - cron:  '00 8 * * *'  # every day at 08:00 UTC
      workflow_dispatch:  # Allows you to run this workflow manually from the Actions tab

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Run Jenkins build action
            uses: lucasrijllart/github-actions/jenkins_build@master
            with:
              job: 'https://build.jenkins.com/job/my-app/job/master/'
              creds: ${{ secrets.JENKINS_CREDS }}
    ```

2. Github secret value

    Add a repository secret `JENKINS_CREDS` which contains a value in the format:
    `<username>:<token>`. Where `<token>` contains the value of an Access Token generated
    in the Jenkins user panel.

