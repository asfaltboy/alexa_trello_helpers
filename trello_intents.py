from os.path import join, dirname
from os import environ

from dotenv import load_dotenv
import alexandra

from trello_utils import get_client

alex = alexandra.Application()
wsgi = alex.create_wsgi_app()

# TODO: use a persistant store instead of in-memory
user_token_map = {}


@alex.intent("ListBoards")
def list_boards_intent(slots, session):
    client = trello_client(session)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")


@alex.intent("SetDefaultBoard")
def set_default_board_intent(slots, session):
    client = trello_client(session)
    board = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Set the board {board} as default")


@alex.intent("ListCardsInBoard")
def list_cards_in_board_intent(slots, session):
    client = trello_client(session)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")



@alex.intent("ListsInBoard")
def lists_in_board_intent(slots, session):
    client = trello_client(session)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")


def trello_client(session):
    global user_token_map
    if not user_token_map:
        api_key, user_token_map = setup_tokens()
    assert session.user_id in user_token_map, (
        'Session.user_id "%s" was not found in token map!' % session.user_id)
    return get_client(api_key=api_key, token=user_token_map[session.user_id])


def setup_tokens():
    """ Parse env vars for user Trello board tokens """
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, verbose=True)

    api_key = environ.get('TRELLO_API_KEY')
    assert api_key, 'Missing TRELLO_API_KEY value!'
    for key, value in environ.items():
        if key.startswith('TRELLO_API_TOKEN_'):
            user_token_map[key[17:]] = value
    return api_key, user_token_map


if __name__ == '__main__':
    setup_tokens()
    alex.run('127.0.0.1', 8080, debug=True)
