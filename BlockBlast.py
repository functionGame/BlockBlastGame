import pygame
import random


pygame.init()

blocks = [
    [[1, 3, 4, 5], [0, 3, 4, 6], [0, 1, 2, 4], [1, 3, 4, 7]],  # one on three
    [[0, 1, 3, 4]], # mini square
    [[0, 3, 4, 5], [0, 1, 3, 6], [0, 1, 2, 5], [1, 4, 6, 7]], # L - shape
    [[0, 3, 4], [0, 1, 3], [0, 1, 4], [1, 3, 4]], # mini corner
    [[1, 3, 4, 5, 7]], # cross
    [[0]], # one
    [[0, 1], [0, 3]], # two
    [[0, 1, 2], [0, 3, 6]] # three
]

weights = [2,3,4,4,2,1,1,3]

block_colors = [
    (77,238,234),
	(116,238,21),
	(255,231,0),
    (247,127,255),
    (252,119,121),
]

class Block:
    def __init__(self, block_x, block_y):
        self.x = block_x
        self.y = block_y
        self.size = grid_size
        self.type = random.choices(range(len(blocks)), weights)[0]
        self.rotation = random.randint(0, len(blocks[self.type]) - 1)
        self.color = random.choice(block_colors)

    def shape(self):
        return blocks[self.type][self.rotation]

def draw_block(block):
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                pygame.draw.rect(screen, block.color, [block.x + (x * block.size), block.y + (y * block.size), block.size, block.size])

def draw_grid(block_size):
    grid_width = screen.get_width()
    grid_height = screen.get_height() // 2

    cols = grid_width // block_size
    rows = grid_height // block_size


    x_gap = (grid_width - cols * block_size) // 2
    y_gap = screen.get_height() // 5

    grid_indices = []

    for y in range(rows):
        for x in range(cols):
            color = (0, 30, 75)
            pygame.draw.rect(screen, color,[(x * block_size) + x_gap, (y * block_size + y_gap), block_size, block_size], 1)
            grid_indices.append([(x * block_size) + x_gap, (y * block_size + y_gap), 0])

    return grid_indices, cols, rows, x_gap, y_gap

