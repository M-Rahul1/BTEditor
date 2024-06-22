import pygame,os
import threading

class PygameSimulation(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.energy_storage = 100
        self.energy_usage = 0
        self.renewable_energy = 0
        self.current_task = None
        self.systems = []
        self.line_colors = {
            'critical': (0, 0, 0),
            'non_critical': (0, 0, 0),
            'renewable': (0, 0, 0),
            'stored': (0, 0, 0)
        }

    def run(self):
        pygame.init()
        WIDTH, HEIGHT = 1000, 800
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Smart Hospital Energy Management Simulation")

        # Load images
        background_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'icons/play.png'))
        hospital_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'icons/play.png'))
        critical_system_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'icons/play.png'))
        hvac_system_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'icons/play.png'))
        lighting_system_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'icons/play.png'))
        renewable_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'icons/play.png'))

        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        GREY = (192, 192, 192)

        class System:
            def __init__(self, x, y, label, energy_consumption, image):
                self.rect = pygame.Rect(x, y, 100, 100)
                self.label = label
                self.energy_consumption = energy_consumption
                self.is_powered = False
                self.image = image

            def draw(self, win):
                win.blit(self.image, (self.rect.x, self.rect.y))
                color = GREEN if self.is_powered else RED
                pygame.draw.rect(win, color, self.rect, 2)
                font = pygame.font.SysFont(None, 24)
                text = font.render(self.label, True, BLACK)
                win.blit(text, (self.rect.x + 5, self.rect.y + 105))

        run = True
        clock = pygame.time.Clock()

        hospital_system = System(400, 400, "Hospital", 0, hospital_img)
        critical_system = System(100, 100, "Critical System", 3, critical_system_img)
        hvac_system = System(300, 100, "HVAC System", 3, hvac_system_img)
        lighting_system = System(500, 100, "Lighting System", 3, lighting_system_img)
        renewable_system = System(800, 100, "Renewable", 0, renewable_img)
        self.systems = [hospital_system, critical_system, hvac_system, lighting_system, renewable_system]

        while run:
            if not self.running:
                pygame.quit()
                break

            clock.tick(60)
            WIN.fill(WHITE)
            WIN.blit(background_img, (0, 0))  # Draw background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for system in self.systems:
                system.draw(WIN)

            # Draw connecting lines
            self.draw_line(WIN, hospital_system, critical_system, 'critical')
            self.draw_line(WIN, hospital_system, hvac_system, 'non_critical')
            self.draw_line(WIN, hospital_system, lighting_system, 'non_critical')
            self.draw_line(WIN, renewable_system, hospital_system, 'renewable')

            # Display energy storage level
            font = pygame.font.SysFont(None, 48)
            energy_text = font.render(f'Energy Storage: {self.energy_storage}%', True, BLACK)
            WIN.blit(energy_text, (650, 50))

            # Update the behavior tree
            if hasattr(self, 'bt_tree'):
                self.bt_tree.tick()

            pygame.display.update()

        pygame.quit()

    def draw_line(self, win, system1, system2, line_type):
        pygame.draw.line(win, self.line_colors[line_type], 
                         (system1.rect.centerx, system1.rect.centery), 
                         (system2.rect.centerx, system2.rect.centery), 5)

    def execute_action(self, action: str):
        if action == "power_critical_system":
            self.power_critical_system()
            self.line_colors['critical'] = (0, 255, 0)  # Green color to indicate power flow
        elif action == "power_non_critical_system":
            self.power_non_critical_system()
            self.line_colors['non_critical'] = (0, 255, 0)  # Green color to indicate power flow
        elif action == "store_excess_energy":
            self.store_excess_energy()
            self.line_colors['renewable'] = (0, 255, 0)  # Green color to indicate energy storage
        elif action == "use_stored_energy":
            self.use_stored_energy()
            self.line_colors['stored'] = (0, 255, 0)  # Green color to indicate energy usage

    def power_critical_system(self):
        if self.energy_storage > self.systems[1].energy_consumption:
            self.systems[1].is_powered = True
            self.energy_storage -= self.systems[1].energy_consumption

    def power_non_critical_system(self):
        for system in self.systems[2:4]:
            if not system.is_powered and self.energy_storage > system.energy_consumption:
                system.is_powered = True
                self.energy_storage -= system.energy_consumption

    def store_excess_energy(self):
        self.energy_storage += self.renewable_energy
        self.renewable_energy = 4
        self.energy_storage = min(self.energy_storage, 100)

    def use_stored_energy(self):
        for system in self.systems:
            if not system.is_powered and self.energy_storage > system.energy_consumption:
                system.is_powered = True
                self.energy_storage -= system.energy_consumption

    def start_simulation(self):
        self.running = True
        self.start()

    def stop_simulation(self):
        self.running = False
        self.join()