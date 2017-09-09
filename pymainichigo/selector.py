import os.path

import sgf

from pymainichigo.sgf.gogame import GoGame

class SgfSelecter(object):
    def __init__(self, config):
        pass

    def get_board(self, move=100):
        pass

class FileSelector(SgfSelecter):
    def __init__(self, config):
        super(FileSelector, self).__init__(config)
        self.fn = os.path.expanduser(config['sgf']['file'])
        with open(self.fn, 'r') as f:
            collection = sgf.parse(f.read())
            self.game = collection.children[0]
            self.N = int(self.game.root.properties.get("SZ", ["19"])[0])

    def get_game_length(self):
        moves = 0
        for node in self.game:
            moves += 1
        return moves

    def get_board(self, max_move_num=100):
        board = GoGame(size=self.N, handicap=0)

        move_num = 0
        for node in self.game:
            move_num += 1
            move = node.properties.get("B") or node.properties.get("W")
            if move:
                move_coords = sgf.SGF_POS.index(move[0][0]), sgf.SGF_POS.index(move[0][1])
                board.move_stone(*move_coords)
                if move_num >= max_move_num:
                    break

        return board.contents, move_coords
