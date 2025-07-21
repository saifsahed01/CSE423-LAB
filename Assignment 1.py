##Assignment 1
#Task 1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width, height = 500, 500           #[window size]
sky_t = 0.0
num_raindrops = 150
rain_drops = [[random.randint(0, width), random.randint(0, height)] for _ in range(num_raindrops)]
rain_direction = 0          # Default to no rain tilt
rain_speed = 1  

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)    #background color (sky blue)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, width, 0, height)  # projection for 2D

def lerp(a, b, t):
    return a + (b - a) * t

def interpolate_color(day_color, night_color, t):
    return (
        lerp(day_color[0], night_color[0], t),
        lerp(day_color[1], night_color[1], t),
        lerp(day_color[2], night_color[2], t),
    )

def update_rain():
    global rain_direction, rain_speed
    for i in range(len(rain_drops)):
        x, y = rain_drops[i]
        y -= rain_speed 
        x += rain_direction * 1.5  
        
        if y < 0:
            y = height
            x = random.randint(0, width)  

        rain_drops[i] = [x, y]

def draw_raindrop(x, y):
    glVertex2f(x, y)

def draw_rain():
    glColor3f(0, 0, 1)  # Set rain color to blue
    glBegin(GL_POINTS)
    for x, y in rain_drops:
        draw_raindrop(x, y)  # Draw each raindrop as a point
    glEnd()
    
def reset_rain():
    update_rain()
    draw_rain()
    

def draw_rectangle(x1, y1, x2, y2, color):
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_triangle(x1, y1, x2, y2, x3, y3, color):
    glColor3fv(color)
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def draw_point(x, y, size, color):
    glColor3fv(color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def display():
    global sky_t
    sky_t = max(0.0, min(1.0, sky_t))
    sky_color = interpolate_color((0.5, 0.8, 1.0), (0.05, 0.05, 0.2), sky_t)
    glClearColor(*sky_color, 1.0)  
    glClear(GL_COLOR_BUFFER_BIT)  

    draw_rectangle(0, 0, width, height /6, (0.1, 0.1, 0.1))     # Ground Border
    draw_rectangle(0, 0, width+2, height /6, (0.2, 0.8, 0.2))     # Ground
    draw_rectangle(98, (height / 6), 402, height / 2, (0.1, 0.1, 0.1))  # Building Border
    draw_rectangle(100, (height / 6)+2, 400, (height / 2)-2, (0.8, 0.5, 0.2))  # Building
    draw_triangle(50, (height / 2)-1, 250, (height / 1.4), 450, (height / 2)-1, (0.1, 0.1, 0.1))  # Roof Border
    draw_triangle(58, (height / 2)+1, 250, (height / 1.4)-2, 442, (height / 2)+1, (0.8, 0.3, 0.1))  # Roof
    draw_rectangle(220, (height / 6), 270, (height / 3), (0.1, 0.1, 0.1)) # Door Border
    draw_rectangle(222, (height / 6)+2, 268, (height / 3)-2, (0.9, 0.9, 0.9))  # Door  
    draw_point(235, height/ 6 + 40, 6, (0.1, 0.1, 0.1))  # Doorknob
    draw_point(255, height/ 6 + 40, 6, (0.1, 0.1, 0.1))  # Doorknob
    draw_rectangle(243, height / 6, 247, height / 3, (0.1, 0.1, 0.1))  # Door Middle
    draw_rectangle(130, (height / 6)+60, 170, (height / 6)+96, (0.1, 0.1, 0.1))  # Left Window Border
    draw_rectangle(132, (height / 6)+62, 168, (height / 6)+94, (0.9, 0.9, 0.9))  # Left Window
    draw_rectangle(330, (height / 6)+60, 370, (height / 6)+96, (0.1, 0.1, 0.1))  # Right Window Border
    draw_rectangle(332, (height / 6)+62, 368, (height / 6)+94, (0.9, 0.9, 0.9))  # Right Window

    draw_rain() 
    
    glutSwapBuffers()  

def keyboard(key, x, y):
    global sky_t, rain_direction, rain_speed
    if key == b'w':  
        sky_t = 1.0 - sky_t
        if sky_t == 1.0:
            print("It's Night!!")
        else:
            print("It's Day!!")
    elif key == b'r':
        reset_rain()  
        rain_direction = 0
        rain_speed = 5 
        sky_t = 0.0
        print("All Reset!!")

def mouse(button, state, x, y):
    global rain_direction
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rain_direction = -1  
        print("Rain direction set Right to Left")
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        rain_direction = 1  
        print("Rain direction set Left to Right")
    elif button == GLUT_MIDDLE_BUTTON and state == GLUT_DOWN:
        rain_direction = 0  
        print("Rain Direction set to Middle")
    update_rain()  

def special_keys(key, x, y):
    global rain_speed
    if key == GLUT_KEY_UP: 
        rain_speed += 1 
        print("Rain speed increased to:", rain_speed)
    if key == GLUT_KEY_DOWN: 
        rain_speed = max(1, rain_speed - 1)
        print("Rain speed decreased to:", rain_speed)


def idle():
    update_rain()  
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)  
    glutInitWindowSize(width, height)  
    glutInitWindowPosition(100, 100)  
    glutCreateWindow(b"Task 1 - House in a Rainy Day")  
    init()  

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse) 
    glutSpecialFunc(special_keys)  
    glutIdleFunc(idle)  

    glutMainLoop()

