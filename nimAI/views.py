import time

from django.shortcuts import render
from django.http import JsonResponse

from .AI.nim_gameplay import (train_and_initialize,
                              update_game_state,
                              ai_lost,
                              ai_move,
                              declare_human_winner,
                              update_high_score,
                              reset_board)

INITIAL_BOARD = [1, 3, 5, 7]


def index(request):
    """
    Render landing page with the options to
    - expand and read the rules
    - select training options
    """
    request.session["high_score"] = request.session.get("high_score", 0)
    context = {"high_score": request.session["high_score"]}

    return render(request, "nimAI/index.html", context)


def reset(request):
    """
    Reset the board without training the AI agent again.
    """
    reset_board(request.session, board=INITIAL_BOARD.copy())
    context = {
        "new_board": request.session["current_board"],
        "winner": request.session["winner"],
        "high_score": request.session["high_score"]
    }
    return render(request, "nimAI/nim.html", context)


def show_training_options(request):
    """
    Render training page,
    allowing user to select the amount of AI training rounds
    """
    request.session["high_score"] = request.session.get("high_score", 0)
    context = {"high_score": request.session["high_score"]}

    return render(request, "nimAI/nim_train.html", context)


def train_and_show_board(request):
    """
    Train AI agent
    and render game-playing page with initialized board
    """
    # Training with n_train rounds is requested
    if request.method == "POST":
        n_train = int(request.POST["n_train"])

    # BE validation to avoid malicious post requests
    # (n_train cannot be set to > 300 by using FE functionality)
    if n_train > 300:
        exit()

    # The input slider is not linear.
    # For higher numbers, one slider unit increases n_train quicker.
    if n_train > 200:
        n_train = 1000 + (n_train - 200) * 90
    elif n_train > 100:
        n_train = 100 + (n_train - 100) * 9

    request.session["n_train"] = n_train
    request.session["high_score"] = request.session.get("high_score", 0)

    train_and_initialize(request.session, n_train, board=INITIAL_BOARD.copy())
    time.sleep(2.9)

    context = {
        "new_board": request.session["current_board"],
        "new_board_len_range": range(len(request.session["current_board"])),
        "row_ranges": [range(row) for row in request.session["current_board"]],
        "winner": request.session["winner"],
        "high_score": request.session["high_score"]
    }

    return render(request, "nimAI/nim.html", context)


def send_ai_move(request):
    """
    Update board state representation.
    Request an AI move and send it back to client as JSON.
    Requests are managed via AJAX.
    """

    def get_player_move(session, request):
        pile = amount = None
        for i in range(len(session["current_board"])):
            # Form input will only be non-empty for the selected row
            if request.POST.getlist(f"row_{i}"):  # e.g., ["Clicked", "Clicked", "Clicked]
                pile = i
                amount = len(request.POST.getlist(f"row_{i}"))
        return pile, amount

    # Player's move
    player_pile, player_amount = get_player_move(request.session, request)
    update_game_state(request.session, player_pile, player_amount)

    # AI's move
    ai_pile, ai_amount = ai_move(request.session)
    update_game_state(request.session, ai_pile, ai_amount)

    if ai_lost(request.session["current_board"]):
        declare_human_winner(request.session)
        update_high_score(request.session)

    data = {
        "winner": request.session["winner"],
        "pile": ai_pile,
        "amount": ai_amount,
        "high_score": request.session["high_score"]
    }

    return JsonResponse(data)
