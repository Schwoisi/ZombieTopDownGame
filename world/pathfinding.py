import pygame as pg
import heapq
from settings import *


class PathFinder:
    """Einfache A* Implementation für das Zombie-Pathfinding"""

    def __init__(self, game):
        self.game = game
        self.walls = [[0 for _ in range(GRIDWIDTH)] for _ in range(GRIDHEIGHT)]
        self.update_walls()

    def update_walls(self):
        """Aktualisiert die Wandmatrix aus den aktuellen Wand-Sprites"""
        # Reset walls grid
        self.walls = [[0 for _ in range(GRIDWIDTH)] for _ in range(GRIDHEIGHT)]
        # Set walls from map
        for wall in self.game.walls:
            self.walls[wall.y][wall.x] = 1

    def find_path(self, start, end):
        """Findet einen Pfad von Start- zu Zielpunkt mit A*"""
        # Konvertiere Pixel-Koordinaten zu Grid-Koordinaten
        start_x, start_y = int(start[0] // TILESIZE), int(start[1] // TILESIZE)
        end_x, end_y = int(end[0] // TILESIZE), int(end[1] // TILESIZE)

        # Stellen Sie sicher, dass Start und Ziel innerhalb der Grenzen liegen
        if not (0 <= start_x < GRIDWIDTH and 0 <= start_y < GRIDHEIGHT and
                0 <= end_x < GRIDWIDTH and 0 <= end_y < GRIDHEIGHT):
            return []

        # Überprüfen Sie, ob Start oder Ziel in einem Hindernis liegen
        if self.walls[start_y][start_x] or self.walls[end_y][end_x]:
            return []

        # Prioritätswarteschlange für offene Knoten (f_cost, position)
        open_set = []
        heapq.heappush(open_set, (0, (start_x, start_y)))

        # Verfolgen, woher jeder Knoten kommt
        came_from = {}

        # g_score: Kosten vom Start zu jedem Knoten
        g_score = {(x, y): float('inf') for x in range(GRIDWIDTH) for y in range(GRIDHEIGHT)}
        g_score[(start_x, start_y)] = 0

        # f_score: Geschätzte Gesamtkosten (g_score + Heuristik)
        f_score = {(x, y): float('inf') for x in range(GRIDWIDTH) for y in range(GRIDHEIGHT)}
        f_score[(start_x, start_y)] = self.heuristic((start_x, start_y), (end_x, end_y))

        # Set für besuchte Knoten
        closed_set = set()

        while open_set:
            # Knoten mit niedrigstem f_score
            _, current = heapq.heappop(open_set)

            if current in closed_set:
                continue

            # Ziel erreicht
            if current == (end_x, end_y):
                path = self.reconstruct_path(came_from, current)
                return [(p[0] * TILESIZE + TILESIZE // 2, p[1] * TILESIZE + TILESIZE // 2) for p in path]

            closed_set.add(current)

            # Prüfe alle Nachbarn
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                # Überprüfe Grenzen
                if not (0 <= neighbor[0] < GRIDWIDTH and 0 <= neighbor[1] < GRIDHEIGHT):
                    continue

                # Überprüfe Hindernisse
                if self.walls[neighbor[1]][neighbor[0]]:
                    continue

                # Diagonale Bewegung in Wände vermeiden
                if dx != 0 and dy != 0:  # Diagonaler Schritt
                    if self.walls[current[1]][neighbor[0]] or self.walls[neighbor[1]][current[0]]:
                        continue

                # Berechne g_score für Nachbarn
                # Diagonale Bewegung kostet √2 ≈ 1.414
                move_cost = 1.414 if dx != 0 and dy != 0 else 1
                tentative_g_score = g_score[current] + move_cost

                if tentative_g_score < g_score[neighbor]:
                    # Dies ist ein besserer Weg
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, (end_x, end_y))
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Kein Pfad gefunden
        return []

    def heuristic(self, a, b):
        """Schätzt die Kosten von a nach b mit der Manhattan-Distanz"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        """Rekonstruiert den Pfad von Start zu Ziel"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]  # Umkehren, um vom Start zum Ziel zu gehen