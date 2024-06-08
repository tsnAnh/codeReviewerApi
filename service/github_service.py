from typing import List

from github import Auth, Github
import logging

from block_of_code_changes import BlockOfCodeChanges

logger = logging.getLogger(__name__)


class GitHubService:
    gh: Github

    def __init__(self, auth: Auth):
        self.gh = Github(auth=auth)

    def get_code_changes_in_pull_request(self, pull_request) -> List[BlockOfCodeChanges]:
        print(f'{pull_request}')
        repo = self.gh.get_repo(pull_request['head']['repo']['full_name'])
        pr = repo.get_pull(pull_request['number'])

        files = pr.get_files()

        list_of_block_of_code_changes = []

        for file in files:
            print(f'Processing file {file}')

            patch_content = file.patch

            patch_lines = patch_content.splitlines()

            added_lines = [line[2:] for line in patch_lines if line.startswith('+ ') and not line.startswith('+++')]
            print('Added lines:')
            for added_line in added_lines:
                print(added_line)

            list_of_block_of_code_changes.append(BlockOfCodeChanges('\n'.join(added_lines), file.filename, ''))
            print("\n" + "=" * 50 + "\n")
        print("\n" + "=" * 50 + "\n")

        print(list_of_block_of_code_changes)
        return list_of_block_of_code_changes
