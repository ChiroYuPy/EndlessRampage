import pygame
from pygame import Vector2


class XpBar:
    def __init__(self, pos):
        self.width = 320
        self.height = 12
        self.pos = pos - Vector2(self.width / 2, self.height / 2)

        self.max_xp = 100
        self.xp = 0

        self.skill_points = 0

        self.level = 0

    def draw(self, window):
        pygame.draw.rect(window,
                         '#b8e2fd',
                         (self.pos.x, self.pos.y - 20, self.width, self.height),
                         border_radius=8)

        pygame.draw.rect(window,
                         '#2790d6',
                         (self.pos.x, self.pos.y - 20, (self.width * self.xp / self.max_xp), self.height),
                         border_radius=8)

        text_font = pygame.font.Font(None, 24)
        text1 = text_font.render(str(self.xp), True, '#2790d6')
        text2 = text_font.render('/', True, '#dbb72c')
        text3 = text_font.render(str(self.max_xp), True, '#ec602d')
        text4 = text_font.render('Lvl.', True, '#9ee523')
        text5 = text_font.render(str(self.level), True, '#4dc514')

        text1_pos = (self.pos.x, self.pos.y)
        text2_pos = (text1_pos[0] + text1.get_width() + 3, text1_pos[1])
        text3_pos = (text2_pos[0] + text2.get_width() + 3, text1_pos[1])
        text4_pos = (self.pos.x + self.width - text4.get_width() - text5.get_width(), self.pos.y)
        text5_pos = (self.pos.x + self.width - text5.get_width(), self.pos.y)

        window.blit(text1, text1_pos)
        window.blit(text2, text2_pos)
        window.blit(text3, text3_pos)
        window.blit(text4, text4_pos)
        window.blit(text5, text5_pos)

    def update_xp(self, value):
        self.xp += value
        if self.xp > self.max_xp:
            self.xp -= self.max_xp
            self.update_xp(0)
            self.level += 1
            self.skill_points += 1
            self.max_xp = round(100 * (1.1 ** self.level))
