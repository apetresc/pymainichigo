import sgf

from gogame import GoGame

class SgfSelecter(object):
    def __init__(self, config):
        pass

    def get_board(self, move=100):
        pass

class FileSelector(SgfSelecter):
    def __init__(self, config):
        super(FileSelector, self).__init__(config)
        self.fn = config['sgf']['file']

    def get_board(self, move_=100):
        with open(self.fn, 'r') as f:
            collection = sgf.parse(f.read())
            game = collection.children[0]
            N = int(game.root.properties.get("SZ", ["19"])[0])

        board = GoGame(size=N, handicap=0)

        move_num = 0
        for node in game:
            move_num += 1
            move = node.properties.get("B") or node.properties.get("W")
            if move:
                board.move_stone(sgf.SGF_POS.index(move[0][0]), sgf.SGF_POS.index(move[0][1]))
                if move_num >= move_:
                    break

        return board.contents
