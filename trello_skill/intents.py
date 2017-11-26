import alexandra

from .utils import trello_client, get_trello_user

alex = alexandra.Application()
BOARDS_LAST_USED_COUNT = 5


@alex.intent("ListBoards")
def list_boards_intent(slots, session):
    client = trello_client(session.user_id)
    boards = client.list_boards()
    sorted_boards = sorted(
        boards, key=lambda b: (
            b.date_last_activity is not None, b.date_last_activity
        ), reverse=True)[:BOARDS_LAST_USED_COUNT]
    board_names = ', '.join(l.name for l in sorted_boards)
    return alexandra.respond(
        f'You have {len(boards)} boards. Listing '
        f'{BOARDS_LAST_USED_COUNT} last used: {board_names}'
    )


@alex.intent("SetDefaultBoard")
def set_default_board_intent(slots, session):
    board = slots['Board']
    client = trello_client(session.user_id)
    trello_user = get_trello_user(session.user_id)
    boards = [l.name for l in client.list_boards()]
    if not board or board not in boards:
        return alexandra.respond(f"Invalid board {board}")
    # if trello_user.default_board:
    #     return alexandra.reprompt("Your current default is {trello_user.default_board}, are you sure you want to replace it?")
    trello_user.default_board = board
    trello_user.save()
    return alexandra.respond(f"I've set the board {board} as the default")


@alex.intent("ListsInBoard")
def lists_in_board_intent(slots, session):
    client = trello_client(session.user_id)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")


@alex.intent("ListCardsInBoard")
def list_cards_in_board_intent(slots, session):
    client = trello_client(session.user_id)
    boards = ', '.join(l.name for l in client.list_boards())
    return alexandra.respond(f"Listing your boards: {boards}")
