'''
Provides a basic frontend

Kathleen incorporated all changes to users.py
Marcus incorporated all changes to user_status.py code.
'''
import sys
import logging
from datetime import datetime
import main

# Build logger
FILE_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(FILE_FORMAT)
LOG_FILE = f'log_{datetime.today():%d-%m-%Y}.log'
file_handler = logging .FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
# Add launch statement
logger.info('Session launched at %s.', datetime.today().strftime(':%H:%M:%S'))


def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_collection)


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)


def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        logging.info("An error occurred while trying to add new user")
    else:
        logging.info("User was successfully added")


def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if main.update_user(user_id, email, user_name, user_last_name, user_collection):
        logging.info("User was successfully updated")
    else:
        logging.info("An error occurred while trying to update user")


def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if not result:
        logging.info("ERROR: User does not exist")
    else:
        logging.info('User ID: %s', result.user_id)
        logging.info('Email: %s', result.user_email)
        logging.info('Name: %s', result.user_name)
        logging.info('Last name: %s', result.user_last_name)


def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        logging.info("An error occurred while trying to delete user")
    else:
        logging.info("User was successfully deleted")


def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        logging.info("An error occurred while trying to add new status")
    else:
        logging.info("New status was successfully added")


def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, status_collection):
        logging.info("An error occurred while trying to update status")
    else:
        logging.info("Status was successfully updated")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if not result:
        logging.info("ERROR: Status does not exist")
    else:
        logging.info("User ID: %s", result.user_id)
        logging.info("Status ID: %s", result.status_id)
        logging.info("Status text: %s", result.status_text)


def filter_status_by_string():
    '''
    Filters statuses by phrases
    '''
    search_word = input('Enter the string to search: ')
    result = main.filter_status_by_string(search_word, status_collection)
    try:
        while True:
            next_result = next(result)
            print(next_result.status_text)
            yn_delete = input('Delete the status? (Y/N): ')
            if yn_delete.lower().strip() == 'y':
                delete_status_given(next_result.status_id)
            else:
                yn_review = input('Review the next status? (Y/N): ')
                if yn_review.lower().strip() == 'n':
                    break
    except StopIteration:
        logging.info('No more statuses with the following phrase %s', search_word)


def search_all_status_updates_matching_a_string():
    '''
    Filters statuses by phrase
    '''
    search_word = input('Enter the string to search: ')
    result = main.filter_status_by_string(search_word, status_collection)
    try:
        for result_x in result:
            print(result_x.status_text)
    except TypeError:
        logging.info('No statuses with the following phrase %s', search_word)


def flagged_status_updates():
    '''
    Filter statuses for search word and turn results into tuples
    '''
    search_word = input('Enter the string to search: ')
    result = main.filter_status_by_string(search_word, status_collection)
    try:
        [print((x.status_id, x.user_id, x.status_text)) for x in result]
    except TypeError:
        logging.info('No statuses with the following phrase %s', search_word)


def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        logging.info("An error occurred while trying to delete status")
    else:
        logging.info("Status was successfully deleted")


def delete_status_given(status_id):
    '''
    Deletes status from the database
    '''
    if not main.delete_status(status_id, status_collection):
        logging.info("An error occurred while trying to delete status")
    else:
        logging.info("Status was successfully deleted")


def status_generator(query):
    '''
    Status generator to return current status from query.

    StopIteration not needed here.
    '''
    for status in query:
        yield status


def search_all_status_updates():
    '''
    Ask for user_id, report how many status' were found and
    ask user if they'd like to print each one
    '''
    user_id = input('Enter user ID to find status for: ')
    query = main.search_all_status_updates(user_id, status_collection)
    # If successful query, build and loop through generator
    if query:
        status_gen = status_generator(query)
        for status in status_gen:
            # Ask user for yes or no
            question = 'Would you like to see the next status? (Y/N): '
            ans = input(question)
            while not validate_yes_no(ans):
                ans = input(question)
            # Interpret answer
            if ans.lower() == 'y':
                print(status.status_text)
            else:
                logging.info('Exiting search_all_status_updates.')
                return
        logging.info('You have reached the last status.')


def validate_yes_no(ans: str) -> bool:
    '''
    Validates a yes or no response.
    '''
    if ans.lower() == 'y' or ans.lower() == 'n':
        return True
    print('Please enter a valid response.')
    input('Press any key to continue...')
    return False


def quit_program():
    '''
    Quits program
    '''
    logging.info('Quitting program.')
    sys.exit()


if __name__ == '__main__':
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': add_status,
        'H': update_status,
        'I': search_status,
        'J': delete_status,
        'K': search_all_status_updates,
        'L': filter_status_by_string,
        'M': search_all_status_updates_matching_a_string,
        'N': flagged_status_updates,
        'O': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Add status
                            H: Update status
                            I: Search status
                            J: Delete status
                            K: Search user's status
                            L: Search status by phrase
                            M: Search all status updates matching a string
                            N: Search status by phrase as tuple
                            O: Quit

                            Please enter your choice: """)
        user_selection = user_selection.upper().strip()
        if user_selection in menu_options:
            logging.info('User selected %s ' \
                         '-> executing %s.',
                         user_selection,
                         menu_options[user_selection].__name__)
            menu_options[user_selection]()
        else:
            logging.info('%s is an invalid option.', user_selection)
            logging.info("Invalid option")
