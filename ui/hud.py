import pygame as pg
from settings import *


class HUD:
    """Verwaltet die Benutzeroberfläche (HUD)"""

    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 28)
        self.large_font = pg.font.Font(None, 48)

    def draw(self):
        """Zeichnet alle HUD-Elemente"""
        self.draw_health_bar()
        self.draw_ammo_counter()
        self.draw_wave_info()
        self.draw_wave_transition()

    def draw_health_bar(self):
        """Zeichnet die Gesundheitsleiste des Spielers"""
        # Hintergrund
        health_bar_width = 200
        health_bar_height = 20
        outline_rect = pg.Rect(10, 10, health_bar_width, health_bar_height)
        pg.draw.rect(self.game.screen, BLACK, outline_rect)

        # Berechne aktuelle Gesundheit als Prozentsatz
        health_percent = self.game.player.health / self.game.player.max_health

        # Innere Leiste
        if health_percent > 0.7:
            color = GREEN
        elif health_percent > 0.3:
            color = YELLOW
        else:
            color = RED

        # Innere Leiste basierend auf aktueller Gesundheit
        inner_width = int(health_bar_width * health_percent)
        inner_rect = pg.Rect(10, 10, inner_width, health_bar_height)
        pg.draw.rect(self.game.screen, color, inner_rect)

        # Text für Gesundheit
        health_text = f"Health: {self.game.player.health}/{self.game.player.max_health}"
        text_surface = self.font.render(health_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(110, 20))
        self.game.screen.blit(text_surface, text_rect)

    def draw_ammo_counter(self):
        """Zeichnet den Munitionszähler"""
        ammo_text = f"Ammo: {self.game.player.ammo}"
        text_surface = self.font.render(ammo_text, True, WHITE)
        self.game.screen.blit(text_surface, (10, 40))

    def draw_wave_info(self):
        """Zeichnet die Welleninformation"""
        wave_text = f"Wave: {self.game.wave_manager.current_wave}"
        text_surface = self.font.render(wave_text, True, WHITE)
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.game.screen.blit(text_surface, text_rect)

        # Anzahl der verbleibenden Zombies anzeigen
        zombies_text = f"Zombies: {len(self.game.zombies)}"
        text_surface = self.font.render(zombies_text, True, WHITE)
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 40))
        self.game.screen.blit(text_surface, text_rect)

    def draw_wave_transition(self):
        """Zeigt eine Nachricht beim Übergang zwischen Wellen an"""
        # Nur anzeigen, wenn zwischen den Wellen
        if self.game.wave_manager.wave_completed and not self.game.game_over:
            now = pg.time.get_ticks()
            time_left = (WAVE_COOLDOWN - (now - self.game.wave_manager.wave_cooldown_timer)) // 1000

            if time_left >= 0:
                # Halbtransparenter Hintergrund
                s = pg.Surface((SCREEN_WIDTH, 80), pg.SRCALPHA)
                s.fill((0, 0, 0, 128))
                self.game.screen.blit(s, (0, SCREEN_HEIGHT // 2 - 40))

                # Wave-Text
                wave_text = f"Wave {self.game.wave_manager.current_wave} completed!"
                text_surface = self.large_font.render(wave_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                self.game.screen.blit(text_surface, text_rect)

                # Countdown-Text
                next_wave_text = f"Next wave in {time_left + 1}..."
                text_surface = self.font.render(next_wave_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.game.screen.blit(text_surface, text_rect)