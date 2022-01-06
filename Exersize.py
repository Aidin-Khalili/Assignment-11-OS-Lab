import arcade
import random
import enum
import math

#My constant value
SCREEN_TITLE = "Snake"
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
SCREEN_HEADER = 50
SNAKE_LENGTH = 1
SNAKE_SEGMENT_RADIUS = 10
SNAKE_SPEED = 1 / 10

class move_Direct(enum.Enum):#Again it's as an std but we change
    Up = 1
    Down = 2
    Left = 3
    Right = 4

class Snake():
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__score = 0
        self.__numMoves = 0
        self.__body = self.GenerateBody()
        self.__food = None
        self.__food_x = 0
        self.__food_y = 0
        self.__badfood = None
        self.__move_Direct = move_Direct.Right
        self.__dead = False
        self.food_Spawning()
        arcade.schedule(self.update_value, SNAKE_SPEED)
        arcade.schedule(self.Poop_Spawning, random.random() * 2)
        
    def get_Score(self):
        return self.__score

    def get_Nums_Of_Moves(self):
        return self.__numMoves

    def get_Body_Coordinate(self):
        return self.__body

    def get_Poop(self):
        return self.__badfood

    def get_Useful_Food(self):
        return self.__food

    def is_Die(self):
        return self.__dead

    def GenerateBody(self):
        body = []
        while len(body) < SNAKE_LENGTH:
            x = int(self.__width / 2 - len(body))
            y = int(self.__height / 2)
            coor = [x, y]
            body.append(coor)
        return body

    def food_Spawning(self):
        x, y = self.GetRandomCoor()
        self.__food_x = x
        self.__food_y = y
        self.__food = [x, y]
        arcade.unschedule(self.food_Spawning)

    def detecting_Colision_To_Body(self, body):
        head = body[0]
        dead = False
        if head in body[1:]:
            dead = True
        return dead

    def get_Mines_Score(self):
        dead = False
        if self.__score < 0:
            dead = True
        return dead
        
    def Poop_Spawning(self, _):
        x,y = self.GetRandomCoor()
        self.__badfood = [x,y]
        arcade.unschedule(self.Poop_Spawning)
        
    def GetRandomCoor(self):
        x = random.randint(0, self.__width)
        y = random.randint(0, self.__height)
        if [x, y] in self.__body and self.calculate_Dis_Between_2_Points(self.__body[0], [x, y]) > 5:
            x, y = self.GetRandomCoor()
        return x, y
        
    def calculate_Dis_Between_2_Points(self, point1, point2):
        x_dist = abs(point1[0] - point2[0])
        y_dist = abs(point2[1] - point2[1])
        x_dist_pow = math.pow(x_dist, 2)
        y_dist_pow = math.pow(y_dist, 2)
        dist = math.sqrt(x_dist_pow + y_dist_pow)
        return int(dist)
        
    def is_Eating_Food(self, body):
        head = body[0]
        eaten = False
        if self.__food == head:
            self.__score += 2
            self.__food = None
            eaten = True
            arcade.schedule(self.food_Spawning, random.random() * 2)
        if eaten == True:
            self.food_Spawning()
        return eaten

    def is_Eating_Bad_Food(self, body):
        head = body[0]
        bad_eaten = False
        if self.__badfood == head:
            self.__score -= 1
            self.__badfood = None
            bad_eaten = True
            arcade.schedule(self.Poop_Spawning, random.random() * 2)
        return bad_eaten

    def moving_Ai(self):
        if self.__body[0][0] != self.__food_x and self.__body[0][1] != self.__food_y:
            if self.__body[0][0] > self.__food_x:
                self.__move_Direct = move_Direct.Left
            elif self.__body[0][0] < self.__food_x:
                self.__move_Direct = move_Direct.Right
            elif self.__body[0][1] > self.__food_y:
                self.__move_Direct = move_Direct.Down
            elif self.__body[0][1] < self.__food_y:
                self.__move_Direct = move_Direct.Up
        elif   self.__body[0][0] != self.__food_x:
            if self.__body[0][0] > self.__food_x:
                self.__move_Direct = move_Direct.Left
            elif self.__body[0][0] < self.__food_x:
                self.__move_Direct = move_Direct.Right
        elif self.__body[0][1] != self.__food_y:
            if self.__body[0][1] > self.__food_y:
                self.__move_Direct = move_Direct.Down
            elif self.__body[0][1] < self.__food_y:
                self.__move_Direct = move_Direct.Up

    def snake_Moving(self,):
            new_body = []
            x = 0
            y = 0
            self.moving_Ai()
            if self.__move_Direct == move_Direct.Right or self.__move_Direct == move_Direct.Left:
                if self.__move_Direct == move_Direct.Right:
                    x = 1
                else:
                    x = -1
            elif self.__move_Direct == move_Direct.Up or self.__move_Direct == move_Direct.Down:
                if self.__move_Direct == move_Direct.Up:
                    y = 1
                else:
                    y = -1
            head = self.__body[0]
            new_head = [head[0] + x, head[1] + y]
            new_body.append(new_head)
            for i, _ in enumerate(self.__body):
                    if not i == 0:
                        new_body.append(self.__body[i - 1])
            self.__numMoves += 1
            collision_On_Edge = False
            if new_head[0] < 0 or new_head[0] > self.__width:
                     collision_On_Edge = True
            if new_head[1] < 0 or new_head[1] > self.__height:
                    collision_On_Edge = True
            return new_body, collision_On_Edge

    def update_value(self, _):
        if not self.__dead:
            new_body, self.__dead = self.snake_Moving()
            if not self.__dead:
                self.__dead = self.detecting_Colision_To_Body(new_body)
            if not self.__dead:
                self.__dead = self.get_Mines_Score()
            if not self.__dead:
                new_segment = self.is_Eating_Food(new_body)
                if new_segment:
                    new_body.append(self.__body[-1])
            if not self.__dead:
                self.is_Eating_Bad_Food(new_body)
            if not self.__dead:
                self.__body = new_body

