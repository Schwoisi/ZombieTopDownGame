import pygame as pg
import sys
from os import path
from settings import *
from sprites.player import Player
from sprites.zombie import NormalZombie, FastZombie, StrongZombie
from sprites.projectile import Bullet
from sprites.powerup import HealthPowerup, AmmoPowerup, SpeedPowerup
from world.map import Map
from waves.wave_manager import WaveManager
from ui.hud import HUD


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()  # Für Sound-Effekte
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True
        self.paused = False
        self.game_over = False

    def load_data(self):
        """Laden aller externen Dateien (Bilder, Sounds, etc.)"""
        self.game_folder = path.dirname(__file__)
        self.assets_folder = path.join(self.game_folder, 'assets')
        self.images_folder = path.join(self.assets_folder, 'images')
        self.sounds_folder = path.join(self.assets_folder, 'sounds')

        # Hier würden wir Bilder und Sounds laden
        # Beispiel: self.player_img = pg.image.load(path.join(self.images_folder, 'player.png')).convert_alpha()

        # Temporäre Platzhalter für Sprites
        self.player_img = pg.Surface((PLAYER_SIZE, PLAYER_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.player_img, BLUE, (PLAYER_SIZE // 2, PLAYER_SIZE // 2), PLAYER_SIZE // 2)

        self.zombie_normal_img = pg.Surface((ZOMBIE_NORMAL_SIZE, ZOMBIE_NORMAL_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.zombie_normal_img, GREEN, (ZOMBIE_NORMAL_SIZE // 2, ZOMBIE_NORMAL_SIZE // 2),
                       ZOMBIE_NORMAL_SIZE // 2)

        self.zombie_fast_img = pg.Surface((ZOMBIE_FAST_SIZE, ZOMBIE_FAST_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.zombie_fast_img, YELLOW, (ZOMBIE_FAST_SIZE // 2, ZOMBIE_FAST_SIZE // 2),
                       ZOMBIE_FAST_SIZE // 2)

        self.zombie_strong_img = pg.Surface((ZOMBIE_STRONG_SIZE, ZOMBIE_STRONG_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.zombie_strong_img, RED, (ZOMBIE_STRONG_SIZE // 2, ZOMBIE_STRONG_SIZE // 2),
                       ZOMBIE_STRONG_SIZE // 2)

        self.bullet_img = pg.Surface((BULLET_SIZE, BULLET_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.bullet_img, WHITE, (BULLET_SIZE // 2, BULLET_SIZE // 2), BULLET_SIZE // 2)

        # Power-Up Platzhalter
        self.health_powerup_img = pg.Surface((TILESIZE // 2, TILESIZE // 2), pg.SRCALPHA)
        pg.draw.rect(self.health_powerup_img, RED, (0, 0, TILESIZE // 2, TILESIZE // 2))

        self.ammo_powerup_img = pg.Surface((TILESIZE // 2, TILESIZE // 2), pg.SRCALPHA)
        pg.draw.rect(self.ammo_powerup_img, YELLOW, (0, 0, TILESIZE // 2, TILESIZE // 2))

        self.speed_powerup_img = pg.Surface((TILESIZE // 2, TILESIZE // 2), pg.SRCALPHA)
        pg.draw.rect(self.speed_powerup_img, BLUE, (0, 0, TILESIZE // 2, TILESIZE // 2))

    def new(self):
        """Startet ein neues Spiel"""
        # Sprite-Gruppen erstellen
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()

        # Spielkarte laden
        self.map = Map(self)

        # Spieler erstellen
        self.player = Player(self, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.player)

        # Wellen-Manager initialisieren
        self.wave_manager = WaveManager(self)

        # HUD initialisieren
        self.hud = HUD(self)

        # Spiel starten
        self.run()

    def run(self):
        """Game-Loop"""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # Zeitdelta in Sekunden
            self.events()
            if not self.paused and not self.game_over:
                self.update()
            self.draw()

    def events(self):
        """Event-Handler"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused

                if self.game_over and event.key == pg.K_r:
                    self.game_over = False  # Game Over-Status zurücksetzen
                    self.playing = False    # Aktuelle Spielschleife beenden, damit new() aufgerufen wird

    def update(self):
        """Aktualisiert alle Sprites und Spielzustände"""
        # Wellen-Manager aktualisieren
        self.wave_manager.update()

        # Alle Sprites aktualisieren
        self.all_sprites.update()

        # Kollisionserkennung für Projektile
        hits = pg.sprite.groupcollide(self.zombies, self.bullets, False, True)
        for zombie, bullets in hits.items():
            for bullet in bullets:
                zombie.take_damage(BULLET_DAMAGE)

        # Kollision Spieler mit Zombies
        hits = pg.sprite.spritecollide(self.player, self.zombies, False)
        for zombie in hits:
            self.player.take_damage(zombie.damage)
            # Knockback könnte hier hinzugefügt werden

        # Kollision Spieler mit Power-Ups
        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in hits:
            powerup.apply(self.player)

        # Prüfen, ob Spieler tot ist
        if self.player.health <= 0:
            self.game_over = True

    def draw(self):
        """Rendert den Spielbildschirm"""
        self.screen.fill(DARKGREY)

        # Karte zeichnen
        self.map.draw(self.screen)

        # Alle Sprites zeichnen
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        # HUD zeichnen
        self.hud.draw()

        # Pause- oder Game-Over-Bildschirm anzeigen
        if self.paused:
            self.draw_pause_screen()
        elif self.game_over:
            self.draw_game_over_screen()

        pg.display.flip()

    def draw_pause_screen(self):
        """Zeigt Pause-Bildschirm an"""
        s = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
        s.fill((0, 0, 0, 128))  # Halb-transparentes Schwarz
        self.screen.blit(s, (0, 0))

        font = pg.font.Font(None, 64)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        font = pg.font.Font(None, 32)
        text = font.render("Press ESC to continue", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(text, text_rect)

    def draw_game_over_screen(self):
        """Zeigt Game-Over-Bildschirm an"""
        s = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
        s.fill((0, 0, 0, 128))  # Halb-transparentes Schwarz
        self.screen.blit(s, (0, 0))

        font = pg.font.Font(None, 64)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        font = pg.font.Font(None, 32)
        text = font.render(f"Wave: {self.wave_manager.current_wave}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(text, text_rect)

        text = font.render("Press R to restart", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(text, text_rect)


# Hauptprogramm
if __name__ == "__main__":
    g = Game()
    while g.running:
        g.new()
    pg.quit()
    sys.exit()