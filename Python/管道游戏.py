EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}


### add code here ###


class PipeGame:
    """
    A game of Pipes.
    """

    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
        """
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)],
                        [StartPipe(1), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)],
                        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)],
                        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)],
                        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3),  Tile('tile', True)],
                        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)]]

        playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        """
        self._board_layout = self.load_file('game_1.csv')[0:-1]
        self._playable = self.load_file('game_1.csv')[-1]
        self._starting_position = 0
        self._ending_position = 0
        self.end_pipe_positions()

    def load_file(self, filename):
        """ Read the game information from a csv file about board_layout and playable_pipes.

        Parameter:
            filename(str): The name of the csv file will be read.

        Return:
            tuple(dict,<str,int>, list<list<Tile>>): A tuple containing a dictionary which represents
        the information of playable_pipes and a list which represents the board_layout.
        """
        fd = open(filename,'r')
        content = []
        dic={}
        pipe_type=['straight', 'corner', 'cross', 'junction-t', 'diagonals', 'over-under']
        for line in fd:
            tem=line.strip('\n').split(',')
            content.append(tem)
        for i in range(6):
            dic[pipe_type[i]] = int(content[-1][i])
        content.pop(-1)
        for m in range(len(content)):
            for n in range(len(content[0])):
                if content[m][n] =='#':
                        content[m][n] = Tile('tile')
                elif content[m][n] in SPECIAL_TILES:
                    if content[m][n] == 'S':
                        content[m][n] = StartPipe()
                    if content[m][n] == 'E':
                        content[m][n] = EndPipe()
                    if content[m][n] == 'L':
                        content[m][n] = Tile('locked', False)
                elif content[m][n] in PIPES:
                    content[m][n] = Pipe(PIPES[content[m][n]])
                elif len(content[m][n]) == 3:
                    content[m][n] = Pipe(PIPES[content[m][n][0:-1]], int(content[m][n][-1]))
                elif len(content[m][n]) == 2:
                    if content[m][n][0] == 'S':
                        content[m][n] = StartPipe(int(content[m][n][1]))
                    elif content[m][n][0] == 'E':
                        content[m][n] = EndPipe(int(content[m][n][1]))
        content.append(dic)
        return content

    def get_board_layout(self):
        """Return: list<list<Tile,...>>, a list of lists where each element is a list representation of the row.
        """
        return self._board_layout

    def get_playable_pipes(self):
        """Return: dict<str:int>, a dictionary of all the playable pipes and number of times each pipe can be played
        """
        return self._playable

    def change_playable_amount(self, pipe_name, number):
        """Add the quantity of playable pipes of type specified by pipe_name to number.

        Parameter:
            pipe_name(str): The name of pipe type.
            number(int): The number of pipe that would be added.
        """
        self._playable[pipe_name] += number

    def get_pipe(self, position):
        """Parameter: position(tup<int, int>): Position of the pipe in the board_layout.

        Return: (Pipe|Tile)， While a Pipe at the position return Pipe, else return Tile.
        """

        return self._board_layout[position[0]][position[1]]
        

    def set_pipe(self, pipe, position):
        """Place the specified pipe at the given position.

        Parameter:
            pipe(Pipe): The kind of the pipe would be placed in the position.
            position(tup<int, int>): Position of the pipe in the board_layout.
        """
        if self._playable[pipe.get_name()] > 0:
            self._playable[pipe.get_name()] -= 1
            self._board_layout[position[0]][position[1]] = pipe

    def pipe_in_position(self, position):
        """Check whether there is a pipe a the position or not.
        Parameter:
            position(tup<int, int>): Position of the pipe in the board_layout.
        Return:
            (Pipe): Information of the pipe, while there is a pipe at the position.
            None: While there is not a pipe at the position.
        """
        if type(position) == tuple and position[0] <len(self._board_layout)and position[1]<len(self._board_layout[0]):
            if isinstance(self.get_pipe(position), Pipe) is True:
                return self.get_pipe(position)
            else:
                return None
        else:
            return None

    def remove_pipe(self, position):
        """Remove the pipe at the given position from the board.

        Parameter:
            position(tup<int, int>): Position of the pipe in the board_layout.
        """
        self._playable[self._board_layout[position[0]][position[1]].get_name()] += 1
        self._board_layout[position[0]][position[1]] = Tile('tile')

    def position_in_direction(self, direction, position):
        """Check whether there is a tile on the direction of the pipe.

        Parameter:
            direction(str): String represents N,E,W,S.
            position(tup<int, int>): Position of the pipe in the board_layout.
        Return:
            (tuple<str,tuple<int,int>>): The direction and position in the given
            direction from the given position.
        """
        if direction == 'N' and position[0] > 0:
            return ('S', (position[0] - 1, position[1]))
        elif direction == 'S' and position[0] < len(self._board_layout):
            return ('N', (position[0] + 1, position[1]))
        elif direction == 'W' and position[1] > 0:
            return ('E', (position[0], position[1] - 1))
        elif direction == 'E' and position[1] < len(self._board_layout[0]):
            return ('W', (position[0], position[1] + 1))

    def end_pipe_positions(self):
        """Find and save the start and end pipe positions from the game board.
        """
        count_i = -1
        count_j = -1
        length=len(self._board_layout[0])
        for i in self._board_layout:
            count_i += 1
            for j in i:
                count_j += 1
                if type(j) == StartPipe:
                    self._starting_position = (count_i, count_j % length)
                if type(j) == EndPipe:
                    self._ending_position = (count_i, count_j % length)

    def get_starting_position(self):
        """Return: (tuple<int, int>), the (row, col) position of the start pipe.
        """
        return self._starting_position

    def get_ending_position(self):
        """Return: (tuple<int, int>), the (row, col) position of the end pipe.
        """
        return self._ending_position

    def check_win(self):
        """
        (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):
                if self.position_in_direction(direction, position) is None:
                    new_direction = None
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                    
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                        new_position).get_connected()[0]:
                    return True
                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False


class Tile:
    """Empty tile to be placed in the game board
    """

    def __init__(self, name, selectable=True,):
        """Construct a tile object represents an available space in the game board.

        Parameters:
            name (str): The name of the tile.
            selectable (bool):  Whether the tile can be selected or not.(True means could select)
        """
        self._name = name
        self._selectable = selectable

    def get_name(self):
        """Return: the name(str) of the tile
        """
        return self._name

    def get_id(self):
        """ Return: the id(str) of the tile class.
        """
        return self.__class__.__name__.lower()

    def set_select(self, select):
        """ Sets the status of the select switch to True or False.

        Parameters:
            elect(bool): While the tile can be selected it is True, else False.
        """
        self._selectable = select

    def can_select(self):
        """ Test whether the tile can be selected or not.
            Return:  True if the tile is selectable, or False if the tile is not selectable.
        """
        return self._selectable

    def __str__(self):
        return "Tile('{0}', {1})".format(self._name, self._selectable)

    def __repr__(self):
        return "Tile('{0}', {1})".format(self._name, self._selectable)


class Pipe(Tile):
    """ Pipes are a special type of Tile, which can be connected to other pipes in the
        game board to form a path.
    """

    def __init__(self, name, orientation=0, selectable=True):
        """Construct a Pipe object which is a subclass of Tile. Pipes are a special
                type of Tile, which can be connected to other pipes in the game board to form a path.

        Parameter:
            name(str): The name of the pipe type constituted by 6 kinds of tile.
            orientation(int): An integer in the range [0,3] representing the orientation of the Pipe.
            electable(bool): Whether the tile can be selected or not.(True means could select)
        """
        super().__init__(name, selectable)
        self._selectable = selectable
        self._orientation = orientation

    def get_connected(self, side):
        """Check the Pipe connecting this side with which other sides.

        Parameter:
            side(str): A string representing  N, S, E, W.
        Return:
            （list<str>): All sides that are connected to the given side.
        """
        ori = ['N', 'E', 'S', 'W']
        temp = self.get_orientation()
        if self._name == 'straight':
            if side == ori[temp] or side == ori[(temp + 2) % 4]:
                return list(ori[(ori.index(side) + 2) % 4])
            else:
                return []
        elif self._name == 'corner':
            if side == ori[temp]:
                return list(ori[(temp + 1)%4])
            if side == ori[(temp + 1) % 4]:
                return list(ori[temp])
            else:
                return []
        elif self._name == 'cross':
            ori.remove(side)
            return ori
        elif self._name == 'junction-t':
            if side != ori[temp]:
                ori.pop(temp)
                ori.remove(side)
                return ori
            else:
                return []
        elif self._name == 'diagonals':
            if temp % 2 == 0:
                if ori.index(side) % 2 == 0:
                    return list(ori[(ori.index(side) + 1)])
                else:
                    return list(ori[(ori.index(side) - 1)])
            else:
                if ori.index(side) % 2 == 0:
                    return list(ori[(ori.index(side) - 1) % 4])
                else:
                    return list(ori[(ori.index(side) + 1) % 4])
        elif self._name == 'over-under':
            return list(ori[(ori.index(side) + 2) % 4])

    def rotate(self, direction):
        """ Rotates the pipe one turn.
        """
        self._orientation += direction
        while self._orientation > 3:
            self._orientation %= 4

    def get_orientation(self):
        """ Returns the orientation(int) of the pipe (orientation must be in the range [0, 3]).
        """
        return self._orientation

    def __str__(self):
        return "Pipe('{0}', {1})".format(self._name, self._orientation)

    def __repr__(self):
        return "Pipe('{0}', {1})".format(self._name, self._orientation)


class SpecialPipe(Pipe):
    """SpecialPipe is an abstract class used to represent the start and end pipes in the game
    """

    def __init__(self, name, orientation=0):
        """Construct a SpecialPipe object which is a subclass of Pipe. StartPipe and EndPipe make up
        SpecialPipe.

        Parameter:
            name(str): The name of the pipe type constituted by 6 kinds of tile.
            orientation(int): An integer in the range [0,3] representing the orientation of the Pipe.
        """

        self._orientation = orientation
        self._name = name

    def get_id(self):
        """Return id(str) of the SpecialPipe.
        """
        return 'special_pipe'

    def __str__(self):
        return '{0}({1})'.format(self.__class__.__name__, self._orientation)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self._orientation)


class StartPipe(SpecialPipe):
    """A StartPipe represents the start pipe in the game.
    """

    def __init__(self, orientation=0):
        """Construct a StartPipe object which is a subclass of SpecialPipe.

        Parameter:
            orientation(int): An integer in the range [0,3] representing the orientation of the Pipe.
        """
        super().__init__(orientation)
        self._name = 'start'
        self._orientation = orientation

    def get_connected(self, side=None):
        """Check the StartPipe connecting with which other side.

        Parameter: side(str)=None: The SpecialPipe only has one side connected to other Pipes.
        Return: list(str):（list<str>): The side connecting with the StartPipe.
        """
        ori = ['N', 'E', 'S', 'W']
        temp = self.get_orientation()
        return [ori[temp]]


class EndPipe(SpecialPipe):
    """A EndPipe represents the start pipe in the game.
    """

    def __init__(self, orientation=0):
        """Construct a EndPipe object which is a subclass of SpecialPipe.

        Parameter:
            orientation(int): An integer in the range [0,3] representing the orientation of the Pipe.
        """
        super().__init__(orientation)
        self._name = 'end'
        self._orientation = orientation

    def get_connected(self, side=None):
        """Check the EndPipe connecting with which other side.

        Parameter: side(str)=None: The SpecialPipe only has one side connected to other Pipes.
        Return: list(str):（list<str>): The side connecting with the StartPipe.
        """
        ori = ['S', 'W', 'N', 'E']
        temp = self.get_orientation()
        return [ori[temp]]


def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()

