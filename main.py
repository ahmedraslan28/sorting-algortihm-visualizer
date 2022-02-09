import random
import pygame

pygame.init()


class Button:
    colours = [(201, 209, 200), (91, 112, 101), (0, 0, 255)]

    def __init__(self, color_idx, x, y, width, height, text='', font_size=15):
        self.color_idx = color_idx
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.colours[self.color_idx], (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def update(self, mouse, is_clicked=False, click_speed=False):
        if is_clicked or click_speed:
            self.color_idx = 2
        elif self.is_over(mouse):
            self.color_idx = 1
        else:
            self.color_idx = 0


btn = []


class DrawInformation:
    # colors
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = (98, 109, 113)
    # BACKGROUND_COLOR = WHITE
    BLOCKS_COLORS = [
        (205, 205, 192),
        (221, 188, 149),
        (179, 136, 103)
    ]

    # Padding
    TOP_PAD = 2
    RIGHT_PAD = 400
    LEFT_PAD = 1
    TOTAL_PAD = LEFT_PAD + RIGHT_PAD

    # Font types
    FONT = pygame.font.SysFont('comicsans', 15)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    lst = []
    min_val = max_val = block_width = block_height = start_x = 0

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) - 1
        self.max_val = max(lst)
        self.block_width = (self.width - self.TOTAL_PAD) / len(lst)
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val)
        self.start_x = self.LEFT_PAD


def generate_lst(n, min_val, max_val):
    lst = []
    for i in range(n):
        lst.append(random.randint(min_val, max_val))
    return lst


def draw(info):
    info.window.fill(info.BACKGROUND_COLOR)
    draw_lst(info)
    pygame.display.update()


def draw_lst(info, colour_position={}, clear=False):
    if clear:
        info.window.fill(info.BACKGROUND_COLOR)
    for i, num in enumerate(info.lst):
        x = info.start_x + i * info.block_width
        y = info.height - (num - info.min_val) * info.block_height
        colour = info.BLOCKS_COLORS[i % 3]
        if i in colour_position:
            colour = colour_position[i]
        pygame.draw.rect(info.window, colour, (x, y, info.block_width, info.height))
    for i in btn:
        i.draw(info.window, info.BLACK)
    if clear:
        pygame.display.update()


def bubble_sort(info):
    lst = info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_lst(info, {j: info.GREEN, j + 1: info.RED}, True)
                yield True
    return lst


