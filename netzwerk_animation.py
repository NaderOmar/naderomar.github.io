import pygame
import sys
import random
import math

# Initialisierung von Pygame
pygame.init()

# Fenstergröße und Titel
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Netzwerk-Animation")

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Schriftart für Buttons
font = pygame.font.SysFont(None, 36)

# Button-Klasse definieren
class Button:
    def __init__(self, text, pos):
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], 200, 50)
        self.color = WHITE
        self.text_surf = font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.active = True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def disable(self):
        self.color = (150, 150, 150)
        self.active = False

    def is_clicked(self, pos):
        return self.active and self.rect.collidepoint(pos)

# Partikel-Klasse definieren
class Particle:
    def __init__(self):
        self.pos = [random.uniform(0, WIDTH), random.uniform(0, HEIGHT)]
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Kantenprüfung und Umkehr der Richtung
        if self.pos[0] <= 0 or self.pos[0] >= WIDTH:
            self.vel[0] *= -1
        if self.pos[1] <= 0 or self.pos[1] >= HEIGHT:
            self.vel[1] *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.pos[0]), int(self.pos[1])), 3)

# Button erstellen
button = Button("Animation Starten", (WIDTH // 2 - 100, HEIGHT // 2 - 25))

# Liste der Partikel
particles = []
num_particles = 100  # Anzahl der Partikel
animation_active = False

# Hauptschleife
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mausklick-Ereignis
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_clicked(event.pos):
                button.disable()
                animation_active = True
                # Partikel initialisieren
                particles = [Particle() for _ in range(num_particles)]

    window.fill(BLACK)

    if not animation_active:
        button.draw(window)
    else:
        # Partikel bewegen und zeichnen
        for particle in particles:
            particle.move()
            particle.draw(window)

        # Verbindungen zwischen nahen Partikeln zeichnen
        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                dx = particles[i].pos[0] - particles[j].pos[0]
                dy = particles[i].pos[1] - particles[j].pos[1]
                dist = math.hypot(dx, dy)
                if dist < 100:
                    alpha = max(0, 255 - (dist * 2))
                    # Linie mit Transparenz (wenn unterstützt)
                    line_color = (255, 255, 255)
                    pygame.draw.line(window, line_color, particles[i].pos, particles[j].pos, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
