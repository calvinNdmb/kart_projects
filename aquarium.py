import pygame
import math
import random

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de voitures minimalistes")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Constantes pour la voiture
CAR_WIDTH, CAR_HEIGHT = 40, 20
MAX_SPEED = 15
ACCELERATION = 0.3
FRICTION = 0.01
TURN_SPEED = 3
CHANGE_DECISION_PROBABILITY = 1  # Probabilité de changer de direction ou de vitesse à chaque frame

# Classe pour la voiture
class Car:
    def __init__(self, x, y, controlled=False):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 360) if not controlled else 0
        self.speed = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.controlled = controlled
        self.autonomous = not controlled
        if self.autonomous:
            self.turn_direction = random.choice([-1, 1])
            self.change_direction_time = random.uniform(1, 3)

    def update(self):
        if self.controlled:
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
        else:
            # Prendre des décisions aléatoires à chaque frame
            if random.random() < CHANGE_DECISION_PROBABILITY:
                self.turn_direction = random.choice([-1, 1])
                self.speed = random.uniform(0, MAX_SPEED)
                self.angle += self.turn_direction * TURN_SPEED
            
            # Mise à jour de la position
            self.x += self.velocity_x
            self.y += self.velocity_y

            # Limites pour ne pas sortir de la fenêtre (répétition des bords)
            if self.x < 0:
                self.x = WIDTH
            elif self.x > WIDTH:
                self.x = 0
            if self.y < 0:
                self.y = HEIGHT
            elif self.y > HEIGHT:
                self.y = 0

        # Calculer la vélocité
        self.calculate_velocity()

    def accelerate(self, forward=True):
        if self.controlled:
            # Accélère la voiture vers l'avant ou l'arrière
            direction = 1 if forward else -1
            self.speed += ACCELERATION * direction
            self.speed = max(-MAX_SPEED, min(MAX_SPEED, self.speed))

    def turn(self, left=True):
        if self.controlled:
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

# Fonction pour générer des positions aléatoires
def random_position():
    return random.randint(CAR_WIDTH, WIDTH - CAR_WIDTH), random.randint(CAR_HEIGHT, HEIGHT - CAR_HEIGHT)

# Initialiser plusieurs voitures avec des positions aléatoires
#cars = [Car(*random_position(), controlled=(i == 0)) for i in range(100)]
cars = [Car(*random_position(), controlled=True) for i in range(1)]
# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

while running:
    window.fill(WHITE)  # Fond blanc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches pour la voiture contrôlée
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        cars[0].accelerate(forward=True)
    if keys[pygame.K_DOWN]:
        cars[0].accelerate(forward=False)
    if keys[pygame.K_LEFT]:
        cars[0].turn(left=True)
    if keys[pygame.K_RIGHT]:
        cars[0].turn(left=False)

    # Mise à jour et dessin de chaque voiture
    for car in cars:
        car.update()
        car.draw(window)

    # Rafraîchir l'écran
    pygame.display.update()

    # Cadence de 60 FPS
    clock.tick(60)

# Quitter pygame
pygame.quit()
