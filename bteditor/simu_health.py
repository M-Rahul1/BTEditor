class PygameSimulation(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.current_task = None
        self.patients = []
        self.current_patient_index = 0  # Track the index of the current patient

    def run(self):
        pygame.init()
        WIDTH, HEIGHT = 1000, 800
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Healthcare System Simulation")

        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        BLACK = (0, 0, 0)
        GREY = (192, 192, 192)

        class Robot:
            def __init__(self, x, y, label):
                self.rect = pygame.Rect(x, y, 50, 50)
                self.color = BLUE
                self.speed = 5
                self.label = label

            def move_to(self, x, y):
                if self.rect.x < x:
                    self.rect.x += self.speed
                elif self.rect.x > x:
                    self.rect.x -= self.speed
                if self.rect.y < y:
                    self.rect.y += self.speed
                elif self.rect.y > y:
                    self.rect.y -= self.speed

            def draw(self, win):
                pygame.draw.rect(win, self.color, self.rect)
                font = pygame.font.SysFont(None, 24)
                text = font.render(self.label, True, BLACK)
                win.blit(text, (self.rect.x, self.rect.y - 25))

        class Patient:
            def __init__(self, x, y, label):
                self.rect = pygame.Rect(x, y, 50, 50)
                self.color = GREEN
                self.needs_help = False
                self.label = label

            def draw(self, win):
                pygame.draw.rect(win, self.color, self.rect)
                font = pygame.font.SysFont(None, 24)
                text = font.render(self.label, True, BLACK)
                win.blit(text, (self.rect.x, self.rect.y - 25))

        class Medicine:
            def __init__(self, x, y, label):
                self.rect = pygame.Rect(x, y, 30, 30)
                self.color = BLACK
                self.label = label

            def draw(self, win):
                pygame.draw.rect(win, self.color, self.rect)
                font = pygame.font.SysFont(None, 24)
                text = font.render(self.label, True, BLACK)
                win.blit(text, (self.rect.x, self.rect.y - 25))

        def draw_patient_needs_help(win, patients):
            for patient in patients:
                if patient.needs_help:
                    pygame.draw.circle(win, RED, (patient.rect.x + 25, patient.rect.y + 25), 10)
        #add medicine block to patients only after attending to them
        def draw_medicine(win, patients):
            pygame.draw.rect(win, BLACK, (patient.rect.x + 25, patient.rect.y + 25, 10, 10))
                
        run = True
        clock = pygame.time.Clock()

        robot = Robot(100, 100, "Robot")
        patients = [
            Patient(300, 300, "Patient 1"),
            Patient(600, 300, "Patient 2"),
            Patient(450, 600, "Patient 3")
        ]
        medicine = Medicine(800, 100, "Medicine")

        self.patients = patients

        while run:
            if not self.running:
                pygame.quit()
                break

            clock.tick(60)
            WIN.fill(WHITE)
            pygame.draw.rect(WIN, GREY, (0, 0, WIDTH, HEIGHT))  # Draw floor

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            robot.draw(WIN)
            medicine.draw(WIN)
            for patient in patients:
                patient.draw(WIN)

            
            if self.current_task == "needs_help":
                draw_patient_needs_help(WIN, patients)
                
            elif self.current_task == "to_medicine":
                robot.move_to(medicine.rect.x, medicine.rect.y)
            
            elif self.current_task == "deliver_to_patient":
                if robot.rect.colliderect(medicine.rect):
                    self.current_task = "deliver_medicine"
                    self.current_patient_index = 0  # Start with the first patient
            
            elif self.current_task == "deliver_medicine":
                if self.current_patient_index < len(patients):
                    patient = patients[self.current_patient_index]
                    robot.move_to(patient.rect.x, patient.rect.y)
                    if robot.rect.colliderect(patient.rect):
                        self.current_patient_index += 1  # Move to the next patient
                    draw_medicine(WIN, patients)
                else:
                    self.current_task = None  # Delivery complete

            elif self.current_task == "attend_patient":
                patient = patients[2]  # Focus only on Patient 3
                if patient.needs_help:
                    robot.move_to(patient.rect.x, patient.rect.y)
                    if robot.rect.colliderect(patient.rect):
                        patient.needs_help = False
                        self.current_task = None

            pygame.display.update()

        pygame.quit()

    def start_simulation(self):
        self.running = True
        self.start()

    def stop_simulation(self):
        self.running = False
        self.join()

    def execute_action(self, action: str):
        if action in ["to_medicine", "deliver_to_patient"]:
            self.patients[2].needs_help = False
            self.current_task = action
        elif action == "attend_patient":
            self.current_task = action
        elif action == "needs_help":
            self.current_task = action
            self.patients[2].needs_help = True