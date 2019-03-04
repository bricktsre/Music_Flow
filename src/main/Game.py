import random,sys,queue,pygame
from Enemy import Enemy  
from Player import Player
from MusicData import MusicData
from Definitions import Color,Direction

WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = Color.BLACK

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
myFont = pygame.font.SysFont("monospace", 35)
clock = pygame.time.Clock()

music_data_queue = queue.Queue(maxsize=0) 
cached_queue = queue.Queue(maxsize=0)

class Game:
    max_enemies = 12

    def __init__(self,filename):
        self.player = Player(WIDTH / 2, HEIGHT / 2, Color.RED)
        self.enemy_list = list()

        self.game_over = False

        self.score = 0
        self.old_time = 0
        self.song_file = filename
        self.temp_music_data = MusicData(0,(0,0,0),0)#,(0,0),(0,0))

    def add_enemies(self,enemy_list,md):
        md_tuple = md.data
        if len(enemy_list) < Game.max_enemies and md_tuple[0] != 0: 
            position_and_direction = self.get_position_and_direction(md_tuple[2])
            e = Enemy(md_tuple[0],md_tuple[1],md_tuple[2],position_and_direction[0],position_and_direction[1])
            enemy_list.append(e)

    def get_position_and_direction(self,size):
        return_array = [0,0]
        side  = random.randint(0,3)
        if side == 0:
            return_array[0] = (random.randint(0,WIDTH-size),HEIGHT-size)
            return_array[1] = (0,-1)
            #return_array[1] = (random.randint(-1,1),-1)
        elif side == 1:
            return_array[0] = (0,random.randint(0,HEIGHT-size))
            return_array[1] = (1,0)
            #return_array[1] = (1,random.randint(-1,1))
        elif side == 2:
            return_array[0]=  (random.randint(0,WIDTH-size),0)
            return_array[1] = (0,1)
            #return_array[1] = (random.randint(-1,1),1)
        else:
            return_array[0] = (WIDTH-size,random.randint(0,HEIGHT-size))
            return_array[1] = (-1,0)
            #return_array[1] = (-1,random.randint(-1,1))
        return return_array


    def draw_enemies(self,enemy_list):
        for enemy in enemy_list:
            pygame.draw.rect(screen, enemy.color, (enemy.x, enemy.y, enemy.size, enemy.size))


    def update_enemy_positions(self,enemy_list, score):
        for idx, enemy in enumerate(enemy_list):
            if enemy.y < 0 or enemy.y > HEIGHT or enemy.x < 0 or enemy.x > WIDTH:
                enemy_list.pop(idx)
                score += 1
            else:
                enemy.move()
        return score


    def collision_check(self,enemy_list, player):
        for enemy in enemy_list:
            if self.detect_collision(player, enemy):
                return True
        return False


    def detect_collision(self,player, enemy):
        p_x = player.x
        p_y = player.y

        e_x = enemy.x
        e_y = enemy.y

        if (e_x >= p_x and e_x < (p_x + player.SIZE)) or (p_x >= e_x and p_x < (e_x + enemy.size)):
            if (e_y >= p_y and e_y < (p_y + player.SIZE)) or (p_y >= e_y and p_y < (e_y + enemy.size)):
                return True
        return False

    def add_music_data(self,speed,color,size):#,position,direction):
        music_data_queue.put(MusicData(speed,color,size))#,position,direction))
        cached_queue.put(MusicData(speed,color,size))

    def key_presses(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_player(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                   self.move_player(Direction.RIGHT)
                elif event.key == pygame.K_UP:
                    self.move_player(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.move_player(Direction.DOWN)
            
    def move_player(self,direction):
        for i in range(25):
            self.player.move(direction)
            pygame.draw.rect(screen, self.player.color, (self.player.x, self.player.y, self.player.SIZE, self.player.SIZE))
            pygame.display.update()      

    def button(self,msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #print(click)
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action()         
        else:
            pygame.draw.rect(screen, ic,(x,y,w,h))

        smallText = pygame.font.SysFont("monospace",20)
        textSurf = smallText.render(msg, True, Color.WHITE)
        textRect = textSurf.get_rect()
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(textSurf, textRect)

    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            screen.fill(Color.BLACK)
            largeText = pygame.font.SysFont("monospace",115)
            TextSurf = largeText.render("Music Flow", True, Color.WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ((WIDTH/2),(HEIGHT/3))
            screen.blit(TextSurf, TextRect)

            self.button("Play Game",WIDTH/2 -75,(HEIGHT/3)*2,150,75,Color.OLIVE,Color.GREEN,self.game_loop)

            pygame.display.update()
            clock.tick(15)

    def game_end(self):
        self.player = Player(WIDTH / 2, HEIGHT / 2, Color.RED)
        self.enemy_list = list()

        self.game_over = False

        self.score = 0
        self.old_time = 0
        music_data_queue = cached_queue

        while True:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            screen.fill(Color.BLACK)
            largeText = pygame.font.SysFont("monospace",115)
            TextSurf = largeText.render("Game Over", True, Color.WHITE)
            TextRect = TextSurf.get_rect()
            TextRect.center = ((WIDTH/2),(HEIGHT/3))
            screen.blit(TextSurf, TextRect)

            self.button("Play Again",WIDTH/2 -75,(HEIGHT/3)*2,150,75,Color.OLIVE,Color.GREEN,self.game_loop)

            pygame.display.update()
            clock.tick(15)     

    def game_loop(self):
        pygame.mixer_music.load(self.song_file)
        pygame.mixer_music.play(loops=0, start=0.0)
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            time_diff = current_time - self.old_time
            if time_diff > 100:
                self.old_time = current_time
            
            if not music_data_queue.empty() and time_diff > 100:
                md = music_data_queue.get()   
            else:
                md = self.temp_music_data
                  

            self.key_presses()
            self.add_enemies(self.enemy_list,md)
            self.score = self.update_enemy_positions(self.enemy_list, self.score)

            screen.fill(BACKGROUND_COLOR)
            text = "Score:" + str(self.score)
            label = myFont.render(text, 1, Color.YELLOW)
            screen.blit(label, (WIDTH - 200, HEIGHT - 40))

            self.draw_enemies(self.enemy_list)
            pygame.draw.rect(screen, self.player.color, (self.player.x, self.player.y, self.player.SIZE, self.player.SIZE))
            
            if self.collision_check(self.enemy_list, self.player):
               self.game_over = True
               self.game_end()        
            
            # Less accurate, very little CPU Usage
            #clock.tick(40)
            # Very accurate, more CPU usage
            clock.tick_busy_loop(50)
            #print(clock.get_fps())

            pygame.display.update()