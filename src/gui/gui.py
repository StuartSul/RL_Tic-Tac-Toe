from src.engine.board import Board
from src.gui.boardslot import BoardSlot
from tkinter import Tk, Frame, Label, Button, PhotoImage

TK_SILENCE_DEPRECATION = 1

class GUI:
    """Board GUI created with tkinter"""
    status_text = {Board.BLACK_TURN: "Black's turn",
                   Board.BLACK_WIN: 'Black wins!',
                   Board.WHITE_TURN: "White's turn",
                   Board.WHITE_WIN: 'White wins!',
                   Board.DRAW: 'Draw!'}
    res_path = 'res/'
    img_name = {Board.EMPTY_SLOT: 'empty.gif',
                Board.BLACK_SLOT: 'black.gif', 
                Board.WHITE_SLOT: 'white.gif'}

    def __init__(self, board, windowtitle='Board'):
        self.board = board
        self.board.lock.acquire()
        
        self.window = Tk()
        self.window.title(windowtitle)

        self.img = {}
        for key, name in GUI.img_name.items():
            self.img[key] = PhotoImage(file=GUI.res_path + name)

        self.windowheight = self.board.size * self.img[Board.EMPTY_SLOT].height()
        self.windowwidth = self.board.size * self.img[Board.EMPTY_SLOT].width()

        self.window.geometry(str(self.windowwidth) + 'x' + str(self.windowheight+30) + '+100+100')
        self.window.resizable(True, True)

        self.labelframe = Frame(self.window, height=20, bd=0)
        self.labelframe.pack(side='top', fill='x')

        self.resetbutton = Button(self.labelframe, text='Reset', fg='black', command=self.board.reset)
        self.resetbutton.pack(side='left', fill='y')

        self.statuslabel = Label(self.labelframe, text=GUI.status_text[self.board.status], height=1, width=10)
        self.statuslabel.pack(side='right', fill='y')

        self.gameframe = Frame(self.window, bd=0)
        self.gameframe.pack(expand=True, fill='both')

        self.board_gui = []
        for i in range(self.board.size):
            self.board_gui.append([])
            for j in range(self.board.size):
                self.board_gui[i].append(BoardSlot(self.gameframe, i=i, j=j, bd=0, padx=0, pady=0, 
                                                  image=self.img[self.board.board[i][j]], 
                                                  height=self.img[self.board.board[i][j]].height(), 
                                                  width=self.img[self.board.board[i][j]].width()))
                self.board_gui[i][j].bind('<Button-1>', lambda x: self.board.place(x.widget.i, x.widget.j))
                self.board_gui[i][j].grid(row=i, column=j)

        self.board.load_gui(self)
        self.board.lock.release()
        self.window.mainloop()

    def update(self, i=None, j=None):
        self.statuslabel['text'] = GUI.status_text[self.board.status]
        if i == None or j == None:
            for i in range(self.board.size):
                for j in range(self.board.size):
                    self.board_gui[i][j]['image'] = self.img[self.board.board[i][j]]
        else:
            self.board_gui[i][j]['image'] = self.img[self.board.board[i][j]]