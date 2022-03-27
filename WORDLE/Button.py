import pygame


class Button:
    def __init__(self, pos, width, height, text_input, font, background_color, font_color):
        self.x_pos = pos[0]  # 設定button的位置
        self.y_pos = pos[1]
        self.width = width  # 設定按鈕長度寬度
        self.height = height
        self.text_input = text_input  # 設定按鈕的文字
        self.font = font  # 設定按鈕的字形
        self.background_color = background_color  # 設定按鈕背景顏色
        self.font_color = font_color  # 設定按鈕的字形顏色

        self.text = font.render(text_input, True, font_color)  # 字形的物件
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # 字體的位置

        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # 矩形的位置

    def update(self, screen):
        pygame.draw.rect(screen, self.background_color,
                         (self.x_pos - self.width / 2, self.y_pos - self.height / 2, self.width, self.height),
                         border_radius=3)
        screen.blit(self.text, self.text_rect)

    def check_input(self, position):
        button_top = int(self.y_pos - self.height / 2)
        button_bottom = int(self.y_pos + self.height / 2)
        button_left = int(self.x_pos - self.width / 2)
        button_right = int(self.x_pos + self.width / 2)
        if position[0] not in range(button_left, button_right) or position[1] not in range(button_top, button_bottom):
            return False
        return True

    # def changeColor(self, position):
    #     if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
    #                                                                                       self.rect.bottom):
    #         self.text = self.font.render(self.text_input, True, self.hovering_color)
    #     else:
    #         self.text = self.font.render(self.text_input, True, self.base_color)
