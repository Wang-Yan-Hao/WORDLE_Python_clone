import random

import pygame
import json
from Button import Button

# 啟動套件
pygame.init()
# 設定視窗名稱
pygame.display.set_caption("Wordle")
# 設定遊戲視窗
screen = pygame.display.set_mode((1000, 760))

# 設定一些變數的大小
SQ_SIZE = 63  # 正方形的大小
WIDTH = 900
HEIGHT = 800
MARGIN = 5  # 格子跟格子中間的空格
T_MARGIN = 100  # 上面的margin
B_MARGIN = 100  # 下面的margin
LR_MARGIN = 330  # 左右的margin

# 設定字體 他的字形以及大小
my_font = pygame.font.Font("assets/MorningRainbow.ttf", 38)
FONT = pygame.font.SysFont("assets/NotablyAbsentRegular-8M2zJ.ttf", 50)
BOTTOM_FONT = pygame.font.SysFont("assets/NotablyAbsentRegular-8M2zJ.ttf", 22)
SMLL_FONT = pygame.font.SysFont("assets/NotablyAbsentRegular-8M2zJ.ttf", 25)
#  相關的顏色
GREY = (121, 125, 127)
GREEN = (106, 172, 100)
YELLOW = (202, 181, 87)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UNGUESSED = ALPHABET
GAME_OVER = False

INPUT = ""  # 使用這正在輸入的字串
GUESSES = []  # 使用者已經猜測的字串。
Word_color = {}


def load_dict(file_name):
    json_file = open(file_name)  # 打開json檔案
    words = json.load(json_file)  # 用json.loads把json檔案轉成字典形式
    json_file.close()

    return_words = []  # 要回傳的字串陣列
    for key in words:  # 對於字典中每個key，長度為五的英文字，就把他丟要我們要回傳的字串陣列
        if len(key) == 5:
            return_words.append(key.upper())
    return return_words


DICT_GUESSING = load_dict("assets/words_dictionary.json")  # 一個字串 是字典
ANSWER = random.choice(DICT_GUESSING)  # 從字典裡隨意挑一個字當答案


def determine_unguessed_letters(guesses):
    guessed_letters = "".join(guesses)
    unguessed_letters = ""
    for l in ALPHABET:
        if l not in guessed_letters:
            unguessed_letters = unguessed_letters + l
    return unguessed_letters


def determine_color(guess, j):
    letter = guess[j]
    if letter == ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        n_target = ANSWER.count(letter)
        n_correct = 0
        n_occurrence = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_occurrence += 1
                elif letter == ANSWER[i]:
                    n_correct += 1
        if n_target - n_correct - n_occurrence >= 0:
            return YELLOW
    return GREY


def draw_keyboard():
    first_column_x = 273
    second_column_x = 300
    third_column_x = 293
    first_column = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
    second_column = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
    third_column = ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACK']
    keyboard = []

    for index in range(len(first_column)):
        if first_column[index] in UNGUESSED:
            current_color = (211, 214, 218)
            font_color = (0, 0, 0)
        elif Word_color.get(first_column[index]) is None:
            current_color = GREY
            font_color = (255, 255, 255)
        else:
            current_color = Word_color.get(first_column[index])
            font_color = (255, 255, 255)

        local = Button((first_column_x + index * 50, 580), 42, 58, first_column[index], BOTTOM_FONT,
                       current_color, font_color)
        keyboard.append(local)
        local.update(screen)
    for index in range(len(second_column)):
        if second_column[index] in UNGUESSED:
            current_color = (211, 214, 218)
            font_color = (0, 0, 0)
        elif Word_color.get(second_column[index]) is None:
            current_color = GREY
            font_color = (255, 255, 255)
        else:
            current_color = Word_color.get(second_column[index])
            font_color = (255, 255, 255)

        local = Button((second_column_x + index * 50, 645), 42, 58, second_column[index], BOTTOM_FONT,
                       current_color, font_color)
        keyboard.append(local)
        local.update(screen)
    for index in range(len(third_column)):
        if third_column[index] in UNGUESSED:
            current_color = (211, 214, 218)
            font_color = (0, 0, 0)
        elif Word_color.get(third_column[index]) is None:
            current_color = GREY
            font_color = (255, 255, 255)
        else:
            current_color = Word_color.get(third_column[index])
            font_color = (255, 255, 255)

        if index == 8:
            third_column_x += 20
        if index == 0 or index == 8:
            local = Button((third_column_x + index * 50, 710), 80, 58, third_column[index], BOTTOM_FONT,
                           (211, 214, 218), (0, 0, 0))
            keyboard.append(local)
            local.update(screen)
            third_column_x += 20
            continue

        local = Button((third_column_x + index * 50, 710), 42, 58, third_column[index], BOTTOM_FONT,
                       current_color, font_color)
        keyboard.append(local)
        local.update(screen)

    return keyboard


