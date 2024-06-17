import pygame
import threading

class PygameSimulation(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.current_action = None

    def run(self):
        pygame.init()
        WIDTH, HEIGHT = 1000, 800
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autonomous Driving Car Simulation")

        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        YELLOW = (255, 255, 0)
        BLACK = (0, 0, 0)
        GREY = (192, 192, 192)

        class TrafficLight:
            def __init__(self, x, y):
                self.rect = pygame.Rect(x, y, 60, 180)
                self.color = YELLOW
                self.timer = 0

            def draw(self, win):
                pygame.draw.rect(win, BLACK, self.rect) 
                if self.color == RED:
                    pygame.draw.circle(win, RED, (self.rect.x + 30, self.rect.y + 30), 20)
                elif self.color == YELLOW:
                    pygame.draw.circle(win, YELLOW, (self.rect.x + 30, self.rect.y + 90), 20)
                elif self.color == GREEN:
                    pygame.draw.circle(win, GREEN, (self.rect.x + 30, self.rect.y + 150), 20)

            def change_color(self, color):
                self.color = color
                
        class Car:
            def __init__(self, x, y):
                self.rect = pygame.Rect(x, y, 50, 100)
                self.color = BLACK
                self.speed = 2
                self.lane = 1  # 1 means within lane, 0 means out of lane

            def move(self):
                if self.lane == 1:
                    self.rect.y -= self.speed
                elif self.lane == 0:
                    self.rect.x += self.speed // 2
                    if self.rect.x >= 475:
                        self.rect.x = 475
                        self.lane = 1

            def draw(self, win):
                pygame.draw.rect(win, self.color, self.rect)

        run = True
        clock = pygame.time.Clock()

        traffic_light = TrafficLight(700, 100)
        car = Car(475, 600)

        while run:
            if not self.running:
                pygame.quit()
                break

            clock.tick(60)
            WIN.fill(WHITE)
            pygame.draw.rect(WIN, GREY, (300, 0, 400, HEIGHT))  # Draw road

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            
            traffic_light.draw(WIN)
            car.draw(WIN)
            
            if self.current_action == "red":
                traffic_light.change_color(RED)
            elif self.current_action == "green":
                traffic_light.change_color(GREEN)

            if self.current_action == "stop":
                car.speed = 0
            elif self.current_action == "proceed":
                car.speed = 2
            elif self.current_action == "caution":
                car.speed = 1
            elif self.current_action == "move_into_lane":
                car.go_off_lane()
            elif self.current_action == "keep_driving":
                car.speed = 2

            if traffic_light.color == RED and car.rect.y < traffic_light.rect.y + 180:
                self.current_action = "stop"
            elif traffic_light.color == GREEN:
                self.current_action = "proceed"
            elif traffic_light.color == YELLOW:
                self.current_action = "caution"

            car.move()
            pygame.display.update()

        pygame.quit()

    def start_simulation(self):
        self.running = True
        self.start()

    def stop_simulation(self):
        self.running = False
        self.join()

    def execute_action(self, action: str):
        if action in ["red", "green"]:
            self.current_action = action