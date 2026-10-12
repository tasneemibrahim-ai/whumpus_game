import random

class WumpusWorld:
    
    #KB
    def intialize(self, grid_size = 4, num_pits = 3, num_gold = 5):
        self.grid_size = grid_size
        self.pit_positions = [(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(num_pits)]
        self.wumpus_position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        self.gold_position = [(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(num_gold)]
        self.world = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.agent_position = (0, 0)
        self.arrows = 1
        self.is_wumpus_alive = True
        self.wumpus.has_screamed = False
        self.has_gold = False
        self.game_over = False
        self.current_score = 1000

    
    #inference engine
    def infer(self, percept):
        if 'breeze' in percept:              
            self.infer_pit()

        if 'stench' in percept:             
            self.infer_wumpus()
        if 'gliter' in percept :
            self.infer_gold()   

    #Precept
    def percepts(self):
        percept_list = []
    
        if self.is_stench(self.agent_position):
            percept_list.append('stench')
    
        if self.is_breeze(self.agent_position):
            percept_list.append('breeze')

        if self.is_gliter(self.agent_position):
            percept_list.append('gliter')      

        if self.is_scream():
            percept_list.append('scream')   

        return percept_list

    def is_breeze(self, position):
        for pit_position in self.pit_positions:
            if (
                (position[0] == pit_position[0] and abs(position[1] - pit_position[1]) == 1) or
                (position[1] == pit_position[1] and abs(position[0] - pit_position[0]) == 1)
            ):
                return True
        return False

    def is_stench(self, position):
        return (
            (position[0] == self.wumpus_position[0] and abs(position[1] - self.wumpus_position[1]) == 1) or
            (position[1] == self.wumpus_position[1] and abs(position[0] - self.wumpus_position[0]) == 1)
        )
    
    def is_gliter(self, position):
        return self.has_gold   

    #inference engine
    def infer_pit(self):
        if self.is_breeze(self.agent_position):
            print("There is a breeze. Possible pit nearby.")
        else:
            print("No breeze. Likely no pit nearby.") 

    #inference engine
    def infer_wumpus(self):
        if self.is_stench(self.agent_position):
            print("There is a stench. Wumpus might be nearby.")
        else:
            print("No stench. Likely no Wumpus nearby.")

            
    #inference engine
    def infer_gold(self):
        if self.is_gold(self.agent_position):
            print("There is a gliter. you caught the gold.")
        else:
            print("No gliter. search for the gold.")         

    #Agent Function
    def agent_action(self):
        while True:
            self.print_grid()

            action = input("Enter your action (left, right, up, down, grab, release, shoot, quit): ").lower()

            if action == 'quit':
                print("Quitting the game.")
                break
            elif action == 'grab':
                self.grab()
                self.check_state()

            elif action == 'release':
                self.release()
                self.check_state()

            elif action == 'shoot':
                self.is_shoot()
                self.check_state() 

            elif action in ['left', 'right', 'up', 'down']:
                self.move(action)
            
            else:
                print("Invalid action. Please enter a valid action.")

    def grab(self):
        if self.agent_position == self.gold_position and self.has_gold == False :
            self.has_gold = True
            print("You grabbed the gold!")

    def release(self):
        if self.agent_position == (0, 0) and self.has_gold:
            self.has_gold = False
            print("You released the gold!")
            print("congratulations! you won the game")
            

#for new_position in self.world and self.has_gold == True
                        
    def move_agent(self, new_position):
        self.agent_position = new_position
        if self.world [new_position[0]][new_position[1]] == 'G':
            self.has_gold = True
            self.release(new_position)

    def is_shoot(self):
        if self.arrows > 0:
            self.arrows -= 1
            wumpus_x, wumpus_y = self.wumpus_position

            if self.agent_position[0] == wumpus_x and abs(self.agent_position[1] - wumpus_y) == 1:
                self.wumpus.has_screamed = True
                self.is_wumpus_alive = False
                return (True)
                print("You shot the Wumpus!")
            elif self.agent_position[1] == wumpus_y and abs(self.agent_position[0] - wumpus_x) == 1:
                self.wumpus.has_screamed = True
                self.is_wumpus_alive = False
                return (True)
                print("You shot the Wumpus!")
            else:
                self.wumpus.has_screamed = False
                self.is_wumpus_alive = True
                return(False)
                print("Missed the Wumpus!")
                
    def move(self, direction):
        x, y = self.agent_position

        if direction == 'left' and x > 0:
            x -= 1
        elif direction == 'right' and x < self.grid_size - 1:
            x += 1
        elif direction == 'up' and y > 0:
            y += 1
        elif direction == 'down' and y < self.grid_size - 1:
            y -= 1
        self.agent_position = (x, y)


    def check_state(self):
        if self.agent_position in self.pit_positions:
            print("Game over! You fell into a pit.")
            self.game_over = True
        elif self.agent_position == self.wumpus_position and self.is_wumpus_alive:
            print("Game over! You were caught by the Wumpus.")
            self.game_over = True
        elif self.current_score == 0 or self.current_score < 0 :
             print("Game over! you lost your score")     
        elif self.agent_position == (0, 0) and self.has_gold:
            self.has_gold = False
            print("Congratulations! You won!")
            self.game_over = False

    def print_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):

                if (i, j) == self.agent_position:
                    print('A', end = ' ')

                elif (i, j) == self.gold_position:
                    print('G', end=' ')

                elif (i, j) == self.wumpus_position and self.is_wumpus_alive:
                    print('W', end=' ')

                elif (i, j) in self.pit_positions:
                    print('P', end=' ')

                else:
                    print('-', end=' ')
            print()
    
    
    #score
    def score_update(knowledge_base, action):
        if action == 'move':
            knowledge_base['current_score'] -= 1
        elif action == 'shoot' and is_shoot == False :
            knowledge_base['current_score'] -= 1
        elif action == 'grab':
            knowledge_base['current_score'] += 10
        elif action == 'shoot' and is_shoot :  
            knowledge_base['current_score'] += 1
        
        def is_shoot(self):
            if self.arrows > 0:
                self.arrows -= 1
                wumpus_x, wumpus_y = self.wumpus_position

                if self.agent_position[0] == wumpus_x and abs(self.agent_position[1] - wumpus_y) == 1:
                    self.wumpus.has_screamed = True
                    self.is_wumpus_alive = False
                    return (True)
                    print("You shot the Wumpus!")
                elif self.agent_position[1] == wumpus_y and abs(self.agent_position[0] - wumpus_x) == 1:
                    self.wumpus.has_screamed = True
                    self.is_wumpus_alive = False
                    return (True)
                    print("You shot the Wumpus!")
                else:
                    self.wumpus.has_screamed = False
                    self.is_wumpus_alive = True
                    return(False)
                    print("Missed the Wumpus!")
    
    #visualization
    def visualize_game(knowledge_base):
        print("Current Score:", knowledge_base['current_score'])
        print("Agent Position:", knowledge_base['agent_position'])

