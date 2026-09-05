"""Copy this file to YOUR_NETID.py and replace the strategy."""

import chess

from chess_tournament_api import ChessAgent, Observation


class MyChessAgent(ChessAgent):
    name = "My Agent"

    def choose_move(self, observation: Observation) -> str:
        board = chess.Board(observation.fen)

        # Replace this first-legal-move policy with your own strategy.
        return next(iter(board.legal_moves)).uci()

