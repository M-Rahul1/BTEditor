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
        pygame.display.set_caption("Coffee Simulation")

        WHITE = (255, 255, 255)
        GREY = (192, 192, 192)
        BROWN = (139, 69, 19)
        BLACK = (0, 0, 0)

        class Cup:
            def __init__(self, x, y, width, height, color, label):
                self.rect = pygame.Rect(x, y, width, height)
                self.color = color
                self.label = label
                self.level = height
                self.layers = [(color, height)]

            def draw(self, win):
                y_offset = self.rect.y + self.rect.height
                for color, height in self.layers:
                    y_offset -= height
                    pygame.draw.rect(win, color, (self.rect.x, y_offset, self.rect.width, height))
                font = pygame.font.SysFont("comicsans", 16)
                label_surface = font.render(self.label, True, WHITE)
                win.blit(label_surface, (self.rect.x - 120, self.rect.y))

            def transfer_content(self, amount, color):
                new_level = max(0, self.level - amount)
                transferred_amount = self.level - new_level
                self.level = new_level
                self.rect.height = new_level
                self.rect.y += amount
                return transferred_amount, color

            def add_layer(self, amount, color):
                self.layers.append((color, amount))

        run = True
        clock = pygame.time.Clock()

        empty_cup = Cup(500, 350, 100, 0, WHITE, "Empty Cup")
        sugar_cup = Cup(300, 650, 50, 100, WHITE, "Sugar")
        milk_cup = Cup(500, 650, 50, 100, GREY, "Milk")
        coffee_cup = Cup(700, 650, 50, 100, BROWN, "Coffee")

        sugar_cup.level = 100
        milk_cup.level = 100
        coffee_cup.level = 100

        cups = {"sugar": sugar_cup, "milk": milk_cup, "coffee": coffee_cup}
        colors = {"sugar": WHITE, "milk": GREY, "coffee": BROWN}

        while run:
            if not self.running:
                pygame.quit()
                break

            clock.tick(60)
            WIN.fill((100, 100, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for cup in cups.values():
                cup.draw(WIN)
            empty_cup.draw(WIN)

            if self.current_action:
                cup = cups[self.current_action]
                amount, color = cup.transfer_content(1, colors[self.current_action])
                if amount > 0:
                    empty_cup.add_layer(amount, color)
                if cup.level <= 0:
                    self.current_action = None

            pygame.display.update()

        pygame.quit()

    def start_simulation(self):
        self.running = True
        self.start()

    def stop_simulation(self):
        self.running = False
        self.join()

    def execute_action(self, action: str):
        if action in ["sugar", "milk", "coffee"]:
            self.current_action = action
