import pygame
import math

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de voiture minimaliste")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Constantes pour la voiture
CAR_WIDTH, CAR_HEIGHT = 40, 20
MAX_SPEED = 10
ACCELERATION = 0.2
FRICTION = 0.05
TURN_SPEED = 3

# Classe pour la voiture
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.velocity_x = 0
        self.velocity_y = 0
    
    def update(self):
        # Mise à jour de la position en fonction de la vitesse
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Simuler la friction
        self.speed *= (1 - FRICTION)

        # Limites pour ne pas sortir de la fenêtre
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
    
    def accelerate(self, forward=True):
        # Accélère la voiture vers l'avant ou l'arrière
        direction = 1 if forward else -1
        self.speed += ACCELERATION * direction
        self.speed = max(-MAX_SPEED, min(MAX_SPEED, self.speed))

    def turn(self, left=True):
        # Tourne la voiture à gauche ou à droite
        direction = 1 if left else -1
        self.angle += TURN_SPEED * direction

    def calculate_velocity(self):
        # Calculer la vélocité en fonction de l'angle et de la vitesse
        rad = math.radians(self.angle)
        self.velocity_x = self.speed * math.cos(rad)
        self.velocity_y = -self.speed * math.sin(rad)

    def draw(self, window):
        # Calculer les coins de la voiture
        rad = math.radians(self.angle)
        car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        
        # Dessiner le rectangle principal de la voiture
        pygame.draw.rect(car_surface, BLACK, (0, 0, CAR_WIDTH, CAR_HEIGHT))
        
        # Dessiner l'avant en rouge (plus fin et mieux centré)
        pygame.draw.rect(car_surface, RED, (CAR_WIDTH - 5, 0, 5, CAR_HEIGHT))
        
        # Pivoter la voiture
        rotated_car = pygame.transform.rotate(car_surface, self.angle)
        rect = rotated_car.get_rect(center=(self.x, self.y))
        
        # Dessiner la voiture
        window.blit(rotated_car, rect.topleft)

# Initialiser la voiture
car = Car(WIDTH // 2, HEIGHT // 2)

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

while running:
    window.fill(WHITE)  # Fond blanc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.accelerate(forward=True)
    if keys[pygame.K_DOWN]:
        car.accelerate(forward=False)
    if keys[pygame.K_LEFT]:
        car.turn(left=True)
    if keys[pygame.K_RIGHT]:
        car.turn(left=False)

    # Mise à jour de la voiture
    car.calculate_velocity()
    car.update()
    
    # Dessiner la voiture
    car.draw(window)

    # Rafraîchir l'écran
    pygame.display.update()

    # Cadence de 60 FPS
    clock.tick(60)

# Quitter pygame
pygame.quit()