main()









#Task 2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

width, height = 500, 500
points = []
point_speed = 1
frozen = False
point_size = 5

is_blinking = False   
blink_state = False      
last_blink_time = 0

class Point: 
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.base_color = (random.random(), random.random(), random.random())
        self.color = self.base_color

    def update(self):
        if not frozen:
            self.x += self.dx * point_speed
            self.y += self.dy * point_speed
            if self.x <= 0 or self.x >= width:
                self.dx = -self.dx
            if self.y <= 0 or self.y >= height:
                self.dy = -self.dy

    def draw(self):
        glColor3fv(self.color)
        glVertex2f(self.x, self.y)

    def update_blink(self, blinking, blink_state):
        if blinking:
            if blink_state:
                self.color = (0.0, 0.0, 0.0) 
            else:
                self.color = self.base_color
        else:
            self.color = self.base_color

def generate_point(x, y):
    direction = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])
    point = Point(x, y, direction[0], direction[1])
    points.append(point)

def reset_points():
    global points, point_size, point_speed
    point_size = 5
    point_speed = 1
    points = []

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(point_size)
    glBegin(GL_POINTS)
    for point in points:
        point.update()
        point.update_blink(is_blinking, blink_state)
        point.draw()
    glEnd()
    glutSwapBuffers()

def keyboard(key, x, y):
    global point_size, frozen
    if key == b' ':
        frozen = not frozen
    if not frozen:
        if key == b'\x1b':
            glutLeaveMainLoop()
        elif key == b'w':
            point_size += 1
            print(f"Point size increased to {point_size}")
        elif key == b's':
            point_size = max(1, point_size - 1)
            if point_size == 1:
                print("Point size cannot be decreased further")
            else:
                print(f"Point size decreased to {point_size}")
            
        elif key == b'r':
            reset_points()
            print("Points reset")

def special_keys(key, x, y):
    global point_speed, frozen
    if not frozen:
        if key == GLUT_KEY_UP:
            point_speed += 1
            print(f"Point speed increased to {point_speed}")
        elif key == GLUT_KEY_DOWN:
            point_speed = max(1, point_speed - 1)
            print(f"Point speed decreased to {point_speed}")
def mouse(button, state, x, y):
    global is_blinking
    if not frozen:
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            generate_point(x, height - y)
            print(f"Point generated at ({x}, {height - y})")
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            is_blinking = not is_blinking
            print(f"Blinking {'started' if is_blinking else 'stopped'}")

def idle():
    global blink_state, last_blink_time, frozen
    if is_blinking:
        current_time = time.time()
        if current_time - last_blink_time > 0.5:
            blink_state = not blink_state
            last_blink_time = current_time
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Task-2 : Amazing Box!!")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, width, 0, height)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutSpecialFunc(special_keys)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
