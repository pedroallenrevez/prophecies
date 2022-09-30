class Cursor:
    def __init__(self):
        self.cursor_x = 0
        self.cursor_y = 0

    def move_x(self, x):
        self.cursor_y += x

    def move_y(self, y):
        self.cursor_x += y

    def move(self, x, y):
        self.move_x(x)
        self.move_y(y)

    def reset(self):
        self.cursor_x = 0
        self.cursor_y = 0

    def forward(self, scrn, steps):
        # TODO - WINDOW FORWARD
        _, cols = scrn.getmaxyx()

        step = self.cursor_y + steps
        if step > cols:
            diff = step - cols
            self.cursor_y = 0
            self.move_y(1)
            self.move_x(diff)
        else:
            self.move_x(steps)

    def next_line(self):
        self.move_y(1)
        self.cursor_y = 0
