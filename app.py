import logging
import os

from flask import Flask, request
from github import Auth
from langchain_openai import OpenAI

from service.code_review_service import CodeReviewService
from service.github_service import GitHubService

app = Flask(__name__)
logger = logging.getLogger()

auth = Auth.Token(os.environ['GITHUB_TOKEN2'])
print(os.environ['GITHUB_TOKEN'])

github_service = GitHubService(auth)

llm = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'])
code_review_service = CodeReviewService(llm)


@app.post('/events')
def github_events():
    request_data = request.get_json()

    code_changes = github_service.get_code_changes_in_pull_request(request_data['pull_request'])

    for code_change in code_changes:
        code_review_service.generate_review_for_code_block(code_change)

    return ''


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=True)
