import pygame as pg
import math
from settings import *
from sprites.projectile import Bullet


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Bild und Rect
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Position und Bewegung
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED

        # Spieler-Attribute
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.ammo = 50  # Anfangsmunition
        self.last_shot = 0  # Zeitpunkt des letzten Schusses

        # Power-Up-Status
        self.speed_boost_active = False
        self.speed_boost_timer = 0

    def get_keys(self):
        """Verarbeitet Tastatureingaben für die Bewegung"""
        self.vel = pg.math.Vector2(0, 0)
        keys = pg.key.get_pressed()

        # Bewegung in 8 Richtungen
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = self.speed

        # Diagonale Bewegung normalisieren (gleiche Geschwindigkeit in alle Richtungen)
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

    def get_mouse(self):
        """Verarbeitet Mauseingaben für das Schießen"""
        mouse_buttons = pg.mouse.get_pressed()
        now = pg.time.get_ticks()

        # Linke Maustaste zum Schießen
        if mouse_buttons[0] and now - self.last_shot > PLAYER_COOLDOWN and self.ammo > 0:
            self.shoot()
            self.last_shot = now
            self.ammo -= 1

    def shoot(self):
        """Erstellt ein neues Projektil in Richtung Mauszeiger"""
        # Berechne Richtung zum Mauszeiger
        mouse_x, mouse_y = pg.mouse.get_pos()
        dir_x = mouse_x - self.pos.x
        dir_y = mouse_y - self.pos.y

        # Normalisiere den Richtungsvektor
        length = math.sqrt(dir_x ** 2 + dir_y ** 2)
        if length > 0:
            dir_x /= length
            dir_y /= length

        # Erstelle das Projektil
        Bullet(self.game, self.pos.x, self.pos.y, dir_x, dir_y)

    def update(self):
        """Aktualisiert Position und Status des Spielers"""
        # Eingaben verarbeiten
        self.get_keys()
        self.get_mouse()

        # Aktualisiere Position basierend auf Geschwindigkeit
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # Kollisionserkennung mit Wänden
        self.collide_with_walls()

        # Power-Up-Timer aktualisieren
        self.update_powerups()

    def collide_with_walls(self):
        """Prüft und verhindert Kollisionen mit Wänden"""
        # X-Achse
        self.rect.centerx = self.pos.x
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            if self.vel.x > 0:  # Bewegung nach rechts
                self.pos.x = hits[0].rect.left - self.rect.width / 2
            if self.vel.x < 0:  # Bewegung nach links
                self.pos.x = hits[0].rect.right + self.rect.width / 2
            self.rect.centerx = self.pos.x

        # Y-Achse
        self.rect.centery = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            if self.vel.y > 0:  # Bewegung nach unten
                self.pos.y = hits[0].rect.top - self.rect.height / 2
            if self.vel.y < 0:  # Bewegung nach oben
                self.pos.y = hits[0].rect.bottom + self.rect.height / 2
            self.rect.centery = self.pos.y

    def update_powerups(self):
        """Aktualisiert und verwaltet aktive Power-Ups"""
        now = pg.time.get_ticks()

        # Speed-Boost verwalten
        if self.speed_boost_active:
            if now - self.speed_boost_timer > POWERUP_DURATION:
                self.speed_boost_active = False
                self.speed = PLAYER_SPEED  # Zurück zur normalen Geschwindigkeit

    def take_damage(self, amount):
        """Reduziert die Gesundheit des Spielers"""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """Erhöht die Gesundheit des Spielers"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def add_ammo(self, amount):
        """Fügt Munition hinzu"""
        self.ammo += amount

    def apply_speed_boost(self):
        """Aktiviert einen temporären Geschwindigkeits-Boost"""
        self.speed_boost_active = True
        self.speed_boost_timer = pg.time.get_ticks()
        self.speed = PLAYER_SPEED * SPEED_POWERUP_MULTIPLIER