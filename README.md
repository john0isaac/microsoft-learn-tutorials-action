# microsoft-learn-tutorials-action
GitHub Action to Automatically format Microsoft Learn Tutorials

This Action Contains two workflows:
- One triggers when you open a new pull request and sends you a welcome comment.
- The other formats the .md files to conform with the Microsoft Learn writing guidelines.

Automatic Formatting:
- Format the first two lines of files.
- Add an empty line to the end of files.
- Replace the word choose and click with select.
- Remove the country locale from links.
- Remove learn.microsoft.com from links.
- Add carriage return around images and notes.
