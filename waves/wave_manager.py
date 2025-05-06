import pygame as pg
import random
from settings import *
from sprites.zombie import NormalZombie, FastZombie, StrongZombie


class WaveManager:
    """Verwaltet die Zombie-Wellen und deren Fortschritt"""

    def __init__(self, game):
        self.game = game
        self.current_wave = 0
        self.wave_completed = True  # Beginnt mit keiner aktiven Welle
        self.wave_cooldown_timer = 0
        self.zombies_in_wave = 0

        # Spawn-Positionen berechnen (Bildschirmränder)
        self.spawn_positions = self.calculate_spawn_positions()

        # Erste Welle starten
        self.start_next_wave()

    def calculate_spawn_positions(self):
        """Berechnet mögliche Spawn-Positionen für Zombies am Bildschirmrand"""
        positions = []

        # Oberer Rand
        for x in range(0, SCREEN_WIDTH, 50):
            positions.append((x, -50))

        # Unterer Rand
        for x in range(0, SCREEN_WIDTH, 50):
            positions.append((x, SCREEN_HEIGHT + 50))

        # Linker Rand
        for y in range(0, SCREEN_HEIGHT, 50):
            positions.append((-50, y))

        # Rechter Rand
        for y in range(0, SCREEN_HEIGHT, 50):
            positions.append((SCREEN_WIDTH + 50, y))

        return positions

    def update(self):
        """Aktualisiert den Status der aktuellen Welle"""
        now = pg.time.get_ticks()

        # Prüfen, ob alle Zombies in der aktuellen Welle besiegt wurden
        if not self.wave_completed and len(self.game.zombies) == 0:
            self.wave_completed = True
            self.wave_cooldown_timer = now

        # Wenn Welle beendet ist und Cooldown abgelaufen, neue Welle starten
        if self.wave_completed and now - self.wave_cooldown_timer > WAVE_COOLDOWN:
            self.start_next_wave()

    def start_next_wave(self):
        """Startet die nächste Welle"""
        self.current_wave += 1
        self.wave_completed = False

        # Berechne Anzahl der Zombies für diese Welle
        self.zombies_in_wave = WAVE_BASE_ZOMBIES + (self.current_wave - 1) * WAVE_ZOMBIE_INCREMENT

        # Spawne Zombies
        self.spawn_zombies()

        # HUD-Nachricht für neue Welle
        print(f"Wave {self.current_wave} started!")

    def spawn_zombies(self):
        """Spawnt Zombies für die aktuelle Welle"""
        # Bestimme Verteilung der Zombie-Typen basierend auf der aktuellen Welle
        normal_percentage = max(0.9 - (self.current_wave * 0.05), 0.4)  # Nimmt mit jeder Welle ab
        fast_percentage = min(0.1 + (self.current_wave * 0.03), 0.4)  # Steigt mit jeder Welle
        strong_percentage = min(0.0 + (self.current_wave * 0.02), 0.2)  # Steigt ab Welle 1

        # Anzahl jedes Typs berechnen
        normal_count = int(self.zombies_in_wave * normal_percentage)
        fast_count = int(self.zombies_in_wave * fast_percentage)
        strong_count = max(0, self.zombies_in_wave - normal_count - fast_count)  # Rest

        # Zombies spawnen
        for _ in range(normal_count):
            self.spawn_random_zombie(NormalZombie)

        for _ in range(fast_count):
            self.spawn_random_zombie(FastZombie)

        for _ in range(strong_count):
            self.spawn_random_zombie(StrongZombie)

    def spawn_random_zombie(self, zombie_class):
        """Spawnt einen Zombie an einer zufälligen Position am Rand"""
        # Zufällige Position aus den vorberechneten Positionen wählen
        pos = random.choice(self.spawn_positions)

        # Zombie erstellen
        zombie_class(self.game, pos[0], pos[1])