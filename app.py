import logging
import os

from flask import Flask, request
from github import Auth

from service.github_service import GitHubService

app = Flask(__name__)
logger = logging.getLogger()

auth = Auth.Token(os.environ['GITHUB_TOKEN2'])
print(os.environ['GITHUB_TOKEN'])

github_service = GitHubService(auth)


@app.post('/events')
def github_events():
    request_data = request.get_json()

    code_changes = github_service.get_code_changes_in_pull_request(request_data['pull_request'])

    # TODO: Use langchain to review the changes

    return ''


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=True)
