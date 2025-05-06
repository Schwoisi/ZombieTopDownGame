import pygame as pg
from settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, dir_x, dir_y):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Bild und Rect
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Position und Bewegung
        self.pos = pg.math.Vector2(x, y)
        self.dir = pg.math.Vector2(dir_x, dir_y)
        self.speed = BULLET_SPEED

        # Lebensdauer des Projektils
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        """Aktualisiert Position und prüft Lebensdauer"""
        # Aktualisiere Position
        self.pos += self.dir * self.speed
        self.rect.center = self.pos

        # Entferne Projektil, wenn es zu lange existiert oder mit Wänden kollidiert
        now = pg.time.get_ticks()
        if now - self.spawn_time > BULLET_LIFETIME:
            self.kill()

        # Prüfen auf Kollision mit Wänden
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()