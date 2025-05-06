import pygame as pg
import random
from settings import *


class Zombie(pg.sprite.Sprite):
    """Basis-Klasse für alle Zombie-Typen"""

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.zombies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Position und Bewegung
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0, 0)

        # Attribute werden in Unterklassen gesetzt
        self.speed = 0
        self.health = 0
        self.damage = 0

        # Bild und Rect werden in Unterklassen gesetzt
        self.image = None
        self.rect = None

    def update(self):
        """Aktualisiert Position und Zustand des Zombies"""
        # Richtung zum Spieler berechnen
        target = self.game.player.pos
        self.vel = target - self.pos

        # Normalisieren und Geschwindigkeit anwenden
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

        # Position aktualisieren
        old_pos = self.pos.copy()  # Position für Kollisionsprüfung merken
        self.pos += self.vel * self.game.dt

        # X und Y separat aktualisieren für korrekte Kollisionserkennung
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')

        self.rect.centery = self.pos.y
        self.collide_with_walls('y')

        # Rect mit endgültiger Position aktualisieren
        self.rect.center = self.pos

    def take_damage(self, amount):
        """Reduziert die Gesundheit des Zombies"""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Entfernt den Zombie und spawnt möglicherweise ein Power-Up"""
        # Mit geringer Wahrscheinlichkeit ein Power-Up droppen
        if random.random() < 0.2:  # 20% Chance
            self.drop_powerup()

        self.kill()

    def drop_powerup(self):
        """Spawnt ein zufälliges Power-Up an der Position des Zombies"""
        rand = random.random()
        if rand < 0.4:  # 40% Chance für Health
            from sprites.powerup import HealthPowerup
            HealthPowerup(self.game, self.pos.x, self.pos.y)
        elif rand < 0.8:  # 40% Chance für Ammo
            from sprites.powerup import AmmoPowerup
            AmmoPowerup(self.game, self.pos.x, self.pos.y)
        else:  # 20% Chance für Speed
            from sprites.powerup import SpeedPowerup
            SpeedPowerup(self.game, self.pos.x, self.pos.y)

    def collide_with_walls(self, dir):
        """Prüft und verhindert Kollisionen mit Wänden"""
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:  # Bewegung nach rechts
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                if self.vel.x < 0:  # Bewegung nach links
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.centerx = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:  # Bewegung nach unten
                    self.pos.y = hits[0].rect.top - self.rect.height / 2
                if self.vel.y < 0:  # Bewegung nach oben
                    self.pos.y = hits[0].rect.bottom + self.rect.height / 2
                self.vel.y = 0
                self.rect.centery = self.pos.y


class NormalZombie(Zombie):
    """Standard-Zombie mit durchschnittlichen Werten"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # Spezifische Attribute
        self.speed = ZOMBIE_NORMAL_SPEED
        self.health = ZOMBIE_NORMAL_HEALTH
        self.damage = ZOMBIE_NORMAL_DAMAGE

        # Bild und Rect
        self.image = game.zombie_normal_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class FastZombie(Zombie):
    """Schneller Zombie mit wenig Gesundheit"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # Spezifische Attribute
        self.speed = ZOMBIE_FAST_SPEED
        self.health = ZOMBIE_FAST_HEALTH
        self.damage = ZOMBIE_FAST_DAMAGE

        # Bild und Rect
        self.image = game.zombie_fast_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class StrongZombie(Zombie):
    """Starker Zombie mit viel Gesundheit und Schaden"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # Spezifische Attribute
        self.speed = ZOMBIE_STRONG_SPEED
        self.health = ZOMBIE_STRONG_HEALTH
        self.damage = ZOMBIE_STRONG_DAMAGE

        # Bild und Rect
        self.image = game.zombie_strong_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Zusätzliche Attribute für den starken Zombie
        self.can_destroy_walls = True
        self.wall_cooldown = 0