import random
import tkinter as tk
import time
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"
NUM = "012345678"
number = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
pokemon_sprites = ['charizard', 'cyndaquil', 'pikachu', 'psyduck', 'togepi', 'umbreon']
TASK_ONE = 'TASK_ONE'
TASK_TWO = 'TASK_TWO'
""" TASK mode strings are used in PokemonGame class.
"""
board_width = 300
"""board_width is the cell length in UI board, you should change it to change board width
It is because BoardModel class has been instantiated in PokemonGame class use this constant.
"""


class BoardModel:
    """ A game of Pokemon.(Model class)"""

    def __init__(self, grid_size, num_pokemon):
        """
            Construct a game of Pokemon.(Model class)

            Parameters:
                grid_size(int): The number of cells in each row(column).
                num_pokemon(int): The number of pokemons in this game.
        """
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._gamestr = UNEXPOSED * grid_size ** 2
        self._pokemon_locations = self.generate_pokemons(self._grid_size, self._num_pokemon)
        self._num_attempted_catches = 0

    def get_game(self):
        """Return:_gamestr(str): A string stored all elements in various cells.
        """
        return self._gamestr

    def get_pokemon_locations(self):
        """Return _pokemon_locations(tuple)A tuple containing  indexes where the pokemons are
        created for the game string.
        """
        return self._pokemon_locations

    def get_num_attempted_catches(self):
        """Return a int which represents how many pokeballs have been used.
        """
        return self._num_attempted_catches

    def set_num_attempted_catches(self, num):
        """Change the times of attempting to catch pokemon.
        """
        self._num_attempted_catches += num

    def get_num_pokemon(self):
        """Return:_num_pokemon(int): A int represents total number of pokemons
        """
        return self._num_pokemon

    def get_grid_size(self):
        """Return: _grid_size(int) : A int represents there are how many cells in a single row.
        """
        return self._grid_size

    def check_loss(self):
        """
        Returns True if the game has been lost, else False.
        """
        return POKEMON in self._gamestr

    def check_win(self):
        """
            Checking if the player has won the game.
        Returns:
            (bool): True if the player has won the game, false if not.
        """
        return UNEXPOSED not in self._gamestr and self._gamestr.count(FLAG) == len(self._pokemon_locations)

    def position_to_index(self, position):
        """
        Parameter:
            position(tuple): A tuple represents the cell location.
        Returns the index(int) corresponding to the
        supplied position.
        """
        index = position[1] + position[0] * self._grid_size
        return index

    def replace_character_at_index(self, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.
        """
        self._gamestr = self._gamestr[:index] + character + self._gamestr[index + 1:]

    def generate_pokemons(self, grid_size, number_of_pokemons):
        """Pokemons will be generated and given a random index within the game.

        Parameters:
            grid_size (int): The grid size of the game.
            number_of_pokemons (int): The number of pokemons that the game will have.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = grid_size ** 2
        pokemon_locations = ()

        for _ in range(number_of_pokemons):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count - 1)
            while index in pokemon_locations:
                index = random.randint(0, cell_count - 1)
            pokemon_locations += (index,)
        return pokemon_locations

    def flag_cell(self, index):
        """This function returns an updated game string after “toggling” the ﬂag at the
        specified index in the game string.

        Parameters:
            index(int):An integer representing the index of the cell in the game string.
        """
        list_game2 = list(self._gamestr)
        if list_game2[index] == FLAG:
            del list_game2[index]
            list_game2.insert(index, UNEXPOSED)
            self._gamestr = "".join(list_game2)
        else:
            del list_game2[index]
            list_game2.insert(index, FLAG)
            self._gamestr = "".join(list_game2)

    def index_in_direction(self, index, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        For example:
          | 1 | 2 | 3 |
        A | i | j | k |
        B | l | m | n |
        C | o | p | q |

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        # convert index to row, col coordinate
        col = index % self._grid_size
        row = index // self._grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        # Notice the use of if, not elif here
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < self._grid_size and 0 <= row < self._grid_size):
            return None
        return self.position_to_index((row, col))

    def neighbour_directions(self, index):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def number_at_cell(self, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if self._gamestr[index] != UNEXPOSED:
            return int(self._gamestr[index])

        numbers = 0
        for neighbour in self.neighbour_directions(index):
            if neighbour in self._pokemon_locations:
                numbers += 1

        return numbers

    def big_fun_search(self, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if self._gamestr[index] == FLAG:
            return queue

        numbers = self.number_at_cell(index)
        if numbers != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self._gamestr[neighbour] != FLAG:
                    numbers = self.number_at_cell(neighbour)
                    if numbers == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def reveal_cells(self, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
        numbers = self.number_at_cell(index)
        self.replace_character_at_index(index, str(numbers))
        clear = self.big_fun_search(index)
        gamestr = self._gamestr
        for i in clear:
            if gamestr[i] != FLAG:
                numbers = self.number_at_cell(i)
                self.replace_character_at_index(i, str(numbers))

        return self._gamestr

    def restart(self):
        """To refresh the game information while game restarting."""
        self._num_attempted_catches = 0
        self._gamestr = UNEXPOSED * self._grid_size ** 2

    def new_game(self):
        """ To generate a new game information, while user choose to start a new game"""
        self._num_attempted_catches = 0
        self._pokemon_locations = self.generate_pokemons(self._grid_size, self._num_pokemon)
        self._gamestr = UNEXPOSED * self._grid_size ** 2

    def load_game(self, game_list):
        """To load game information, while user choose to load a game
        Parameter: game_list(list): A list containing game information.
        """
        self._gamestr = game_list[0]
        self._pokemon_location = game_list[1]
        self._num_attempted_catches = game_list[2]
        self._num_pokemon = game_list[3]
        self._grid_size = game_list[4]


class BoardView(tk.Canvas):
    """UI class, view of the game board """

    def __init__(self, master, grid_size=10, board_width=600, *args, **kwargs):
        """Construct a board view from a the game information.

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            grid_size (list<list<Tile>>): 2D array of tiles in a board.
            board_width (callable): Callable to call when a pipe is being placed.
            *args: Additional positional arguments may be used later.
            **kwargs: Additional keywords arguments may be used later.
        """
        super().__init__(master, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self.config(width=board_width, height=board_width)
        self._game = args[0]
        self.Cell_length = self._board_width / self._grid_size
        self._move = []

    def draw_board(self, board):
        """Draw the board layout where the game board is displayed
        Parameter: board(str): game string from BoardModel class.
        """
        self.delete(tk.ALL)
        for i in range(self._grid_size):
            for j in range(self._grid_size):
                char = board[self.position_to_index((j, i), self._grid_size)]
                if char == UNEXPOSED:
                    self.create_rectangle(j * self.Cell_length, i * self.Cell_length, (j + 1) * self.Cell_length,
                                          (i + 1) * self.Cell_length, fill="green")
                elif char in NUM:
                    index = self.position_to_index((j, i), self._grid_size)
                    self.create_rectangle(j * self.Cell_length, i * self.Cell_length, (j + 1) * self.Cell_length,
                                          (i + 1) * self.Cell_length, fill="#ccff99")
                    self.create_text(self.position_to_pixel((j, i)), text=str(self._game.number_at_cell(index)),
                                     font=("Caladea", 8))
                elif char == POKEMON:
                    self.create_rectangle(j * self.Cell_length, i * self.Cell_length, (j + 1) * self.Cell_length,
                                          (i + 1) * self.Cell_length, fill="yellow")
                elif char == FLAG:
                    self.create_rectangle(j * self.Cell_length, i * self.Cell_length, (j + 1) * self.Cell_length,
                                          (i + 1) * self.Cell_length, fill="red")
        self.bind_clicks()

    def position_to_pixel(self, position):
        """To get the cell center pixel location with the cell position(tuple)
        Parameter: position (tuple<int, int>): The row, column position of a cell.
        """
        x, y = position
        return (x + 0.5) * self.Cell_length, (y + 0.5) * self.Cell_length

    def pixel_to_position(self, pixel):
        """To transform pixel location to position(tuple)
        Parameter: pixel(tuple<int, int> : The pixel location in <x, y> form of a cell.
        """
        x, y = pixel
        return x // self.Cell_length, y // self.Cell_length

    def position_to_index(self, position, grid_size):
        """Getting the cell index with the cell position and the grid size of this game.

        Parameter: position (tuple<int, int>): The row, column position of a cell.
                   grid_size (int): The grid size of the game.
        """
        x, y = position
        return y * grid_size + x

    def bind_clicks(self):
        """Bind clicks on a label to the left click and right click and motion handlers. """
        self.bind("<Button-1>", lambda a: self.left_click(a.x, a.y))
        self.bind("<Button-2>", lambda a: self.right_click(a.x, a.y))
        self.bind("<Button-3>", lambda a: self.right_click(a.x, a.y))
        self.bind("<Motion>", lambda a: self.move_event(a.x, a.y))

    def move_event(self, x, y):
        """Change the cell box outline color by a given amount.
        Parameter:
            x(int): x-coordinate in pixel format.
            y(int): y-coordinate in pixel format.
        """
        position = self.pixel_to_position((x, y))
        m, n = int(position[0]), int(position[1])
        self.delete(self._move)
        if self._game.check_win() == False and self._game.check_loss() == False:
            self._move = self.create_rectangle(m * self.Cell_length, n * self.Cell_length, (m + 1) * self.Cell_length,
                                               (n + 1) * self.Cell_length, fill="green", outline='yellow')

    def left_click(self, x, y):
        """Handle left clicking on a cell to change a cell string and display.
        Parameter:
            x(int): x-coordinate in pixel format.
            y(int): y-coordinate in pixel format.
        """
        position = self.pixel_to_position((x, y))
        index = int(self.position_to_index(position, self._grid_size))

        if self._game.get_game()[index] != FLAG:
            if index in self._game.get_pokemon_locations():
                self._game.replace_character_at_index(index, POKEMON)
                self.draw_board(self._game.get_game())
            else:
                self._game.reveal_cells(index)
                self.draw_board(self._game.get_game())

        if self._game.check_loss():
            poke_locations = self._game.get_pokemon_locations()
            for i in poke_locations:
                self._game.replace_character_at_index(i, POKEMON)
            self.draw_board(self._game.get_game())
            messagebox.showinfo(title="Game over", message="You lose!")

        if self._game.check_win():
            messagebox.showinfo(title="You Win!", message="You Win!")

    def right_click(self, x, y):
        """Handle right clicking on a cell to change a cell string and display.
        Parameter:
            x(int): x-coordinate in pixel format.
            y(int): y-coordinate in pixel format.
        """
        position = self.pixel_to_position((x, y))
        index = int(self.position_to_index(position, self._grid_size))
        if self._game.get_game()[index] not in NUM:
            self._game.flag_cell(index)
            self.draw_board(self._game.get_game())
        if self._game.check_win():
            messagebox.showinfo(title="You Win!", message="You Win!")


class PokemonGame:
    """controller class manages communication between the model class and the model class"""

    def __init__(self, master, grid_size=10, num_pokemon=15, task=TASK_TWO):
        """Create a new game app within a master widget.
            Parameters:
                master (Tk): Window in which this application is to be displayed.
                grid_size(int): The number of cells in each row(column).
                num_pokemon(int): The number of pokemons in this game.
                task(str): A string represents which mode this game is in.
        """
        self._master = master
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._task = task
        self._game = BoardModel(self._grid_size, self._num_pokemon)
        self._saved_game = []
        Label = tk.Label(self._master, text="Pokemon: Got 2 Find Them All!", bg="#ff5050", font=("Arial", 28),
                         fg='white')
        Label.pack(fill=tk.X)
        if self._task == TASK_ONE:
            self._board_view = BoardView(self._master, self._grid_size, board_width, self._game)
        elif self._task == TASK_TWO:
            self._statusbar = StatusBar(self._master, self._game, self)
            self._board_view = ImageBoardView(self._master, self._grid_size, board_width, self._game, self._statusbar,
                                              self)

            controls = tk.Frame(self._statusbar)
            self._new_game = tk.Button(controls, text='New game', width=9, command=self.new_game)
            self._new_game.pack(side=tk.TOP)
            self._restart_game = tk.Button(controls, text='Restart game', width=11, command=self.restart_game)
            self._restart_game.pack(side=tk.BOTTOM)
            controls.pack(side=tk.RIGHT, anchor=tk.SE, ipady=2)

            menu = tk.Menu(self._master)
            self._master.config(menu=menu)
            filemenu = tk.Menu(menu)
            menu.add_cascade(label="File", menu=filemenu)
            filemenu.add_command(label='Save game', command=self.save_game)
            filemenu.add_command(label='Load game', command=self.load_game)
            filemenu.add_command(label='Restart game', command=self.restart_game)
            filemenu.add_command(label='New game', command=self.new_game)
            filemenu.add_command(label='High scores', command=self.high_score)
            filemenu.add_command(label='Quit', command=self.quit)
        self.draw()

    def draw(self):
        """Draw the game to the master widget."""
        self._board_view.pack(side=tk.TOP)
        self._board_view.pack(side=tk.TOP)
        if self._task == TASK_TWO:
            self._statusbar.refresh_time()
            self._statusbar.pack(side=tk.BOTTOM)
            self._statusbar.time()
            self._statusbar.attempted_catches(0)
        self._board_view.draw_board(self._game.get_game())

    def restart_game(self):
        """Restart the game through statusbar class."""
        self._statusbar.restart()

    def new_game(self):
        """Create a new game through statusbar class."""
        self._statusbar.new_game()

    def save_game(self):
        """Save game information in specific txt file allocated by user."""
        game_info = [self._game.get_game() + '\n', str(self._game.get_pokemon_locations()) + '\n',
                     str(self._game.get_num_attempted_catches()) + '\n'
            , str(self._game.get_num_pokemon()) + '\n', str(self._game.get_grid_size()) + '\n',
                     str(self._board_view.get_time()) + '\n']
        filename = filedialog.asksaveasfilename()
        try:
            f = open(filename, "w")
            f.writelines(game_info)
            f.close()
        except ValueError:
            messagebox.showwarning('Warning', 'Please use appropriate filename!')
        except FileNotFoundError:
            messagebox.showwarning('Warning', 'A filename should be input.\n\n        Please try again！')
        if filename != '':
            self._saved_game.append(filename)
        fd = open('saved_game', 'a')
        fd.write('\n' + filename)
        fd.close()

    def load_game(self):
        """Load game information in the user choosing txt file."""
        try:
            f = open('saved_game', 'r')
            saved_game = ''
            for line in f:
                saved_game += line
        except FileNotFoundError:
            f = open('saved_game', 'r')
        messagebox.showinfo(title='Load game', message='Please load from these saved game: ' + saved_game)
        # Load game from text file
        filename = filedialog.asksaveasfilename()
        try:
            fd = open(filename, 'r')
            content = []
            for line in fd:
                content.append(line.strip('\n'))
        except ValueError:
            messagebox.showwarning('Warning', 'Please use appropriate filename!')
        except FileNotFoundError:
            messagebox.showwarning('Warning', 'There is not such a file.\n\n    Please try again！')

        try:
            list1 = []
            list1.append(content[0])
            list1.append(list(map(int, content[1].strip('(').strip(')').split(','))))
            list1.append(int(content[2]))
            list1.append(int(content[3]))
            list1.append(int(content[4]))
            self._game.load_game(list1)
            self._board_view.destroy()
            self._board_view = ImageBoardView(self._master, self._game._grid_size, board_width, self._game,
                                              self._statusbar, self)
            self._board_view.load_game(int(content[5]))
            self._statusbar.load_game(int(content[5]))
            self.draw()
        except UnboundLocalError:
            pass
        except IndexError:
            messagebox.showwarning('Warning', 'This saved game has been destroyed')

    def high_score(self):
        """Handling high score panel which could be reachedin file menu"""
        try:
            root1 = tk.Toplevel()
            root1.title('Top 3')
            root1.geometry("250x150+250+350")
            scores = self.check_highscore()
            tk.Label(root1, text="High Scores", bg="#ff5050", font=("Arial", 24),
                     fg='white').pack(fill=tk.X)
            if len(scores) >= 1:
                for score in scores[:3]:
                    tk.Label(root1, text=f'{score[0]}: {score[1] // 60}m {score[1] % 60}s').pack()
            tk.Button(root1, text='Done', command=root1.destroy).pack(side=tk.BOTTOM)

        except FileNotFoundError:
            messagebox.showinfo(title="No high score file", message="High score file is created!")
            f = open('high_score', 'w')
            f.close()

    def check_highscore(self):
        """Check high score record stroed in the record file."""
        file = open('high_score', 'r')
        scores = []
        try:
            for line in file:
                name, score = line.split(":")
                scores.append(([name, int(score)]))
            scores.sort(key=lambda e: e[1], reverse=False)
            return scores
        except ValueError:
            pass

    def quit(self):
        """Generate a message box check whether user want to quit or not."""
        messagebox.askquestion("Quit the Game", 'Are you sure you want to quit?')
        self._master.destroy()


class StatusBar(tk.Frame):
    """Statusbar display how many pokemon balls have been used and shows the used time and two button """

    def __init__(self, master, *args):
        """Construct a statusbar Frame.

        Parameters:
            master (Tk): Window in which this application is to be displayed.
            *args: additional positional arguments may use later.
        """
        super().__init__(master)
        self._master = master
        self._game = args[0]
        self._app = args[1]
        self._num_pokemon = self._game.get_num_pokemon()
        self._attempted_catches = self._game.get_num_attempted_catches()

        self._image = []
        image1 = get_image("images/full_pokeball")
        self._image.append(image1)
        image2 = get_image("images/clock")
        self._image.append(image2)
        # define the statusbar elements
        pokeball = tk.Label(self, image=image1)
        self.pokeball_text = tk.Label(self, text="")
        self._total_time = 0
        self._current_time = '0m 0s'
        self._timer_text = tk.Label(self, text='')
        self._timer_label = tk.Label(self, image=image2)
        # pack some of the statusbar
        pokeball.pack(side=tk.LEFT, padx=(25, 0))
        self.pokeball_text.pack(side=tk.LEFT)
        self._timer_label.pack(side=tk.LEFT, padx=(25, 0))
        self._timer_text.pack(side=tk.LEFT)

    def attempted_catches(self, num_balls):
        """Pack the text label in the frame about the used pokemon balls"""
        self._attempted_catches = num_balls
        self.pokeball_text.config(text= f'  {self._attempted_catches} attemped catches \n'
                                    f'{self._num_pokemon - self._attempted_catches} pokeballs left')
        self.pokeball_text.pack(side=tk.LEFT)

    def time(self):
        """Configure the time text in right format."""
        self._timer_text.config(text=f'Time elapsed\n {self._current_time}')

    def refresh_time(self):
        """Refresh the current time."""
        total_seconds = self._total_time
        mins = total_seconds // 60
        seconds = total_seconds % 60
        self._current_time = f'{mins}m {seconds}s'
        self.time()

    def restart(self):
        """Restart the game and refresh game information in BoardView class."""
        self._game.restart()
        self._attempted_catches = 0
        self._app._board_view.destroy()
        self._app._board_view = ImageBoardView(self._master, self._app._grid_size, board_width, self._game, self,
                                               self._app)
        self._app.draw()

    def new_game(self):
        """Create a new game and refresh game information in BoardView class."""
        self._game.new_game()
        self._attempted_catches = 0
        self._app._board_view.destroy()
        self._app._board_view = ImageBoardView(self._master, self._app._grid_size, board_width, self._game, self,
                                               self._app)
        self._app.draw()

    def load_game(self, load_time):
        """Refresh time information form load game."""
        self._total_time = load_time


class ImageBoardView(BoardView):
    """UI class, view of the game board in task_TWO mode."""
    def __init__(self, master, grid_size, board_width, *args, **kwargs):
        """Construct a board view from a the game information.

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            grid_size (list<list<Tile>>): 2D array of tiles in a board.
            board_width (callable): Callable to call when a pipe is being placed.
            *args: Additional positional arguments may be used later.
            **kwargs: Additional keywords arguments may be used later.
        """
        super().__init__(master, grid_size, board_width, *args, **kwargs)
        self._image = []
        self._statusbar = args[1]
        self._app = args[2]
        self._start_time = time.time()
        self._total_time = 0
        self._load_time = 0
        self.time_count()
        self.reply = None

    def resize_image(self, image):
        """Resize the image will display on the game board to adapt the board_width.
        Parameter:
            image (.gif or .png): picture will be used in game display.
        """
        try:
            img = Image.open(image + ".png")
            img = img.resize((int(self.Cell_length), int(self.Cell_length)), Image.ANTIALIAS)
            img.save(image + ".png")
        except tk.TclError:
            img = Image.open(image + "gif")
            img = img.resize((int(self.Cell_length), int(self.Cell_length)), Image.ANTIALIAS)
            img.save(image + "gif")

    def draw_board(self, board):
        """Draw the board layout where the game board is displayed
            Parameter: board(str): game string from BoardModel class.
        """
        self.delete(tk.ALL)
        self._image.clear()
        self.resize_image("images/unrevealed")
        self.resize_image("images/unrevealed_moved")
        self.resize_image("images/pokeball")
        for m in range(6):
            self.resize_image(f"images/pokemon_sprites/{pokemon_sprites[m]}")
        for n in range(9):
            self.resize_image(f"images/{number[n]}_adjacent")
        for i in range(self._grid_size):
            for j in range(self._grid_size):
                char = board[self.position_to_index((j, i), self._grid_size)]
                if char == UNEXPOSED:
                    image = get_image("images/unrevealed")
                    self.create_image(self.position_to_pixel((j, i)), image=image)
                    self._image.append(image)
                elif char in NUM:
                    image = get_image(f"images/{number[int(char)]}_adjacent")
                    self.create_image(self.position_to_pixel((j, i)), image=image)
                    self._image.append(image)
                elif char == POKEMON:
                    pokemon = pokemon_sprites[random.randint(0, 5)]
                    image = get_image(f"images/pokemon_sprites/{pokemon}")
                    self.create_image(self.position_to_pixel((j, i)), image=image)
                    self._image.append(image)
                elif char == FLAG:
                    image = get_image("images/pokeball")
                    self.create_image(self.position_to_pixel((j, i)), image=image)
                    self._image.append(image)
        self.bind_clicks()

    def time_count(self):
        """Count the total time has been spent in one game."""
        self._total_time = int(time.time() - self._start_time) + self._load_time
        self._statusbar._total_time = self._total_time
        self._statusbar.refresh_time()
        if self._game.check_win() == False and self._game.check_loss() == False:
            self.after(1000, self.time_count)

    def move_event(self, x, y):
        """Change the cell box outline color by a given amount.
            Parameter:
                x(int): x-coordinate in pixel format.
                y(int): y-coordinate in pixel format.
        """
        position = self.pixel_to_position((x, y))
        m, n = int(position[0]), int(position[1])
        index = int(self.position_to_index(position, self._grid_size))
        self.delete(self._move)
        if self._game.check_win() == False and self._game.check_loss() == False:
            try:
                if self._game.get_game()[index] != FLAG and self._game.get_game()[index] not in NUM:
                    image = get_image("images/unrevealed_moved")
                    self._image.append(image)
                    self._move = self.create_image(self.position_to_pixel((m, n)), image=image)
            except IndexError:
                pass

    def get_time(self):
        """Return _total_time(int): number of total seconds has been spent in one game."""
        return self._total_time

    def reveal_pokemon(self):
        """Display all pokemon on game board while lose."""
        poke_locations = self._game.get_pokemon_locations()
        for i in poke_locations:
            self._game.replace_character_at_index(i, POKEMON)
        self.draw_board(self._game.get_game())
        if self.reply == 'yes':
            self._statusbar.new_game()
        elif self.reply == 'no':
            self.quit()

    def reply_game(self):
        """While a game over choose to start a new game or quit the game."""
        if self.reply == 'yes':
            self._statusbar.new_game()
        elif self.reply == 'no':
            self.quit()

    def left_click(self, x, y):
        """Handle left clicking on a cell to change a cell string and display.
            Parameter:
                x(int): x-coordinate in pixel format.
                y(int): y-coordinate in pixel format.
        """
        position = self.pixel_to_position((x, y))
        index = int(self.position_to_index(position, self._grid_size))

        if self._game.get_game()[index] != FLAG:
            if index in self._game.get_pokemon_locations():
                self._game.replace_character_at_index(index, POKEMON)
                self.draw_board(self._game.get_game())
            else:
                self._game.reveal_cells(index)
                self.draw_board(self._game.get_game())

        if self._game.check_loss():
            self.reveal_pokemon()
            self.reply = messagebox.askquestion(title="Game over", message="You lose! Would you like to play again?")
            self.reply_game()
        if self._game.check_win():
            self.check_highscore()
            self.reply_game()

    def right_click(self, x, y):
        """Handle right clicking on a cell to change a cell string and display.
            Parameter:
                x(int): x-coordinate in pixel format.
                y(int): y-coordinate in pixel format.
        """
        position = self.pixel_to_position((x, y))
        index = int(self.position_to_index(position, self._grid_size))

        if self._game.get_game()[index] not in NUM:
            self._game.flag_cell(index)
            self.draw_board(self._game.get_game())
            if self._game.get_game()[index] != FLAG:
                self._game.set_num_attempted_catches(-1)
            else:
                self._game.set_num_attempted_catches(1)
        if self._game.check_win():
            self.check_highscore()
            self.reply_game()
        self._statusbar.attempted_catches(self._game.get_num_attempted_catches())
        self._statusbar.pack()

    def input_game1(self):
        """Save game information in high_score file."""
        new_record = self.entry.get() + ':' + str(self._total_time)
        f = open('high_score', 'a')
        f.write('\n' + new_record)
        f.close()
        self.root2.destroy()

    def check_highscore(self):
        """While win, if it is a new record, it should be recorded in high_score file."""
        scores = self._app.check_highscore()
        if self._total_time < scores[2][1]:
            self.root2 = tk.Toplevel()
            self.root2.title('New Record')
            self.root2.geometry("250x80+250+350")
            prompt = tk.Label(self.root2, text='Please input your name')
            prompt.pack()
            self.entry = tk.Entry(self.root2, width=15)
            self.entry.pack()
            input_button = tk.Button(self.root2, text='Input', command=self.input_game1)
            input_button.pack()
        else:
            self.reply = messagebox.askquestion(title="Win", message="You Win! Would you like to play again?")

    def load_game(self, load_time):
        """load game time"""
        self._total_time = load_time
        self._load_time = load_time


def get_image(image_name):
    """(tk.PhotoImage) Get a image file based on capability.

    If a .png doesn't work, default to the .gif image.
    (This function was copied from A2.GUI)
    """
    try:
        image = tk.PhotoImage(file=image_name + ".png")
    except tk.TclError:
        image = tk.PhotoImage(file=image_name + ".gif")
    return image


def main():
    """Main function, which allow the tkinter display continue through mainloop.
    """
    root = tk.Tk()
    root.title(" " + "Pokemon: Got 2 Find Them All!")
    PokemonGame(root)
    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()
