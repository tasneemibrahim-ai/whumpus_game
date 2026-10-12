import random
import tkinter as tk
from tkinter import messagebox

class KnowledgeBase:
    def __init__(self, size):
        self.size = size
        self.rooms = set()
        self.wumpus = None
        self.gold = None
        self.grabbed_gold = set()
        self.pits = set()

    def initialize(self):
        self._generate_rooms()
        self._generate_wumpus()
        self._generate_gold()
        self._generate_pits()

    def _generate_rooms(self):
        self.rooms = {(x, y) for x in range(1, self.size + 1) for y in range(1, self.size + 1)}

    def _generate_wumpus(self):
        self.wumpus = random.sample(list(self.rooms), 1)[0]

    def _generate_gold(self):
        self.gold = random.sample(list(self.rooms - {self.wumpus}), 1)[0]

    def _generate_pits(self):
        num_pits = random.randint(1, min(len(self.rooms) - 2, 5))
        self.pits = set(random.sample(list(self.rooms - {self.wumpus, self.gold}), num_pits))

    def has_wumpus(self, x, y):
        return (x, y) == self.wumpus

    def has_gold(self, x, y):
        return (x, y) == self.gold and (x, y) not in self.grabbed_gold

    def has_pit(self, x, y):
        return (x, y) in self.pits

    def grab_gold(self, x, y):
        if self.has_gold(x, y):
            self.grabbed_gold.add((x, y))
            return True
        return False

    def get_nearby_rooms(self, x, y):
        neighbors = [
            (x, y + 1),  # Up
            (x, y - 1),  # Down
            (x + 1, y),  # Right
            (x - 1, y),  # Left
        ]
        return [(nx, ny) for nx, ny in neighbors if 1 <= nx <= self.size and 1 <= ny <= self.size]

class InferenceEngine:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def infer(self, x, y):
        nearby_rooms = self.knowledge_base.get_nearby_rooms(x, y)
        messages = []

        for nx, ny in nearby_rooms:
            if self.knowledge_base.has_wumpus(nx, ny):
                messages.append("You smell a stench.")
            if self.knowledge_base.has_gold(nx, ny):
                messages.append("You see a glimmer of gold.")
            if self.knowledge_base.has_pit(nx, ny):
                messages.append("You feel a breeze.")

        if self.knowledge_base.has_wumpus(x, y):
            return "You are in the same room as the Wumpus. You are killed!"
        if self.knowledge_base.has_gold(x, y):
            return "You found the gold! Grab it to win."
        if self.knowledge_base.has_pit(x, y):
            return "You fell into a pit. Game over!"
        return "\n".join(messages) if messages else "The room feels safe."

    def update_knowledge_base(self, x, y):
        self.knowledge_base.wumpus = None
        self.knowledge_base.gold = None

class Agent:
    def __init__(self, knowledge_base, inference_engine, visualization):
        self.knowledge_base = knowledge_base
        self.inference_engine = inference_engine
        self.visualization = visualization
        self.current_position = (1, 1)
        self.score = 0
        self.max_moves = 20
        self.move_left = self.max_moves
        self.output_text = ""

    def move(self, direction):
        if self.move_left <= 0:
            self.append_output("Out of moves. Game over.")
            return

        if not self._is_valid_move(direction):
            self.append_output(f"You cannot move further {direction}.")
            return

        x, y = self.current_position
        if direction == "up":
            y += 1
        elif direction == "down":
            y -= 1
        elif direction == "right":
            x += 1
        elif direction == "left":
            x -= 1

        self.current_position = (x, y)
        self.move_left -= 1
        self.update_perceptions()
        self.update_score(-1)

        # Check for hazards after moving
        if self.check_for_perils(x, y):
            self.append_output("You encountered danger. Game over.")
            self.move_left = 0  # End the game immediately

    def grab(self):
        x, y = self.current_position
        if self.knowledge_base.grab_gold(x, y):
            self.append_output("You picked the gold successfully.")
            self.update_score(20)
            self.knowledge_base.gold = None
            self.knowledge_base.grabbed_gold.add((1, 1))
        else:
            self.append_output("There is no gold in this room.")

    def _is_valid_move(self, direction):
        x, y = self.current_position
        return (
            (direction == "up" and y < self.knowledge_base.size) or
            (direction == "down" and y > 1) or
            (direction == "right" and x < self.knowledge_base.size) or
            (direction == "left" and x > 1)
        )

    def update_perceptions(self):
        x, y = self.current_position
        message = self.inference_engine.infer(x, y)
        self.append_output(message)

    def update_score(self, points):
        self.score += points
        self.append_output(f"Current Score: {self.score}")
        self.append_output(f"Moves Left: {self.move_left}")

    def end_game(self):
        x, y = self.current_position
        if (x, y) == (1, 1) and (1, 1) in self.knowledge_base.grabbed_gold:
            if self.score >= 0:
                self.append_output("Congratulations! You have climbed out of the cave with the gold.")
                self.visualization.show_message("Congratulations! You have won.")
                self.visualization.root.destroy()
            else:
                self.append_output("You cannot climb without the gold. Game over.")
        else:
            self.append_output("You can only climb from the starting position (1, 1) with the gold.")

    def check_for_perils(self, x, y):
        if self.knowledge_base.has_wumpus(x, y) or self.knowledge_base.has_pit(x, y):
            return True
        return False

    def play(self):
        while self.move_left > 0:
            self.update_visualization()
            command = input("Enter a command (up, down, right, left, grab, climb): ")
            if command.lower() == 'grab':
                self.grab()
            elif command.lower() == 'climb':
                self.end_game()
            else:
                self.move(command.lower())

        self.append_output("Game over! Out of moves.")

    def update_visualization(self):
        self.visualization.visualize()
        self.append_output(f"Current Position: {self.current_position}")
        percepts = self.generate_percepts(*self.current_position)
        self.append_output(f"Percepts: {percepts}")

    def generate_percepts(self, x, y):
        percepts = []
        if self.knowledge_base.has_wumpus(x, y):
            percepts.append("stench")
        if self.knowledge_base.has_gold(x, y):
            percepts.append("glimmer")
        if self.knowledge_base.has_pit(x, y):
            percepts.append("breeze")
        return percepts

    def append_output(self, message):
        self.output_text += message + "\n"
        self.visualization.update_output_text()