def check_block(curBlock, cur_x, cur_y):
    checkBlock = True
    dropBlock = False
    for y in range(3):
        for x in range(3):
            if y * 3 + x in curBlock.shape():
                if not (x_gap <= x * curBlock.size + cur_x <= (cols - 1) * grid_size + x_gap):
                    dropBlock = True
                    checkBlock = False
                elif not (y_gap <= y * curBlock.size + cur_y <= (rows - 1) * grid_size + y_gap):
                    dropBlock = True
                    checkBlock = False
                elif x * curBlock.size + curBlock.x > cols * grid_size + x_gap \
                        or x * curBlock.size + curBlock.x < x_gap \
                        or y * curBlock.size + curBlock.y > rows * grid_size + y_gap \
                        or y * curBlock.size + curBlock.y < y_gap:
                    checkBlock = False

                if not checkBlock:
                    break

                x_val = ((cur_x - x_gap + x * grid_size) // grid_size)
                y_val = ((cur_y - y_gap + y * grid_size) // grid_size)

                if (y_val > rows - 1) or (x_val > cols - 1):
                    checkBlock = False
                elif placed_blocks[y_val][x_val] != None:
                    checkBlock = False
    return dropBlock, checkBlock

def checkBlockWorks(new_block):
    cur_check = False
    for row in range(len(placed_blocks)):
        for col_block in range(len(placed_blocks[row])):
            if placed_blocks[row][col_block] == None:
                iter_check = True
                for by in range(3):
                    for bx in range(3):
                        if by * 3 + bx in new_block.shape():
                            if (row + by < len(placed_blocks)) and (col_block + bx < len(placed_blocks[row])):
                                if placed_blocks[row + by][col_block + bx] != None:
                                    iter_check = False
                            else: iter_check = False
                if iter_check:
                    cur_check = True
                    break
    return cur_check

def check_message(cleared_message, print_message):
    if len(cleared_message) > 0:
        messageFont = pygame.font.Font('freesansbold.ttf', y_gap // 5)

        for item in cleared_message:
            message = messageFont.render(item, True, (255, 255, 255))
            messageRect = message.get_rect()
            messageRect.center = (screen.get_width() // 2, (rows // 2) * grid_size + y_gap)

            if "GAME OVER" not in cleared_message:
                if item == "Row Cleared!":
                    messageRect.y -= 15
                if item == "Column Cleared!":
                    messageRect.y += 15

            print_message.append([[message, messageRect], counter])
    return [], print_message

screen = pygame.display.set_mode((78 * 4, 160 * 4), 0, 32)
pygame.display.set_caption("Block Blast!")

grid_size  = 30

move = False
added = False
game_over = False
game_finished = False

screen_blocks = []
clicked_blocks = []
screen_check = [False, False, False]

grid_indices, cols, rows, x_gap, y_gap = draw_grid(grid_size)

placed_blocks = []
empty_grid = []
for y in range(rows):
    placed_blocks.append([])
    empty_grid.append([])
    for x in range(cols):
        placed_blocks[-1].append(None)
        empty_grid[-1].append(0)

titleFont = pygame.font.Font('freesansbold.ttf', y_gap // 3)
title = titleFont.render('Block Blast!', True, (255, 255, 255))
titleRect = title.get_rect()
titleRect.center = (screen.get_width() // 2, y_gap // 2)

scores = []

file = open("highscore", 'a')
file.close()

file = open("highscore", 'r')
line = file.readline()
while line:
    line = line.strip()
    scores.append(int(line))
    line = file.readline()
file.close()

if len(scores) > 0:
    highscore = max(scores)
else:
    highscore = 0

highscoreFont = pygame.font.Font('freesansbold.ttf', y_gap // 7)
highscoreText = highscoreFont.render("Highscore: " + str(highscore), True, (255, 255, 255))
highscoreRect = highscoreText.get_rect()
highscoreRect.center = (screen.get_width() // 3, y_gap // 7)

score = 0
scoreFont = pygame.font.Font('freesansbold.ttf', y_gap // 6)
scoreText = scoreFont.render("Score: " + str(score), True, (255, 255, 255))
scoreRect = scoreText.get_rect()
scoreRect.center = (screen.get_width() // 2, y_gap // 2 + y_gap // 4)

cleared_message = []
print_message = []

counter = 0
while not game_over:
    counter += 1

    screen.fill((0, 0, 0))
    draw_grid(grid_size)
    screen.blit(title, titleRect)
    screen.blit(scoreFont.render("Score: " + str(score), True, (255, 255, 255)), scoreRect)
    screen.blit(highscoreFont.render("Highscore: " + str(highscore), True, (255, 255, 255)), highscoreRect)

    for block in screen_blocks:
        if block != None:
            draw_block(block)

    cleared_message, print_message = check_message(cleared_message, print_message)

    allPlaced = True
    for block in screen_blocks:
        if block:
            allPlaced = False

    if allPlaced and len(clicked_blocks) == 0:
        screen_blocks = []
        for space in range(3):
            block_size = grid_size * 3
            margin = (screen.get_width() - block_size * 3) // 4
            block = Block(margin * (space + 1) + block_size * space, ((screen.get_height() - ((rows * grid_size) + y_gap)) // 2)+ ((rows * grid_size) + y_gap) - grid_size * 3 // 2)

            screen_blocks.append(block)

    if (allPlaced and len(clicked_blocks) == 0) or (allPlaced == False and added):
        for block in range(len(screen_blocks)):
            if screen_blocks[block] != None:
                checked = checkBlockWorks(screen_blocks[block])
                screen_check[block] = checked
            else:
                screen_check[block] = None
        checkedFull = False
        for item in screen_check:
            if item == True:
                checkedFull = True
        if checkedFull:
            for block in screen_blocks:
                if block != None:
                    draw_block(block)
        else:
            cleared_message.append("GAME OVER")
            game_finished = True
            end_counter = counter

    if added:
        clear_blocks = []
        columns = []
        for y in range(rows):
            clear_blocks.append([])
            columns.append([])
            for x in range(cols):
                clear_blocks[-1].append(0)
                columns[y].append(0)

        for row in range(len(placed_blocks)):
            check_row = True
            for block in placed_blocks[row]:
                if block == None:
                    check_row = False

            if check_row:
                clear_blocks[row] = []
                for block in placed_blocks[row]:
                    clear_blocks[row].append(1)
                cleared_message.append("Row Cleared!")

        for col in range(len(columns)):
            for row in range(len(placed_blocks)):
                if placed_blocks[row][col] == None:
                    columns[col][row] = 0
                else:
                    columns[col][row] = 1

            check_col = True
            for block in columns[col]:
                if block == 0:
                    check_col = False

            if check_col:
                for row in range(len(clear_blocks)):
                    clear_blocks[row][col] = 1
                cleared_message.append("Column Cleared!")

        clearedCount = 0
        for y in range(rows):
            for x in range(cols):
                if clear_blocks[y][x] == 1:
                    placed_blocks[y][x] = None
                    clearedCount += 1

        score += clearedCount * 2
        added = False

    for row in range(len(placed_blocks)):
        for col in range(len(placed_blocks[row])):
            if placed_blocks[row][col] != None:
                block_info = placed_blocks[row][col]
                pygame.draw.rect(screen, block_info[1],[(col * grid_size) + x_gap, (row * grid_size + y_gap), grid_size, grid_size])

    for message in print_message:
        if (counter - message[1]) < 1000:
            screen.blit(message[0][0], message[0][1])
        else:
            print_message.remove(message)

    if not(game_finished):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if move:
                    curBlock = clicked_blocks[0]

                    dropBlock = False
                    diff_x, diff_y = 100000000,100000000
                    cur_x, cur_y = 0, 0
                    for point in grid_indices:
                        if abs(curBlock.x - point[0]) < diff_x:
                            diff_x = abs(curBlock.x - point[0])
                            cur_x  = point[0]
                        if abs(curBlock.y - point[1]) < diff_y:
                            diff_y = abs(curBlock.y - point[1])
                            cur_y = point[1]

                    dropBlock, checkBlock = check_block(curBlock, cur_x, cur_y)

                    if dropBlock:
                        place = screen_blocks.index(None)

                        block_size = curBlock.size * 3
                        margin = (screen.get_width() - block_size * 3) // 4

                        curBlock.x = margin * (place + 1) + (curBlock.size * 3) * place
                        curBlock.y = ((screen.get_height() - ((rows * grid_size) + y_gap)) // 2) + ((rows * grid_size) + y_gap) - grid_size * 3 // 2
                        screen_blocks[place] = curBlock
                        clicked_blocks.remove(curBlock)
                        move = False
                        break

                    if checkBlock:
                        curBlock.x, curBlock.y = cur_x, cur_y

                        blockCount = 0

                        for y in range(3):
                            for x in range(3):
                                if y * 3 + x in curBlock.shape():
                                    x_val = ((cur_x - x_gap + x * grid_size) // grid_size)
                                    y_val = ((cur_y - y_gap + y * grid_size) // grid_size)

                                    blockCount += 1

                                    placed_blocks[y_val][x_val] = (True, curBlock.color)

                        score += blockCount

                        added = True
                        clicked_blocks.remove(curBlock)
                        move = False
                    else:
                        x, y = event.pos
                        curBlock.x, curBlock.y = x, y
                else:
                    x, y = event.pos
                    for block in screen_blocks:
                        if block != None and (block.x <= x <= block.x + block.size * 3 and block.y <= y <= block.y + block.size * 3):
                            clicked_blocks.append(block)
                            screen_blocks[screen_blocks.index(block)] = None
                            move = True

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos

    if move:
        for block in clicked_blocks:
            block.x = x - block.size
            block.y = y - (block.size * 3) // 2

            draw_block(block)

    pygame.display.update()

    if game_finished:
        if counter - end_counter > 4000:
            game_over = True

file = open("highscore", 'a')
file.write(str(score) + "\n")
file.close()

pygame.quit()
