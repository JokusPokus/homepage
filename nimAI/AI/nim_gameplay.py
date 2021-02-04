from .train import train
from .nimAI import NimAI
from typing import Dict, List, Tuple


def train_and_initialize(session, n_train: int, board: List) -> None:
    """
    Trains the agent for n_train rounds and initializes the board.
    Everything is saved in the sessions dictionary.
    """
    ai_instance = train(int(n_train))
    session["nim_ai"] = ai_instance.q
    session["current_board"] = board
    session["winner"] = 0  # no winner yet


def reset_board(session, board: List) -> None:
    """
    Resets the board to its initial state with no winner.
    """
    session["current_board"] = board
    session["winner"] = 0  # no winner yet


def update_game_state(session, pile: int, amount: int) -> None:
    """Updates the current board according to the Human's move"""

    pile = int(pile)
    amount = int(amount)

    # Take chosen amount of objects from the pile
    session["current_board"][pile] -= amount


def ai_lost(current_board: List) -> bool:
    # True if all piles in current_board are empty
    return not any(current_board)


def declare_human_winner(session) -> None:
    session["winner"] = "Human"


def update_high_score(session) -> None:
    session["high_score"] = max(session["n_train"], session["high_score"])


def ai_move(session) -> Tuple[int, int]:
    """Picks the AI's response based on the current board,
    assuming it's the AI's turn.

    If the Human has already lost before the AI move or the AI loses after its move,
    session["winner"] is updated.
    """

    # Get AI move and update board
    ai_instance = NimAI(q=session.get("nim_ai"))

    pile, amount = ai_instance.choose_action(session["current_board"], epsilon=False)

    return pile, amount


