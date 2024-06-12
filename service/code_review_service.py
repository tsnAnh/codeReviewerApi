from langchain_core.language_models import BaseLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from block_of_code_changes import BlockOfCodeChanges

language_context_prompt = PromptTemplate.from_template("""
You are an AI assistant with the capability to analyze source code. After reviewing the provided code snippet, identify and succinctly describe the primary programming language used in a single sentence. Focus on syntax, libraries, and language-specific markers that are evident in the snippet.

Task:

Analyze the given code snippet for identifiable features such as syntax, usage of libraries, and any distinctive characteristics.
Formulate your analysis into a single sentence that clearly states the identified programming language along with a brief rationale based on the observed features.
Code Snippet:
{code}
File extension:
{extension}

Output Format:
"The code snippet provided is written in [Programming Language], as indicated by [distinctive features, such as specific syntax, library usage, etc.]."
""")

code_review_prompt_template = PromptTemplate.from_template("""
You are an AI coding assistant tasked with reviewing a set of code changes submitted as part of a Pull Request. The specific codebase will be provided for context, but you can start with the preliminary guidelines below. Your objectives are as follows:

Code Review: Thoroughly examine the submitted code changes. Look for any coding errors, including syntax mistakes, logical errors, potential inefficiencies, and areas of improvement.
Error Explanation: For each issue you identify, provide a detailed explanation of what the error is, why it's problematic, and how it could impact the application or software's functionality.
Suggest Corrections: If errors are found, offer specific suggestions on how to fix them. Provide code snippets to clearly illustrate your recommended changes or improvements.
Praise Good Practices: If sections of the code meet or exceed standard coding practices, be sure to acknowledge these. Praise the developer for their clean, efficient, or innovative coding approaches, reinforcing positive practices. Only praise on complex code block
Educational Feedback: Offer constructive feedback aimed at enhancing the developer’s understanding and skills. Discuss key concepts and best practices related to the specific challenges or features addressed in the PR.
Encouragement and Motivation: Maintain a supportive and encouraging tone throughout the review. Motivate the developer to continue refining their skills and to take pride in their accomplishments.
Additional Context:
{context}
The coder's experience level varies; adapt your feedback to be helpful for beginners, intermediates, and advanced developers alike.
This PR includes changes that are crucial for the application's core functionalities. Specific details will be provided alongside the codebase.
Utilize your expertise to guide the developer towards better coding practices and contribute positively to their ongoing development in the coding community.
You just need to focus on the logic and flow of the code, for those files consider as config or build files (like package.json, build.gradle, yarn.lock, ...) , just ignore them.

File name: {filename}

Code:
```
{code}
```

Code review content:
File Name: {filename}

Here are some examples of code review content of the file:
Line [number]: [Review content]
Line [number]: [Review content]

If a line has no issue, please do not include it
""")


def substring_after_last(s, delimiter):
    # Find the last occurrence of the delimiter
    pos = s.rfind(delimiter)
    # Slice the string from the character after the position of the delimiter
    return s[pos + 1:] if pos != -1 else ""


class CodeReviewService:
    llm: BaseLLM

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def generate_review_for_code_block(self, block_of_code_changes: BlockOfCodeChanges):
        chain = language_context_prompt | self.llm | StrOutputParser()
        review_chain = code_review_prompt_template | self.llm | StrOutputParser()
        extension = substring_after_last(block_of_code_changes.file_name, '.')
        context = chain.invoke({'extension': extension, 'code': block_of_code_changes.code_changes,
                                })
        review = review_chain.invoke({'context': context, 'code': block_of_code_changes.code_changes,
                                      'filename': block_of_code_changes.file_name})

        print(context)
        print(review)
