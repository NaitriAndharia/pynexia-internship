import random


SNAKES = {
    99: 54,
    95: 72,
    87: 36,
    62: 19,
    54: 34,
    43: 18,
    17: 7,
}

LADDERS = {
    4: 25,
    13: 46,
    33: 49,
    42: 63,
    50: 69,
    62: 81,
    74: 92,
}


def display_board(positions):
    print("\n" + "=" * 61)
    print("                     SNAKE & LADDER BOARD (1-100)")
    print("=" * 61)

    for row in range(9, -1, -1):
        row_cells = []
        for col in range(10):
            if row % 2 == 1:
                cell = row * 10 + (10 - col)
            else:
                cell = row * 10 + (col + 1)

            markers = []
            for p_idx, p in enumerate(positions, start=1):
                if p["pos"] == cell:
                    markers.append(f"P{p_idx}")

            if markers:
                label = f"{cell:3d}({','.join(markers)})"
            elif cell in SNAKES:
                label = f"{cell:3d}S"
            elif cell in LADDERS:
                label = f"{cell:3d}L"
            else:
                label = f"{cell:5d}"

            row_cells.append(f"{label:<9}")
        print(" ".join(row_cells))

    print("-" * 61)
    print("Legend: S = Snake Head | L = Ladder Base | P1/P2 = Player Position")
    print("=" * 61)


def roll_dice():
    return random.randint(1, 6)


def move_player(player, dice):
    current = player["pos"]
    target = current + dice

    if target > 100:
        print(f"Rolled {dice}, but need {100 - current} or less to reach 100. Stayed at {current}.")
        return

    print(f"{player['name']} rolled {dice}: {current} -> {target}")
    pos = target

    if pos in LADDERS:
        climbed = LADDERS[pos]
        print(f"  [Ladder!] Climbed from {pos} up to {climbed}!")
        pos = climbed
    elif pos in SNAKES:
        bitten = SNAKES[pos]
        print(f"  [Snake!] Bitten at {pos}, slid down to {bitten}!")
        pos = bitten

    player["pos"] = pos


def setup_players():
    while True:
        try:
            count = int(input("Enter number of players (2-4) [default: 2]: ").strip() or "2")
            if 2 <= count <= 4:
                break
            print("[Error] Please enter between 2 and 4 players.")
        except ValueError:
            print("[Error] Enter a valid number.")

    players = []
    for i in range(1, count + 1):
        name = input(f"Enter Player {i} name [default: Player {i}]: ").strip() or f"Player {i}"
        players.append({"name": name, "pos": 0})
    return players


def play_game():
    print("\n=== WELCOME TO SNAKE & LADDER GAME ===")
    players = setup_players()
    turn = 0

    while True:
        display_board(players)
        current_player = players[turn % len(players)]
        print(f"\n{current_player['name']}'s turn (Current Position: {current_player['pos']})")
        choice = input("Press Enter to roll dice (or type 'q' to quit): ").strip().lower()

        if choice == "q":
            print("Game exited. Thanks for playing!")
            break

        dice = roll_dice()
        move_player(current_player, dice)

        if current_player["pos"] == 100:
            display_board(players)
            print("\n" + "*" * 45)
            print(f"  WINNER! {current_player['name']} reached 100!")
            print("*" * 45)
            break

        turn += 1


if __name__ == "__main__":
    play_game()