class Game_UI(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT + SCREEN_HEADER, SCREEN_TITLE)
        arcade.set_background_color( arcade.color.SMOKY_BLACK )
        GridWidth, GridHeight = self.Calculate_Grid()
        self.snake = Snake(GridWidth, GridHeight)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_line( 0, SCREEN_HEIGHT + 1, SCREEN_WIDTH, SCREEN_HEIGHT + 1, arcade.color.DUTCH_WHITE, 2)
        try:
            score = self.snake.get_Score()
            arcade.draw_text("Score is : " + str(score), 10, SCREEN_HEIGHT + SCREEN_HEADER / 4, arcade.color.WHITE_SMOKE, 24)
        except:
            score = "..."
            arcade.draw_text("Score is : " + str(score), 10, SCREEN_HEIGHT + SCREEN_HEADER/4, arcade.color.WHITE_SMOKE, 24)
        try:
            dead = self.snake.is_Die()
            score = self.snake.get_Score()
            score > 0
        except:
            dead = False
        if dead:
            arcade.draw_text("Game over!", 0, SCREEN_HEIGHT / 2, arcade.color.WHITE_SMOKE, 60, width = SCREEN_WIDTH, align = "center")
        elif score < 0:
            arcade.draw_text("You got mines score!", 0, SCREEN_HEIGHT / 2, arcade.color.WHITE_SMOKE, 60, width = SCREEN_WIDTH, align = "center")
        self.drawing_Food()
        self.drawing_Body()
        self.drawing_Poop()

    def Calculate_Grid(self):
        width = ( SCREEN_WIDTH / SNAKE_SEGMENT_RADIUS ) - 1
        height = ( SCREEN_HEIGHT / SNAKE_SEGMENT_RADIUS ) - 1
        return width, height

    def drawing_Body(self):
        try:
            body = self.snake.get_Body_Coordinate()
        except:
            body = [[0,0]]
        for i, coor in enumerate( body ):
            color = arcade.color.DARK_PASTEL_GREEN
            if i == 0:
                color = arcade.color.GRANNY_SMITH_APPLE
            arcade.draw_circle_filled(coor[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, coor[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, SNAKE_SEGMENT_RADIUS / 2, color)

    def drawing_Food(self):
        try:
            food = self.snake.get_Useful_Food()
        except:
            food = None
        if not food == None:
            arcade.draw_circle_filled(food[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, food[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, SNAKE_SEGMENT_RADIUS / 2, arcade.color.RED)

    def drawing_Poop(self):
        try:
            badfood = self.snake.get_Poop()
        except:
            badfood = None
        if not badfood == None:
            arcade.draw_circle_filled(badfood[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, badfood[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2, SNAKE_SEGMENT_RADIUS / 2, arcade.color.DARK_BROWN)

my_game = Game_UI()
arcade.run()