class Visualization:
    def __init__(self, knowledge_base, agent):
        self.knowledge_base = knowledge_base
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("Wumpus World")

        self.canvas_size = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.output_text = tk.Text(self.root, height=20, width=40, state="disabled")
        self.output_text.pack()

        self.image_wumpus = tk.PhotoImage(file="Wumpus.png")
        self.image_agent = tk.PhotoImage(file="Player.png")
        self.image_gold = tk.PhotoImage(file="Gold.png")
        self.image_pit = tk.PhotoImage(file="Pit.png")

        if self.agent:
            self.agent.visualization = self
            self.create_buttons()

        # Add a restart button
        restart_button = tk.Button(self.button_frame, text="Restart", command=self.restart_game)
        restart_button.pack(side=tk.LEFT, padx=5, pady=5)
        restart_button.configure(bg="lightgray")

    def create_buttons(self):
        directions = ["up", "down", "left", "right"]
        for direction in directions:
            button = tk.Button(self.button_frame, text=direction, command=lambda d=direction: self.handle_button_click(d))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.set_button_color(button, direction)

        grab_button = tk.Button(self.button_frame, text="Grab", command=self.agent.grab)
        grab_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.set_button_color(grab_button, "grab")

        climb_button = tk.Button(self.button_frame, text="Climb", command=self.agent.end_game)
        climb_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.set_button_color(climb_button, "climb")

    def set_button_color(self, button, direction):
        if direction == "up":
            button.configure(bg="lightblue")
        elif direction == "down":
            button.configure(bg="lightgreen")
        elif direction == "left":
            button.configure(bg="lightcoral")
        elif direction == "right":
            button.configure(bg="lightsalmon")
        elif direction == "grab":
            button.configure(bg="lightgoldenrodyellow")
        elif direction == "climb":
            button.configure(bg="lightpink")

    def handle_button_click(self, direction):
        self.agent.move(direction)
        self.update()

    def update(self):
        self.visualize()
        self.update_output_text()

    def visualize(self):
        self.canvas.delete("all")
        size = self.knowledge_base.size

        for y in range(size, 0, -1):
            for x in range(1, size + 1):
                position = f"({x}, {y})"
                if self.knowledge_base.has_wumpus(x, y):
                    self.draw_item(x, y, self.image_wumpus)
                elif self.knowledge_base.has_gold(x, y):
                    self.draw_item(x, y, self.image_gold)
                elif self.knowledge_base.has_pit(x, y):
                    self.draw_item(x, y, self.image_pit)
                elif (x, y) == self.agent.current_position:
                    self.draw_item(x, y, self.image_agent)
                else:
                    self.draw_item(x, y, ".")

    def draw_item(self, x, y, item):
        cell_size = self.canvas_size / self.knowledge_base.size
        x1, y1 = (x - 1) * cell_size, (self.knowledge_base.size - y) * cell_size
        x2, y2 = x * cell_size, (self.knowledge_base.size - y + 1) * cell_size

        if isinstance(item, tk.PhotoImage):
            self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, anchor=tk.CENTER, image=item)
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=item)

    def update_output_text(self):
        self.output_text.configure(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, self.agent.output_text)
        self.output_text.configure(state="disabled")

    def show_message(self, text):
        messagebox.showinfo("Game Over", text)

    def restart_game(self):
        self.knowledge_base.initialize()
        self.agent.current_position = (1, 1)
        self.agent.score = 0
        self.agent.move_left = self.agent.max_moves
        self.agent.output_text = ""
        self.update()
        messagebox.showinfo("Game Restarted", "The game has been restarted.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    size = 4

    knowledge_base = KnowledgeBase(size)
    knowledge_base.initialize()

    inference_engine = InferenceEngine(knowledge_base)
    visualization = Visualization(knowledge_base, None)

    agent = Agent(knowledge_base, inference_engine, visualization)
    visualization.agent = agent

    agent.current_position = (1, 1)

    visualization.create_buttons()
    visualization.update()
    visualization.run()
