import pygame as pg
import math
from settings import *


class PowerUp(pg.sprite.Sprite):
    """Basis-Klasse für alle Power-Ups"""

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Position
        self.pos = pg.math.Vector2(x, y)

        # Bild und Rect werden in Unterklassen gesetzt
        self.image = None
        self.rect = None

        # Animations-Parameter für visuellen Effekt
        self.bob_range = 5  # Pixel, die das Power-Up auf und ab schwebt
        self.bob_speed = 0.005  # Geschwindigkeit der Schwebebewegung
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        """Aktualisiert das Power-Up (Animation)"""
        # Berechne Y-Offset für schwebenden Effekt
        offset = math.sin((pg.time.get_ticks() - self.spawn_time) * self.bob_speed) * self.bob_range
        self.rect.centery = self.pos.y + offset

    def apply(self, player):
        """Wendet den Power-Up-Effekt auf den Spieler an"""
        pass  # In Unterklassen überschrieben


class HealthPowerup(PowerUp):
    """Stellt Gesundheit wieder her"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # Bild und Rect
        self.image = game.health_powerup_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply(self, player):
        """Stellt Gesundheit des Spielers wieder her"""
        player.heal(HEALTH_POWERUP_AMOUNT)


class AmmoPowerup(PowerUp):
    """Fügt Munition hinzu"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # Bild und Rect
        self.image = game.ammo_powerup_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply(self, player):
        """Fügt Munition hinzu"""
        player.add_ammo(AMMO_POWERUP_AMOUNT)


class SpeedPowerup(PowerUp):
    """Temporärer Geschwindigkeits-Boost"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # Bild und Rect
        self.image = game.speed_powerup_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply(self, player):
        """Aktiviert temporären Geschwindigkeits-Boost"""
        player.apply_speed_boost()