import alexandra

from .utils import trello_client

alex = alexandra.Application()


@alex.intent("ListBoards")
def list_boards_intent(slots, session):
    client = trello_client(session)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")


@alex.intent("SetDefaultBoard")
def set_default_board_intent(slots, session):
    board = slots['Board']
    client = trello_client(session)
    boards = [l.name for l in client.list_boards()]
    if not board or board not in boards:
        return alexandra.respond(f"Invalid board {board}")
    # TODO: persist change to DB
    return alexandra.respond(f"Set the board {board} as default")


@alex.intent("ListsInBoard")
def lists_in_board_intent(slots, session):
    client = trello_client(session)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")


@alex.intent("ListCardsInBoard")
def list_cards_in_board_intent(slots, session):
    client = trello_client(session)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")
