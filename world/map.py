import pygame as pg
import random
from settings import *


class Map:
    """Verwaltet die Spielkarte mit Tiles und Hindernissen"""

    def __init__(self, game):
        self.game = game
        self.tile_size = TILESIZE
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self.map_data = self.generate_map()

        # Erzeuge Wände basierend auf der Map
        self.create_walls()

    def generate_map(self):
        """Erstellt eine zufällige Karte mit Wänden und offenem Raum"""
        # Initialisiere leere Karte (0 = leerer Raum, 1 = Wand)
        map_data = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Rand der Karte mit Wänden füllen
        for x in range(self.width):
            map_data[0][x] = 1
            map_data[self.height - 1][x] = 1
        for y in range(self.height):
            map_data[y][0] = 1
            map_data[y][self.width - 1] = 1

        # Einige zufällige Hindernisse hinzufügen
        for _ in range(20):  # Anzahl der Hindernisse
            # Position festlegen
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)

            # Unterschiedliche Hindernisformen
            shape = random.choice(['block', 'horizontal', 'vertical'])

            if shape == 'block':
                # 2x2 Block
                for dy in range(2):
                    for dx in range(2):
                        map_data[y + dy][x + dx] = 1
            elif shape == 'horizontal':
                # Horizontale Linie
                length = random.randint(3, 5)
                for dx in range(length):
                    if x + dx < self.width - 1:
                        map_data[y][x + dx] = 1
            elif shape == 'vertical':
                # Vertikale Linie
                length = random.randint(3, 5)
                for dy in range(length):
                    if y + dy < self.height - 1:
                        map_data[y + dy][x] = 1

        # Stelle sicher, dass der Spieler-Startpunkt frei ist
        center_x = self.width // 2
        center_y = self.height // 2
        for y in range(center_y - 2, center_y + 3):
            for x in range(center_x - 2, center_x + 3):
                map_data[y][x] = 0

        return map_data

    def create_walls(self):
        """Erstellt Wand-Sprites basierend auf der Karte"""
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 1:  # Wand
                    Wall(self.game, col, row)

    def draw(self, screen):
        """Zeichnet die Karte auf den Bildschirm"""
        # Hintergrund zeichnen
        for y in range(self.height):
            for x in range(self.width):
                rect = pg.Rect(x * self.tile_size, y * self.tile_size,
                               self.tile_size, self.tile_size)

                # Unterschiedliche Farben für verschiedene Tile-Typen
                if self.map_data[y][x] == 0:  # Freier Raum
                    pg.draw.rect(screen, DARKGREY, rect)
                    # Gittermuster für bessere Visualisierung
                    pg.draw.rect(screen, BLACK, rect, 1)


class Wall(pg.sprite.Sprite):
    """Hindernisse, die den Spieler und Zombies blockieren"""

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Bild und Rect
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        # Position in Tile-Koordinaten speichern
        self.x = x
        self.y = y