if __name__ == '__main__':

    print(ANSWER)
    animating = True
    while animating:

        UNGUESSED = determine_unguessed_letters(GUESSES)
        # 把畫布全部填到screen裡面 白色
        screen.fill("white")

        letters = my_font.render("Wordle", True, (0, 0, 0))  # 我們要畫的物件 這邊是WORDLE標誌
        letters_location = letters.get_rect(center=(500, 30))  # 回傳一個位置
        screen.blit(letters, letters_location)  # screen.blit傳入物件和她的位置

        pygame.draw.line(screen, (211, 214, 218), (0, 52), (1000, 52))  # 畫出直線

        KeyBoard = draw_keyboard()  # 畫出鍵盤來

        # 畫出使用者已經輸入的單字
        y = T_MARGIN
        for i in range(6):
            x = LR_MARGIN
            for j in range(5):

                # 畫出正方形的格子
                square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)  # 回傳rect(rectangle)物件
                pygame.draw.rect(screen, (211, 214, 218), square, width=2, border_radius=1)  # 畫出正方形，邊寬為2

                # 畫出已經猜過的單字
                if i < len(GUESSES):
                    color = determine_color(GUESSES[i], j)  # 決定在GUESSES這個字串中，第j個index的顏色
                    if color is YELLOW or color is GREEN:
                        if color is YELLOW and Word_color.get(GUESSES[i][j]) is not None and Word_color[GUESSES[i][j]] is GREEN:
                            pass
                        else:
                            Word_color[GUESSES[i][j]] = color

                    pygame.draw.rect(screen, color, square, border_radius=1)  # 畫出有顏色的正方形

                    letter = FONT.render(GUESSES[i][j], True, (255, 255, 255))  # 畫出字體
                    surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))  # 調整字體位置
                    screen.blit(letter, surface)  # blit是繪製，更新畫面，產生字體

                # 使用者正在輸入的文字
                if i == len(GUESSES) and j < len(INPUT):
                    letter = FONT.render(INPUT[j], True, (0, 0, 0))
                    surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                    screen.blit(letter, surface)

                x += SQ_SIZE + MARGIN
            y += SQ_SIZE + MARGIN

        # 遊戲結束的條件，就是使用者猜字串已經猜6次了
        if len(GUESSES) == 6 and GUESSES[5] != ANSWER:
            GAME_OVER = True
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH / 2 - 120, HEIGHT / 2 - 35, 340, 210), border_radius=3)
            letters = SMLL_FONT.render("The answer is " + ANSWER, True, (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
            letters_location = letters.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2))  # 回傳一個位置
            letters_2 = SMLL_FONT.render("Press space to restart the game or", True,
                                         (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
            letters_location_2 = letters_2.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2 + 70))  # 回傳一個位置
            letters_3 = SMLL_FONT.render("Press esc to leave", True, (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
            letters_location_3 = letters_3.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2 + 140))  # 回傳一個位置

            screen.blit(letters, letters_location)  # screen.blit傳入物件和她的位置
            screen.blit(letters_2, letters_location_2)  # screen.blit傳入物件和她的位置
            screen.blit(letters_3, letters_location_3)  # screen.blit傳入物件和她的位置
            pygame.display.flip()

        if GAME_OVER:  # 代表得到正確答案了
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH / 2 - 120, HEIGHT / 2 - 35, 340, 210), border_radius=3)
            letters = SMLL_FONT.render("You get the answer! Congratulation!", True,
                                       (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
            letters_location = letters.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2))  # 回傳一個位置
            letters_2 = SMLL_FONT.render("Press space to restart the game or", True,
                                         (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
            letters_location_2 = letters_2.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2 + 70))  # 回傳一個位置
            letters_3 = SMLL_FONT.render("Press esc to leave", True, (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
            letters_location_3 = letters_3.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2 + 140))  # 回傳一個位置

            screen.blit(letters, letters_location)  # screen.blit傳入物件和她的位置
            screen.blit(letters_2, letters_location_2)  # screen.blit傳入物件和她的位置
            screen.blit(letters_3, letters_location_3)  # screen.blit傳入物件和她的位置
            pygame.display.flip()

        # 更新視窗，有兩個方法pygame.display.flip pygame.display.update。差別在此文:
        # https://stackoverflow.com/questions/29314987/difference-between-pygame-display-update-and-pygame-display-flip
        pygame.display.flip()

        MENU_MOUSE_POS = pygame.mouse.get_pos()  # 獲得滑鼠的位置

        # 追蹤使用者事件
        for event in pygame.event.get():

            # 關閉視窗還有animating設定會False
            if event.type == pygame.QUIT:
                animating = False

            # 使用者按下按鈕的事件
            elif event.type == pygame.KEYDOWN:

                # 按下esc離開，animating設定為false。
                if event.key == pygame.K_ESCAPE:
                    animating = False

                # 按下倒退建(BACKSPACE)，就是把
                if event.key == pygame.K_BACKSPACE:
                    if len(INPUT) > 0:
                        INPUT = INPUT[:len(INPUT) - 1]

                # 按下確認鍵(return key)，繳交我們的答案。
                elif event.key == pygame.K_RETURN:
                    if INPUT not in DICT_GUESSING:  # 如果輸入的不是字典裏面的單字
                        pygame.draw.rect(screen, (0, 0, 0), (WIDTH / 2 - 50, HEIGHT / 2 - 35, 200, 70), border_radius=3)
                        letters = SMLL_FONT.render("Not in word list", True, (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
                        letters_location = letters.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2))  # 回傳一個位置
                        screen.blit(letters, letters_location)  # screen.blit傳入物件和她的位置

                        pygame.display.flip()
                        pygame.time.wait(1000)

                    elif len(INPUT) == 5 and INPUT in DICT_GUESSING:
                        GUESSES.append(INPUT)
                        GAME_OVER = True if INPUT == ANSWER else False
                        INPUT = ""  # 把input回到最初

                # 空白建(space bar)是從新開始遊戲
                elif event.key == pygame.K_SPACE:
                    GAME_OVER = False
                    ANSWER = random.choice(DICT_GUESSING)
                    GUESSES = []
                    UNGUESSED = ALPHABET
                    INPUT = ""

                # 一般的使用者輸入， 一直把文字加到input後
                elif len(INPUT) < 5 and not GAME_OVER:
                    INPUT = INPUT + event.unicode.upper()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 按下下面鍵盤的時候
                for one_button in KeyBoard:
                    if one_button.check_input(MENU_MOUSE_POS):
                        if one_button.text_input == "ENTER":
                            if INPUT not in DICT_GUESSING:  # 如果輸入的不是字典裏面的單字
                                pygame.draw.rect(screen, (0, 0, 0), (WIDTH / 2 - 50, HEIGHT / 2 - 35, 200, 70),
                                                 border_radius=3)
                                letters = SMLL_FONT.render("Not in word list", True,
                                                           (255, 255, 255))  # 我們要畫的物件 這邊是WORDLE標誌
                                letters_location = letters.get_rect(center=(WIDTH / 2 + 50, HEIGHT / 2))  # 回傳一個位置
                                screen.blit(letters, letters_location)  # screen.blit傳入物件和她的位置

                                pygame.display.flip()
                                pygame.time.wait(1000)
                            elif len(INPUT) == 5 and INPUT in DICT_GUESSING:
                                GUESSES.append(INPUT)
                                UNGUESSED = determine_unguessed_letters(GUESSES)
                                GAME_OVER = True if INPUT == ANSWER else False
                                INPUT = ""  # 把input回到最初
                        elif one_button.text_input == "BACK":
                            if len(INPUT) > 0:
                                INPUT = INPUT[:len(INPUT) - 1]
                        elif len(INPUT) < 5 and not GAME_OVER:
                            INPUT = INPUT + one_button.text_input
                        break