def insertion_sort(draw_info):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current
            if not ascending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_lst(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


def merge_sort(info):
    for i in merge_sort_yield(info.lst):
        info.set_list(i)
        yield True
        draw_lst(info, {}, True)


def merge_sort_yield(arr):
    def merge_sort_rec(start, end):
        if end - start > 1:
            middle = (start + end) // 2
            yield from merge_sort_rec(start, middle)
            yield from merge_sort_rec(middle, end)
            left = arr[start:middle]
            right = arr[middle:end]
            a = 0
            b = 0
            c = start
            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    arr[c] = left[a]
                    a += 1
                else:
                    arr[c] = right[b]
                    b += 1
                c += 1

            while a < len(left):
                arr[c] = left[a]
                a += 1
                c += 1

            while b < len(right):
                arr[c] = right[b]
                b += 1
                c += 1
            yield arr

    yield from merge_sort_rec(0, len(arr))  # call inner function with start/end arguments


def selection_sort(info):
    lst = info.lst

    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_lst(info, {i: info.GREEN, min_idx: info.RED}, True)
        yield True


def main():
    run = True
    global btn
    clock = pygame.time.Clock()
    n = 100
    min_val = 0
    max_val = 200
    lst = generate_lst(n, min_val, max_val)
    info = DrawInformation(1200, 700, lst)
    start_x = 850
    start_y = 150
    increase_btn = Button(0, start_x, start_y, 35, 35, "+", 30)
    num_btn = Button(0, increase_btn.x + increase_btn.width, increase_btn.y, 250, 35, "#100")
    decrease_btn = Button(0, num_btn.x + num_btn.width, increase_btn.y, 35, 35, "-", 30)

    bubble_sort_btn = Button(0, start_x, increase_btn.y + 140, 100, 40, "Bubble sort")
    selection_sort_btn = Button(0, bubble_sort_btn.x + bubble_sort_btn.width + 10, bubble_sort_btn.y, 100, 40,
                                "selection sort")
    merge_sort_btn = Button(0, selection_sort_btn.x + selection_sort_btn.width + 10, bubble_sort_btn.y, 100,
                            40,
                            "merge sort")
    insertion_sort_btn = Button(0, selection_sort_btn.x, selection_sort_btn.y + 50, 100, 40, "insertion sort")

    low_btn = Button(0, 850, insertion_sort_btn.y + 140, 100, 40, "low speed")
    mid_btn = Button(0, low_btn.x + low_btn.width + 10, low_btn.y, low_btn.width, low_btn.height, "mid speed")
    high_btn = Button(0, mid_btn.x + mid_btn.width + 10, low_btn.y, mid_btn.width, mid_btn.height,
                      "high speed")

    start_btn = Button(0, start_x, low_btn.y + 140, 100, 40, "Start")
    reset_btn = Button(0, start_btn.x + start_btn.width + 10, start_btn.y, 100, 40, "Reset")
    stop_btn = Button(0, reset_btn.x + reset_btn.width + 10, start_btn.y, 100, 40, "Stop")

    global btn

    btn = [bubble_sort_btn, selection_sort_btn, merge_sort_btn, insertion_sort_btn, low_btn, mid_btn, high_btn,
           start_btn, reset_btn, stop_btn, increase_btn, num_btn, decrease_btn]
    start = False
    sorting_algorithm = None
    sorting_algorithm_generator = None
    speed = 60
    click_sort = click_speed = -1
    while run:
        clock.tick(speed)
        if start:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                start = False
        else:
            draw(info)
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.is_over(mouse_pos):
                    if sorting_algorithm is not None:
                        sorting_algorithm_generator = sorting_algorithm(info)
                        start = True
                elif stop_btn.is_over(mouse_pos):
                    start = False
                elif bubble_sort_btn.is_over(mouse_pos):
                    if start:
                        start = False
                    sorting_algorithm = bubble_sort
                    click_sort = 0
                elif selection_sort_btn.is_over(mouse_pos):
                    if start:
                        start = False
                    sorting_algorithm = selection_sort
                    click_sort = 1
                elif merge_sort_btn.is_over(mouse_pos):
                    if start:
                        start = False
                    sorting_algorithm = merge_sort
                    click_sort = 2
                elif insertion_sort_btn.is_over(mouse_pos):
                    if start:
                        start = False
                    sorting_algorithm = insertion_sort
                    click_sort = 3
                elif reset_btn.is_over(mouse_pos):
                    start = False
                    info.set_list(generate_lst(n, min_val, max_val))
                elif decrease_btn.is_over(mouse_pos):
                    start = False
                    if n > 50:
                        n -= 50
                        info.set_list(generate_lst(n, min_val, max_val))
                        num_btn.text = "#" + str(n)
                elif increase_btn.is_over(mouse_pos):
                    start = False
                    if n < 750:
                        n += 50
                        info.set_list(generate_lst(n, min_val, max_val))
                        num_btn.text = "#" + str(n)
                elif low_btn.is_over(mouse_pos):
                    start = False
                    click_speed = 4
                    speed = 10
                elif mid_btn.is_over(mouse_pos):
                    start = False
                    click_speed = 5
                    speed = 60
                elif high_btn.is_over(mouse_pos):
                    start = False
                    click_speed = 6
                    speed = 1000

            for i, val in enumerate(btn):
                if val != num_btn:
                    val.update(mouse_pos, (i == click_sort), (i == click_speed))
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
