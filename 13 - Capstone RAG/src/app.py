import os
import json

from src import setup_rag_chain, ask_question
from src import load_vector_db, create_and_load_vectorstore
from src import Jira

current_script_dir = os.path.dirname(os.path.abspath(__file__))

PERSISTENT_DIR = os.path.abspath(os.path.join(current_script_dir, '..', 'vector_db'))
PROMPT_PATH = os.path.abspath(os.path.join(current_script_dir, '..', 'src/prompts.json'))

with open(PROMPT_PATH, 'r') as f:
    prompts = json.load(f)

QA_CHAIN = None

prompt_instructions = prompts['prompts'][0]['instructions']
prompt_config = prompts['prompts'][0]['configuration']

jira_config = prompt_config['jira_integration']
INFO_NOT_FOUND_FLAG = prompt_config.get('fallback_flag', '<INFO_NOT_FOUND_IN_PDFS>')
JIRA_HANDLER: Jira = Jira()


def get_answer(question):
    answer, sources = ask_question(QA_CHAIN, question)

    if answer == "<INFO_NOT_FOUND_IN_PDFS>":
        print("\nInformation was not found in PDFs. Creating Jira ticket...")
        ticket_link = JIRA_HANDLER.create_jira_ticket(question)
        print(f"Jira Ticket Created: {ticket_link}\n")
        return ticket_link, None, False
    else:
        print(f"\nAnswer: {answer}\n")
        print(f"Sources: {sources}\n")
        return answer, sources, True


def init():
    try:
        if os.path.exists(PERSISTENT_DIR):
            vectorstore = load_vector_db(PERSISTENT_DIR)
        else:
            vectorstore = create_and_load_vectorstore()
    except Exception as e:
        os.rmdir(PERSISTENT_DIR)
        vectorstore = create_and_load_vectorstore()

    global QA_CHAIN, JIRA_HANDLER
    JIRA_HANDLER.set_up(jira_config)
    QA_CHAIN = setup_rag_chain(vectorstore, prompt_instructions)

    # print("Document-based Chatbot is ready!\n")
    # while True:
    #     user_input = input("Your question (or 'exit' to quit): ")
    #     if user_input.lower() in ("quit", "exit", "q"):
    #         break
    #
    # answer, sources = ask_question(qa_chain, user_input)
    #
    # if answer == "<INFO_NOT_FOUND_IN_PDFS>":
    #     print("\nInformation was not found in PDFs. Creating Jira ticket...")
    #     ticket_link = jira_handler.create_jira_ticket(user_input)
    #     print(f"Jira Ticket Created: {ticket_link}\n")
    # else:
    #     print(f"\nAnswer: {answer}\n")
    #     print(f"Sources: {sources}\n")
