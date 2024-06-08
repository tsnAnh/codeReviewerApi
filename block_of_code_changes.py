from dataclasses import dataclass


@dataclass
class BlockOfCodeChanges:
    code_changes: str
    file_name: str
    review_text: str
