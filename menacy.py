#!/usr/bin/env python3

import random
from collections import Counter

class TicTacToeBoard:
    def __init__(self):
        self.cells = [' '] * 9

    def __str__(self):
        return (f"\n 0 | 1 | 2     {self.cells[0]} | {self.cells[1]} | {self.cells[2]}\n"
                "---+---+---   ---+---+---\n"
                " 3 | 4 | 5     {self.cells[3]} | {self.cells[4]} | {self.cells[5]}\n"
                "---+---+---   ---+---+---\n"
                " 6 | 7 | 8     {self.cells[6]} | {self.cells[7]} | {self.cells[8]}")

    def is_valid_move(self, position):
        try:
            position = int(position)
        except ValueError:
            return False
        return 0 <= position <= 8 and self.cells[position] == ' '

    def check_winner(self):
        winning_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for a, b, c in winning_conditions:
            if self.cells[a] == self.cells[b] == self.cells[c] != ' ':
                return True
        return False

    def is_draw(self):
        return all(cell != ' ' for cell in self.cells)

    def make_move(self, position, marker):
        self.cells[position] = marker

    def current_state(self):
        return ''.join(self.cells)


class LearningPlayer:
    def __init__(self):
        self.memory = {}
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def begin_game(self):
        self.history = []

    def choose_move(self, board):
        board_state = board.current_state()
        if board_state not in self.memory:
            available_moves = [i for i, cell in enumerate(board_state) if cell == ' ']
            self.memory[board_state] = available_moves * ((len(available_moves) + 2) // 2)

        available_moves = self.memory[board_state]
        if available_moves:
            move = random.choice(available_moves)
            self.history.append((board_state, move))
        else:
            move = -1
        return move

    def record_win(self):
        for (board_state, move) in self.history:
            self.memory[board_state].extend([move] * 3)
        self.wins += 1

    def record_draw(self):
        for (board_state, move) in self.history:
            self.memory[board_state].append(move)
        self.draws += 1

    def record_loss(self):
        for (board_state, move) in self.history:
            if move in self.memory[board_state]:
                self.memory[board_state].remove(move)
        self.losses += 1

    def display_stats(self):
        print(f'Learned {len(self.memory)} board states')
        print(f'W/D/L: {self.wins}/{self.draws}/{self.losses}')

    def display_probability(self, board):
        board_state = board.current_state()
        try:
            stats = Counter(self.memory[board_state]).most_common()
            print(f"Statistics for this board: {stats}")
        except KeyError:
            print("This board state has never been encountered.")


class UserPlayer:
    def __init__(self):
        pass

    def begin_game(self):
        print("Ready to play!")

    def choose_move(self, board):
        while True:
            move = input('Enter your move (0-8): ')
            if board.is_valid_move(move):
                return int(move)
            print("Invalid move. Try again.")

    def record_win(self):
        print("Congratulations, you won!")

    def record_draw(self):
        print("It's a draw.")

    def record_loss(self):
        print("You lost. Better luck next time.")

    def display_probability(self, board):
        pass


def execute_game(first_player, second_player, silent=False):
    first_player.begin_game()
    second_player.begin_game()
    game_board = TicTacToeBoard()

    if not silent:
        print("\nStarting a new game!")
        print(game_board)

    while True:
        if not silent:
            first_player.display_probability(game_board)
        move = first_player.choose_move(game_board)
        if move == -1:
            if not silent:
                print("Player resigns.")
            first_player.record_loss()
            second_player.record_win()
            break
        game_board.make_move(move, 'X')
        if not silent:
            print(game_board)
        if game_board.check_winner():
            first_player.record_win()
            second_player.record_loss()
            break
        if game_board.is_draw():
            first_player.record_draw()
            second_player.record_draw()
            break

        if not silent:
            second_player.display_probability(game_board)
        move = second_player.choose_move(game_board)
        if move == -1:
            if not silent:
                print("Player resigns.")
            second_player.record_loss()
            first_player.record_win()
            break
        game_board.make_move(move, 'O')
        if not silent:
            print(game_board)
        if game_board.check_winner():
            second_player.record_win()
            first_player.record_loss()
            break


if __name__ == '__main__':
    player1 = LearningPlayer()
    player2 = LearningPlayer()
    human_player = UserPlayer()

    for _ in range(1000):
        execute_game(player1, player2, silent=True)

    player1.display_stats()
    player2.display_stats()

    execute_game(player1, human_player)
    execute_game(human_player, player2)
