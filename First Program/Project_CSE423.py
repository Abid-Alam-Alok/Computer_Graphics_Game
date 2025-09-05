from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
# Camera-related variables
cheat_targeted_enemies = set()  # store enemies already shot in cheat mode
cheat_spin_speed = 1  # degrees per frame
bullets_x = []
bullets_y = []
bullets_z = []
bullets_direction_x = []
bullets_direction_y = []
bullets_angle = []
camera_pos = (0,500,500)
camera_offset = (0, 500, 500)  # Camera offset relative to player
player_x = 0
player_y = 0

# Sword-related variables
sword_swing_counter = 0  # Counter to slow down sword rotation
player_z = 0  # Player height for jumping
is_jumping = False  # Jump state
jump_velocity = 0  # Current jump velocity
jump_speed = 15  # Initial jump speed
gravity = 0.8  # Gravity force
enemy_list = []
player_cam_angle = 0
mouse_left = False  # Track left mouse button state
score = 0  # Add score tracking
missed = 0
enem_rad_bottom = 35
enem_growing_bottom = True
enem_rad_top = 20
enem_growing_top = True
enem_growing = True  # Flag for enemy size animation
player_hit_count = 0  # Track how many times enemy touched the player
count = 0
first_person = False
camera_mode = 0  # 0: top view, 1: third person, 2: first person
cheat_mode = False  # If true, enemies won't move towards player
val = 0
cam_spinner = False
static_first_person = False
player_lives = 5
game_over = False  # Game over state
current_weapon = "gun"  # Start with the gun
death_rotation = 0  # Player rotation on X-axis for falling animation
imp_val = 0
sword_rotation = 0
fovY = 120  # Field of view
GRID_LENGTH = 3000  # Length of grid lines (increased from 600)
rand_var = 423
angle_hacks = math.radians(3)
angle_inc = math.radians(5)
move_speed = 10  # Player movement speed

# Boss system variables
boss_health = 10  # Boss requires 10 bullets to kill
boss_alive = True
boss_x = -2500  # Boss position in cave
boss_y = -2500
boss_z = 0
boss_standing = False  # Boss stands up when player enters cave
boss_animation_timer = 0
lava_collision_count = 0  # Track lava collisions for health system

# (samania new): CODE FOR HEALTH, STAMINA, AND WEATHER                          
# Health and Stamina System
MAX_PLAYER_LIVES = 5
player_stamina = 100.0
MAX_STAMINA = 100.0
is_sprinting = False
STAMINA_DRAIN_RATE = 0.3
STAMINA_REGEN_RATE = 0.15
STAMINA_SPRINT_THRESHOLD = 15
STAMINA_COST_JUMP = 20.0

# Weather System
weather_particles = []
MAX_PARTICLES = 500
WEATHER_VOLUME_SIZE = 1500
# ======================

# Cloud variables
cloud_positions = []
cloud_animation_timer = 0

# Bat variables
bat_animation_timer = 0
bat_wing_angle = 0

# House and door system variables
door_open = False
door_timer = 0
door_auto_close_time = 180  # frames (3 seconds at 60fps)
house_x = -800  # House in bottom-left corner
house_y = -800
house_width = 350
house_depth = 350

# Neighbor house door variables
neighbor1_door_open = False
neighbor1_door_timer = 0
neighbor2_door_open = False
neighbor2_door_timer = 0
neighbor3_door_open = False
neighbor3_door_timer = 0

# Village neighbor houses variables
# Neighbor 1: Top-left corner with chickens
neighbor1_x = -800
neighbor1_y = 800
neighbor1_width = 400
neighbor1_depth = 400

# Neighbor 2: Top-right corner with cow and milk cans
neighbor2_x = 800
neighbor2_y = 800
neighbor2_width = 400
neighbor2_depth = 400

# Neighbor 3: Bottom-right corner with apple trees
neighbor3_x = 800
neighbor3_y = -800
neighbor3_width = 400
neighbor3_depth = 400

# Animation variables for village elements
chicken_bob_angle = 0  # For chicken bobbing animation

# Merchant NPCs variables
merchant1_x = neighbor1_x  # Merchant in neighbor house 1
merchant1_y = neighbor1_y
merchant1_angle = 0
merchant1_move_timer = 0
merchant1_direction = 1

merchant2_x = neighbor2_x  # Merchant in neighbor house 2
merchant2_y = neighbor2_y
merchant2_angle = 90
merchant2_move_timer = 60
merchant2_direction = 1

merchant3_x = neighbor3_x  # Merchant in neighbor house 3
merchant3_y = neighbor3_y
merchant3_angle = 180
merchant3_move_timer = 120
merchant3_direction = 1
cow_tail_angle = 0     # For cow tail swaying


# (SAMANIA): CODE FOR DAY/NIGHT CYCLE AND SEASONS

# Day-Night Cycle
time_of_day = 1.0  # 1.0 is midday, 0.0 is midnight
day_night_target = 1.0 # The time of day we are transitioning towards
day_night_transition_speed = 0.05 # How fast the transition happens
is_day = True # Tracks if it's currently day

# Seasonal Change
day_count = 0 # Counter for day-night alternations
days_per_season = 1 # How many "days" until the season changes
# Seasons: 0=Spring, 1=Summer, 2=Autumn, 3=Winter
current_season = 0
season_names = ["Spring", "Summer", "Autumn", "Winter"]

# Seasonal Color Palettes
# Grass colors [base_sand, patch1, patch2]
season_grass_colors = {
    0: [(0.8, 0.7, 0.4), (0.2, 0.8, 0.2), (0.3, 0.9, 0.3)], # Spring: Sandy with vibrant green
    1: [(0.8, 0.7, 0.4), (0.1, 0.6, 0.1), (0.2, 0.7, 0.2)], # Summer: Sandy with deep green
    2: [(0.8, 0.7, 0.4), (0.8, 0.5, 0.2), (0.9, 0.6, 0.1)], # Autumn: Sandy with orange/brown patches
    3: [(0.9, 0.9, 0.9), (0.8, 0.8, 0.8), (1.0, 1.0, 1.0)], # Winter: Light gray/white snow
}
# Tree leaf colors that match the 18 variations in your tree drawing code
season_leaf_colors = {
    0: [(0.0, 0.8, 0.2), (0.1, 0.7, 0.1), (0.0, 0.6, 0.3), (0.2, 0.9, 0.2), (0.0, 0.5, 0.2), (0.3, 0.8, 0.3), (0.0, 0.9, 0.4), (0.1, 0.9, 0.3), (0.0, 0.7, 0.4), (0.2, 0.6, 0.1), (0.0, 0.8, 0.5), (0.3, 0.9, 0.4), (0.1, 0.5, 0.3), (0.0, 0.9, 0.1), (0.2, 0.7, 0.2), (0.1, 0.6, 0.4), (0.0, 0.4, 0.2), (0.4, 0.8, 0.2)], # Spring
    1: [(0.0, 0.6, 0.1), (0.1, 0.5, 0.0), (0.0, 0.5, 0.1), (0.1, 0.6, 0.1), (0.0, 0.4, 0.0), (0.2, 0.6, 0.2), (0.0, 0.7, 0.2), (0.1, 0.7, 0.1), (0.0, 0.5, 0.2), (0.1, 0.4, 0.0), (0.0, 0.6, 0.3), (0.2, 0.7, 0.3), (0.1, 0.4, 0.2), (0.0, 0.7, 0.0), (0.1, 0.5, 0.1), (0.1, 0.5, 0.2), (0.0, 0.3, 0.1), (0.3, 0.6, 0.1)], # Summer
    2: [(1.0, 0.5, 0.0), (0.8, 0.2, 0.1), (0.9, 0.6, 0.1), (0.7, 0.3, 0.0), (1.0, 0.4, 0.0), (0.8, 0.4, 0.1), (0.9, 0.3, 0.0), (1.0, 0.6, 0.2), (0.7, 0.2, 0.0), (0.9, 0.5, 0.2), (1.0, 0.3, 0.1), (0.8, 0.5, 0.0), (0.9, 0.4, 0.1), (1.0, 0.2, 0.0), (0.7, 0.4, 0.2), (0.8, 0.3, 0.1), (0.9, 0.2, 0.0), (1.0, 0.7, 0.1)], # Autumn
    3: [], # Winter: No leaves
}
# Sky colors [day_color, night_color]
sky_colors = [(0.53, 0.81, 0.92), (0.0, 0.0, 0.1)] # Day color matches your original glClearColor

def update_day_night_cycle():
    """Gradually transitions the time of day and handles season changes."""
    global time_of_day, day_night_target, day_count, current_season, is_day

    # Gradually move current time towards the target time
    if time_of_day < day_night_target:
        time_of_day = min(day_night_target, time_of_day + day_night_transition_speed)
    elif time_of_day > day_night_target:
        time_of_day = max(day_night_target, time_of_day - day_night_transition_speed)

    # Check for a completed transition to day
    if time_of_day == 1.0 and not is_day:
        is_day = True
        day_count += 1
        print(f"A new day has begun. Day {day_count} of {days_per_season} in this season.")
        # Check if it's time to change the season
        if day_count >= days_per_season:
            day_count = 0
            current_season = (current_season + 1) % 4 # Cycle through 4 seasons
            print(f"The season has changed to {season_names[current_season]}!")

    # Check for a completed transition to night
    elif time_of_day == 0.0 and is_day:
        is_day = False
        print("Night has fallen.")

# ======================================


# (samnia new): FUNCTIONS FOR HEALTH, STAMINA, AND WEATHER  

def initialize_weather():
    """Creates the initial set of weather particles."""
    global weather_particles
    weather_particles = []
    for _ in range(MAX_PARTICLES):
        x = player_x + random.uniform(-WEATHER_VOLUME_SIZE, WEATHER_VOLUME_SIZE)
        y = player_y + random.uniform(-WEATHER_VOLUME_SIZE, WEATHER_VOLUME_SIZE)
        z = random.uniform(50, 800) # Start at various heights
        weather_particles.append([x, y, z])

def update_stamina():
    """Updates the player's stamina - regenerates when idle."""
    global player_stamina, move_speed, is_sprinting

    # Check if the player is trying to sprint (by holding the sprint key, which is 'q')
    if is_sprinting and move_speed > 10:
        if player_stamina <= 0:
            # If stamina runs out, force player to normal speed
            move_speed = 10
    else:
        # If not sprinting, regenerate stamina
        if player_stamina < MAX_STAMINA:
            player_stamina += STAMINA_REGEN_RATE
            player_stamina = min(MAX_STAMINA, player_stamina)

def update_weather():
    """Updates the position of rain/snow particles."""
    global weather_particles

    # Determine fall speed based on season
    fall_speed = 10 if current_season == 3 else 20 # Snow falls slower

    for i in range(len(weather_particles)):
        # Move particle down
        weather_particles[i][2] -= fall_speed

        # If particle hits the ground or goes out of the volume, reset it
        particle_x, particle_y, particle_z = weather_particles[i]

        # Check if particle is outside the volume around the player or below ground
        is_out_of_bounds = (particle_x < player_x - WEATHER_VOLUME_SIZE or
                            particle_x > player_x + WEATHER_VOLUME_SIZE or
                            particle_y < player_y - WEATHER_VOLUME_SIZE or
                            particle_y > player_y + WEATHER_VOLUME_SIZE)

        if particle_z < 0 or is_out_of_bounds:
            # Reset particle to a new random position at the top of the volume
            new_x = player_x + random.uniform(-WEATHER_VOLUME_SIZE, WEATHER_VOLUME_SIZE)
            new_y = player_y + random.uniform(-WEATHER_VOLUME_SIZE, WEATHER_VOLUME_SIZE)
            new_z = random.uniform(700, 900)
            weather_particles[i] = [new_x, new_y, new_z]

def draw_hud():
    """Draws the 2D Heads-Up Display (Health, Stamina, Game Over)."""
    # Switch to 2D Orthographic view
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800) # Match window size

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable depth testing for 2D overlay
    glDisable(GL_DEPTH_TEST)

    # --- Health Bar ---
    health_percentage = player_lives / MAX_PLAYER_LIVES
    bar_width = 300
    bar_height = 25

    # Background
    glColor3f(0.2, 0.2, 0.2) # Dark gray background
    glBegin(GL_QUADS)
    glVertex2f(20, 750)
    glVertex2f(20 + bar_width, 750)
    glVertex2f(20 + bar_width, 750 + bar_height)
    glVertex2f(20, 750 + bar_height)
    glEnd()

    # Foreground (actual health)
    glColor3f(1.0, 0.1, 0.1) # Red color for health
    glBegin(GL_QUADS)
    glVertex2f(20, 750)
    glVertex2f(20 + (bar_width * health_percentage), 750)
    glVertex2f(20 + (bar_width * health_percentage), 750 + bar_height)
    glVertex2f(20, 750 + bar_height)
    glEnd()
   

    # (samania new)) Health Bar Label                              
    glColor3f(1.0, 1.0, 1.0) # White text
    glRasterPos2f(30, 755) # Position text inside the bar
    health_text = "Health"
    for char in health_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # --- Stamina Bar ---
    stamina_percentage = player_stamina / MAX_STAMINA

    # Background
    glColor3f(0.2, 0.2, 0.2) # Dark gray background
    glBegin(GL_QUADS)
    glVertex2f(20, 715)
    glVertex2f(20 + bar_width, 715)
    glVertex2f(20 + bar_width, 715 + bar_height)
    glVertex2f(20, 715 + bar_height)
    glEnd()

    # Foreground (actual stamina)
    glColor3f(0.2, 0.6, 1.0) # Blue color for stamina
    glBegin(GL_QUADS)
    glVertex2f(20, 715)
    glVertex2f(20 + (bar_width * stamina_percentage), 715)
    glVertex2f(20 + (bar_width * stamina_percentage), 715 + bar_height)
    glVertex2f(20, 715 + bar_height)
    glEnd()
   
 
    # (samania new) Stamina Bar Label      
    #        
    glColor3f(1.0, 1.0, 1.0) # White text
    glRasterPos2f(30, 720) # Position text inside the bar
    stamina_text = "Stamina"
    for char in stamina_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # --- Score Display ---
    glColor3f(1.0, 1.0, 1.0) # White text
    glRasterPos2f(30, 680) # Position below stamina bar
    score_text = f"Score: {score}"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # --- Lives Display ---
    glColor3f(1.0, 1.0, 1.0) # White text
    glRasterPos2f(30, 650) # Position below score
    lives_text = f"Lives: {player_lives}"
    for char in lives_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # --- Game Over Text ---
    if game_over:
        glColor3f(1.0, 0.0, 0.0) # Red
        # Position the text in the center of the screen
        text_to_draw = "GAME OVER"
        x_pos = 420
        y_pos = 400

        glRasterPos2f(x_pos, y_pos)
        for char in text_to_draw:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    # Restore settings
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def draw_weather():
    """Draws rain or snow based on the current season."""
    # We don't draw weather in Spring
    if current_season == 0:
        return

    # Set color and shape based on season
    if current_season == 3: # Winter
        glColor3f(1.0, 1.0, 1.0) # White for snow
        glPointSize(3)
        glBegin(GL_POINTS)
    else: # Summer or Autumn
        glColor3f(0.7, 0.8, 0.9) # Light blue for rain
        glLineWidth(1.5)
        glBegin(GL_LINES)

    for p in weather_particles:
        if current_season == 3: # Draw point for snow
            glVertex3f(p[0], p[1], p[2])
        else: # Draw line for rain
            glVertex3f(p[0], p[1], p[2])
            glVertex3f(p[0], p[1], p[2] - 15) # A short line for the raindrop

    glEnd()



def check_game_over():
    """Check if game over conditions are met and handle game over state"""
    global player_lives, missed, player_hit_count, game_over, enemy_list

    if player_hit_count >= 1:
        player_lives -= 1
        player_hit_count = 0  # Reset hit count
        print(f"Life lost due to enemy contact! Lives remaining: {player_lives}")

    # Clamp player_lives to 0
    if player_lives < 0:
        player_lives = 0

    # Check for game over
    if player_lives <= 0 and not game_over:
        game_over = True
        enemy_list.clear()  # Remove all enemies
        print("GAME OVER!")


def update_player_death_animation():
    global death_rotation

    if game_over and death_rotation < 90:
        death_rotation += 90


def update_player_jump():
    """Update player jumping physics with gravity"""
    global player_z, is_jumping, jump_velocity, gravity

    if is_jumping:
        # Update player height based on velocity
        player_z += jump_velocity

        # Apply gravity to velocity
        jump_velocity -= gravity

        # Check if player has landed
        if player_z <= 0:
            player_z = 0
            is_jumping = False
            jump_velocity = 0


def collision_detector(x1, y1, radius1, x2, y2, radius2):
    dx = x2 - x1
    dy = y2 - y1

    dx_sq = dx **2
    dy_sq = dy **2

    sum = dx_sq + dy_sq

    distance = math.sqrt(sum)

    sum_rads = radius1 + radius2

    if distance < sum_rads:
        collision = True
    else:
        collision = False

    return collision


def collision_detector_3d(x1, y1, z1, radius1, x2, y2, z2, radius2):
   
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    distance_sq = dx**2 + dy**2 + dz**2
    distance = math.sqrt(distance_sq)

    sum_rads = radius1 + radius2

    if distance < sum_rads:
        return True
    else:
        return False


def line_hits_enemy(bullet_x, bullet_y, direction_x, direction_y, enemy_x, enemy_y, enemy_radius):
    """
    Check if a line from (bullet_x, bullet_y) in direction (direction_x, direction_y)
    will hit the circle at (enemy_x, enemy_y) with radius enemy_radius.
    """
    dx = enemy_x - bullet_x
    dy = enemy_y - bullet_y

    dx_squared = dx * dx
    dy_squared = dy * dy

    distance_squared = dx_squared + dy_squared
    dot_product = dx * direction_x + dy * direction_y

    if dot_product < 0:
        collision_status = False
        return collision_status

    direction_length_sq = direction_x ** 2 + direction_y ** 2

    if direction_length_sq == 0:
        collision_status = False
        return collision_status

    numerator = abs(dx * direction_y - dy * direction_x)

    denominator = math.sqrt(direction_length_sq)

    perpendicular_distance = numerator / denominator

    actual_distance = perpendicular_distance

    if actual_distance <= enemy_radius:
        collision_status = True
    else:
        collision_status = False
    # Final collision status return
    return collision_status


def check_house_collision(x, y):
    """Check if position is inside house boundaries - expanded boundary for better movement"""
    # Expand boundary by 50 units on each side for better collision detection
    house_left = house_x - (house_width/2 + 50)
    house_right = house_x + (house_width/2 + 50)
    house_front = house_y + (house_depth/2 + 50)
    house_back = house_y - (house_depth/2 + 50)

    return (house_left < x < house_right) and (house_back < y < house_front)


def check_door_collision(x, y):
    """Check if player is near the main house door"""
    global house_x, house_y, house_width, house_depth
    door_x = house_x + house_width/3  # Door position
    door_y = house_y + house_depth/2  # Front wall
    door_width = 100

    # Check if player is within door area
    distance_to_door = math.sqrt((x - door_x)**2 + (y - door_y)**2)
    return distance_to_door < 120  # Larger door detection range


def check_neighbor1_door_collision(x, y):
    """Check if player is near neighbor1 house door"""
    door_x = neighbor1_x + neighbor1_width/3  # Door position
    door_y = neighbor1_y + neighbor1_depth/2  # Front wall

    # Check if player is within door area
    distance_to_door = math.sqrt((x - door_x)**2 + (y - door_y)**2)
    return distance_to_door < 150  # Larger door for merchant house


def check_neighbor2_door_collision(x, y):
    """Check if player is near neighbor2 house door"""
    door_x = neighbor2_x + neighbor2_width/3  # Door position
    door_y = neighbor2_y + neighbor2_depth/2  # Front wall

    # Check if player is within door area
    distance_to_door = math.sqrt((x - door_x)**2 + (y - door_y)**2)
    return distance_to_door < 150  # Larger door for merchant house


def check_neighbor3_door_collision(x, y):
    """Check if player is near neighbor3 house door"""
    door_x = neighbor3_x + neighbor3_width/3  # Door position
    door_y = neighbor3_y + neighbor3_depth/2  # Front wall

    # Check if player is within door area
    distance_to_door = math.sqrt((x - door_x)**2 + (y - door_y)**2)
    return distance_to_door < 150  # Larger door for merchant house


def check_neighbor1_collision(x, y):
    """Check if position is inside neighbor1 house boundaries"""
    house_left = neighbor1_x - (neighbor1_width/2 + 50)
    house_right = neighbor1_x + (neighbor1_width/2 + 50)
    house_front = neighbor1_y + (neighbor1_depth/2 + 50)
    house_back = neighbor1_y - (neighbor1_depth/2 + 50)

    return (house_left < x < house_right) and (house_back < y < house_front)


def check_neighbor2_collision(x, y):
    """Check if position is inside neighbor2 house boundaries"""
    house_left = neighbor2_x - (neighbor2_width/2 + 50)
    house_right = neighbor2_x + (neighbor2_width/2 + 50)
    house_front = neighbor2_y + (neighbor2_depth/2 + 50)
    house_back = neighbor2_y - (neighbor2_depth/2 + 50)

    return (house_left < x < house_right) and (house_back < y < house_front)


def check_neighbor3_collision(x, y):
    """Check if position is inside neighbor3 house boundaries"""
    house_left = neighbor3_x - (neighbor3_width/2 + 50)
    house_right = neighbor3_x + (neighbor3_width/2 + 50)
    house_front = neighbor3_y + (neighbor3_depth/2 + 50)
    house_back = neighbor3_y - (neighbor3_depth/2 + 50)

    return (house_left < x < house_right) and (house_back < y < house_front)


def is_inside_cave(x, y):
    """Check if position is inside cave boundaries"""
    cave_x = -2500
    cave_y = -2500
    cave_width = 1000
    cave_depth = 1000

    cave_left = cave_x - cave_width/2
    cave_right = cave_x + cave_width/2
    cave_front = cave_y + cave_depth/2
    cave_back = cave_y - cave_depth/2

    return (cave_left < x < cave_right) and (cave_back < y < cave_front)

def check_cave_collision(x, y):
    """Check if position collides with cave walls."""
    cave_x = -2500
    cave_y = -2500
    cave_width = 1000
    cave_depth = 1000
    wall_thickness = 40

    # Back wall
    if (x >= cave_x - cave_width/2 and x <= cave_x + cave_width/2 and
        y >= cave_y - cave_depth/2 - wall_thickness/2 and y <= cave_y - cave_depth/2 + wall_thickness/2):
        return True

    # Left wall
    if (x >= cave_x - cave_width/2 - wall_thickness/2 and x <= cave_x - cave_width/2 + wall_thickness/2 and
        y >= cave_y - cave_depth/2 and y <= cave_y + cave_depth/2):
        return True

    # Right wall
    if (x >= cave_x + cave_width/2 - wall_thickness/2 and x <= cave_x + cave_width/2 + wall_thickness/2 and
        y >= cave_y - cave_depth/2 and y <= cave_y + cave_depth/2):
        return True

    return False
    if (x >= cave_x - cave_width/2 - wall_thickness/2 and x <= cave_x - cave_width/2 + wall_thickness/2 and
        y >= cave_y - cave_depth/2 and y <= cave_y + cave_depth/2):
        return True

    # Right wall
    if (x >= cave_x + cave_width/2 - wall_thickness/2 and x <= cave_x + cave_width/2 + wall_thickness/2 and
        y >= cave_y - cave_depth/2 and y <= cave_y + cave_depth/2):
        return True

    # Front wall (with opening)
    opening_width = 200
    opening_left_x = cave_x - opening_width/2
    opening_right_x = cave_x + opening_width/2

    front_wall_y_min = cave_y + cave_depth/2 - wall_thickness/2
    front_wall_y_max = cave_y + cave_depth/2 + wall_thickness/2

    # Check if player is in the y-range of the front wall
    if (y >= front_wall_y_min and y <= front_wall_y_max):
        # Check if player is in the solid parts of the front wall
        if (x >= cave_x - cave_width/2 and x <= opening_left_x) or \
           (x >= opening_right_x and x <= cave_x + cave_width/2):
            return True

    return False

def check_cave_opening_collision(x, y):
    """Check if position is near the cave opening."""
    cave_x = -2500
    cave_y = -2500
    cave_depth = 1000
    opening_width = 200
    wall_thickness = 40

    opening_left_x = cave_x - opening_width / 2
    opening_right_x = cave_x + opening_width / 2
    opening_y = cave_y + cave_depth / 2

    # A small area around the opening
    return (opening_left_x - 20 < x < opening_right_x + 20 and
            opening_y - wall_thickness < y < opening_y + wall_thickness)

def check_lava_collision(x, y):
    """Check if player collides with lava blocks inside cave"""
    global lava_collision_count, player_lives
   
    # Only check lava collision if player is inside cave
    if not is_inside_cave(x, y):
        return False
   
    # Cave position offset
    cave_x = -2500
    cave_y = -2500
   
    # Lava block positions (relative to cave center)
    lava_positions = [
        (-200, -200, 25, 40),  # Large lava block
        (150, -150, 20, 35),   # Medium lava block
        (-100, 150, 30, 45),   # Large lava block
        (200, 100, 15, 30),    # Small lava block
        (-50, -100, 25, 40),   # Medium lava block
        (100, 200, 20, 35),    # Medium lava block
        (-150, 0, 35, 50),     # Extra large lava block
        (50, -200, 18, 32),    # Small-medium lava block
    ]
   
    player_radius = 20  # Player collision radius
   
    for lx, ly, lz, size in lava_positions:
        # Convert lava position to world coordinates
        world_lx = cave_x + lx
        world_ly = cave_y + ly
        lava_radius = size / 2
       
        # Check collision with lava block
        distance = math.sqrt((x - world_lx)**2 + (y - world_ly)**2)
        if distance < (player_radius + lava_radius):
            lava_collision_count += 1
           
            # Reduce health after 4 lava collisions
            if lava_collision_count >= 4:
                player_lives = 0  # Set health to zero
                lava_collision_count = 0  # Reset counter
           
            return True
   
    return False


def update_door_system():
    """Update door open/close system for all houses"""
    global door_open, door_timer
    global neighbor1_door_open, neighbor1_door_timer
    global neighbor2_door_open, neighbor2_door_timer
    global neighbor3_door_open, neighbor3_door_timer

    # Main house door
    near_door = check_door_collision(player_x, player_y)
    if near_door and not door_open:
        door_open = True
        door_timer = 0
        print(f"Main house door opened! Player at ({player_x:.1f}, {player_y:.1f})")

    if door_open:
        door_timer += 1
        if door_timer > door_auto_close_time:
            door_open = False
            door_timer = 0
            print("Main house door closed!")

    # Neighbor1 house door
    near_neighbor1_door = check_neighbor1_door_collision(player_x, player_y)
    if near_neighbor1_door and not neighbor1_door_open:
        neighbor1_door_open = True
        neighbor1_door_timer = 0
        print(f"Neighbor1 house door opened! Player at ({player_x:.1f}, {player_y:.1f})")

    if neighbor1_door_open:
        neighbor1_door_timer += 1
        if neighbor1_door_timer > door_auto_close_time:
            neighbor1_door_open = False
            neighbor1_door_timer = 0
            print("Neighbor1 house door closed!")

    # Neighbor2 house door
    near_neighbor2_door = check_neighbor2_door_collision(player_x, player_y)
    if near_neighbor2_door and not neighbor2_door_open:
        neighbor2_door_open = True
        neighbor2_door_timer = 0
        print(f"Neighbor2 house door opened! Player at ({player_x:.1f}, {player_y:.1f})")

    if neighbor2_door_open:
        neighbor2_door_timer += 1
        if neighbor2_door_timer > door_auto_close_time:
            neighbor2_door_open = False
            neighbor2_door_timer = 0
            print("Neighbor2 house door closed!")

    # Neighbor3 house door
    near_neighbor3_door = check_neighbor3_door_collision(player_x, player_y)
    if near_neighbor3_door and not neighbor3_door_open:
        neighbor3_door_open = True
        neighbor3_door_timer = 0
        print(f"Neighbor3 house door opened! Player at ({player_x:.1f}, {player_y:.1f})")

    if neighbor3_door_open:
        neighbor3_door_timer += 1
        if neighbor3_door_timer > door_auto_close_time:
            neighbor3_door_open = False
            neighbor3_door_timer = 0
            print("Neighbor3 house door closed!")


def open_door():
    """Open the door when player approaches"""
    global door_open, door_timer
    door_open = True
    door_timer = 0
    print("Door opened!")


def can_move_to_position(new_x, new_y):
    """Check if player can move to a new position"""
    # Check boundary restrictions - prevent movement outside play area
    if new_x <= -GRID_LENGTH or new_x >= GRID_LENGTH or new_y <= -GRID_LENGTH or new_y >= GRID_LENGTH:
        return False

    # Check if trying to enter main house
    if check_house_collision(new_x, new_y):
        # Only allow entry through open door when player is near door
        if door_open and check_door_collision(new_x, new_y):
            return True
        return False

    # Check if trying to enter neighbor1 house
    if check_neighbor1_collision(new_x, new_y):
        # Only allow entry through open door when player is near door
        if neighbor1_door_open and check_neighbor1_door_collision(new_x, new_y):
            return True
        return False

    # Check if trying to enter neighbor2 house
    if check_neighbor2_collision(new_x, new_y):
        # Only allow entry through open door when player is near door
        if neighbor2_door_open and check_neighbor2_door_collision(new_x, new_y):
            return True
        return False

    # Check if trying to enter neighbor3 house
    if check_neighbor3_collision(new_x, new_y):
        # Only allow entry through open door when player is near door
        if neighbor3_door_open and check_neighbor3_door_collision(new_x, new_y):
            return True
        return False

    # Check cave collision
    if check_cave_collision(new_x, new_y):
        return False

    # Check if leaving cave - only through opening
    if is_inside_cave(player_x, player_y) and not is_inside_cave(new_x, new_y):
        if not check_cave_opening_collision(player_x, player_y):
            return False

    # Check if leaving main house - only through door
    current_in_house = check_house_collision(player_x, player_y)
    if current_in_house and not check_house_collision(new_x, new_y):
        # Leaving house - must be through door area
        if door_open and check_door_collision(new_x, new_y):
            return True
        return False

    # Check if leaving neighbor1 house - only through door
    current_in_neighbor1 = check_neighbor1_collision(player_x, player_y)
    if current_in_neighbor1 and not check_neighbor1_collision(new_x, new_y):
        # Leaving house - must be through door area
        if neighbor1_door_open and check_neighbor1_door_collision(new_x, new_y):
            return True
        return False

    # Check if leaving neighbor2 house - only through door
    current_in_neighbor2 = check_neighbor2_collision(player_x, player_y)
    if current_in_neighbor2 and not check_neighbor2_collision(new_x, new_y):
        # Leaving house - must be through door area
        if neighbor2_door_open and check_neighbor2_door_collision(new_x, new_y):
            return True
        return False

    # Check if leaving neighbor3 house - only through door
    current_in_neighbor3 = check_neighbor3_collision(player_x, player_y)
    if current_in_neighbor3 and not check_neighbor3_collision(new_x, new_y):
        # Leaving house - must be through door area
        if neighbor3_door_open and check_neighbor3_door_collision(new_x, new_y):
            return True
        return False

    # Check lava collision - this will handle health reduction
    check_lava_collision(new_x, new_y)

    return True

def check_sword_enemy_collisions():
    """
    Check for collisions between the sword and enemies.
    Remove enemies that are hit by the sword.
    Increase score for each hit.
    """
    global player_x, player_y, player_cam_angle, sword_rotation
    global enemy_list, score, enem_rad_bottom

    # Calculate sword tip position based on player position and sword rotation
    sword_length = 80  # Total length of sword (handle + blade)
    player_cam_angle_rad = math.radians(player_cam_angle)

    # Calculate direction vector based on player angle
    dir_x = -math.sin(player_cam_angle_rad)
    dir_y = math.cos(player_cam_angle_rad)

    # Calculate perpendicular direction for sword extension
    perp_x = -dir_y
    perp_y = dir_x

    # Determine sword tip position based on rotation
    if sword_rotation == 0:  # Right hand
        sword_tip_x = player_x + (perp_x * sword_length)
        sword_tip_y = player_y + (perp_y * sword_length)
    else:  # Left hand
        sword_tip_x = player_x - (perp_x * sword_length)
        sword_tip_y = player_y - (perp_y * sword_length)

    # Sword collision radius (make it larger than the actual sword width for easier hits)
    sword_radius = 20

    # Check each enemy for collision with the sword
    remove_enemy_bag = []  # Indices of enemies to remove

    for enemy_num in range(len(enemy_list)):
        enemy_x, enemy_y, enemy_z = enemy_list[enemy_num]

        if collision_detector(sword_tip_x, sword_tip_y, sword_radius, enemy_x, enemy_y, enem_rad_bottom):
            if enemy_num not in remove_enemy_bag:
                remove_enemy_bag.append(enemy_num)
            score += 1
            print(f"Sword Hit! Score: {score}")

    # Remove hit enemies (in reverse order to avoid index issues)
    remove_enemy_bag.sort(reverse=True)
    for enemy_idx in remove_enemy_bag:
        enemy_list.pop(enemy_idx)


def check_bullet_enemy_collisions():
    """
    Check for collisions between bullets and enemies.
    Remove bullets and enemies that collide.
    Increase score for each hit.
    Spawn new enemies to replace removed ones.
    """
    global bullets_x, bullets_y, bullets_z
    global bullets_direction_x, bullets_direction_y, bullets_angle
    global enemy_list, score, enem_rad_bottom, cheat_mode
    global boss_health, boss_alive, boss_x, boss_y,boss_z

    bullet_bag = []           # Indices of bullets to remove
    remove_enemy_bag = []     # Indices of enemies to remove

    # Determine effective hit radius
    main_rad = enem_rad_bottom
    temp_main_rad = main_rad
    if cheat_mode:
        main_rad *= 5
        temp_main_rad = main_rad

    # Check each bullet against each enemy
    for bullets in range(len(bullets_x)):
        bullet_x = bullets_x[bullets]
        bullet_y = bullets_y[bullets]

        # Check boss collision first
        bullet_z = bullets_z[bullets]
        # Calculate actual boss z position (boss stands up when player enters cave)
        actual_boss_z = boss_z + (40 if boss_standing else 0)
        if boss_alive and collision_detector_3d(bullet_x, bullet_y, bullet_z, 2, boss_x, boss_y, actual_boss_z, 50):
            if bullets not in bullet_bag:
                bullet_bag.append(bullets)
            boss_health -= 1
            score += 1
            print(f"Boss hit! Boss health: {boss_health}, Score: {score}")
            if boss_health <= 0:
                boss_alive = False
                score += 50  # Bonus points for killing boss
                print("Boss defeated!")

        for enemy_num in range(len(enemy_list)):
            enemy_x, enemy_y, enemy_z = enemy_list[enemy_num]

            if collision_detector(bullet_x, bullet_y, 2, enemy_x, enemy_y, main_rad):
                if bullets not in bullet_bag:
                    bullet_bag.append(bullets)
                if enemy_num not in remove_enemy_bag:
                    remove_enemy_bag.append(enemy_num)
                score += 1
                print(f"Hit! Score: {score}")

    #bubble sort for bullets
    n = len(bullet_bag)
    for i in range(n):
        for j in range(0, n-i-1):
            if bullet_bag[j] > bullet_bag[j+1]:
                # Swap
                temp = bullet_bag[j]
                bullet_bag[j] = bullet_bag[j+1]
                bullet_bag[j+1] = temp

    # ----------------------------
    # Reverse the sorted bullets manually
    reversed_bullet_bag = []
    for i in range(len(bullet_bag)-1, -1, -1):
        reversed_bullet_bag.append(bullet_bag[i])

    # Remove bullets
    for bullets in reversed_bullet_bag:
        if bullets < len(bullets_x):
            temp_x = bullets_x[bullets]
            bullets_x.pop(bullets)
            temp_x = None
        if bullets < len(bullets_y):
            temp_val_y = bullets_y[bullets]
            bullets_y.pop(bullets)
            temp_val_y = None
        if bullets < len(bullets_z):
            temp_val_z = bullets_z[bullets]
            bullets_z.pop(bullets)
            temp_val_z = None
        if bullets < len(bullets_direction_x):
            temp_val_dx = bullets_direction_x[bullets]
            bullets_direction_x.pop(bullets)
            temp_val_dx = None
        if bullets < len(bullets_direction_y):
            temp_val_dy = bullets_direction_y[bullets]
            bullets_direction_y.pop(bullets)
            temp_val_dy = None
        if bullets < len(bullets_angle):
            temp_val_angle = bullets_angle[bullets]
            bullets_angle.pop(bullets)
            temp_val_angle = None

    #Removing enemy
    remove_list = []
    for dead_enemy in remove_enemy_bag:
        remove_list.append(dead_enemy)

    while len(remove_list) > 0:
        val_new = remove_list[0]
        for dead_enemy in remove_list:
            if dead_enemy > val_new:
                val_new = dead_enemy
        remove_list.remove(val_new)
        if val_new < len(enemy_list):
            dead_bot = enemy_list[val_new]
            enemy_list.pop(val_new)
            dead_bot = None

    # Spawn new enemies for each removed enemy
    total_dead = len(remove_enemy_bag)
    make_new = 0
    while make_new < total_dead:
        make_new_enemy()
        make_new += 1

def make_new_enemy():
    """
    Spawn a new enemy at a random location away from player.
    This version is intentionally verbose and lengthy, with redundant code
    for clarity and padding purposes, but the behavior is the same.
    """
    global enemy_list

    # Track how many times we attempt spawning
    tries = 0
    bot_create_tries = 20  # Prevent infinite loops in case of unlucky randoms

    # Flag to indicate if enemy was successfully spawned
    enemy_spawned = False

    # Try until we succeed or run out of tries
    while True:
        # Step 1: Check if maximum tries exceeded
        tries_remaining = bot_create_tries - tries
        bot_create_tries_not_reached = tries_remaining > 0  # True if we can still try

        # Step 2: Check if enemy is already spawned
        enemy_not_yet_spawned = not enemy_spawned  # True if we still need to spawn

        # Step 3: Combine both conditions
        should_continue = bot_create_tries_not_reached and enemy_not_yet_spawned

        # Step 4: Break if we should not continue
        if not should_continue:
            break

        # --- Place the body of the loop here ---
        # For example, generate random position, check distance, etc.

        # Increment tries at the end
        tries += 1

        # Generate random X coordinate for enemy
        random_x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        # Assign it explicitly to enemy_x (redundant)
        enemy_x = random_x

        # Generate random Y coordinate for enemy
        random_y = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        # Assign it explicitly to enemy_y (redundant)
        enemy_y = random_y

        # Calculate differences separately (unnecessary but verbose)
        diff_x = enemy_x - player_x
        diff_y = enemy_y - player_y

        # Compute squared differences
        square_diff_x = diff_x ** 2
        square_diff_y = diff_y ** 2

        # Distance to player
        distance_to_player = math.sqrt(square_diff_x + square_diff_y)

        # Extra boolean check before condition
        far_player = distance_to_player > 100
        not_in_house = not check_house_collision(enemy_x, enemy_y)
        not_in_cave = not check_cave_collision(enemy_x, enemy_y)

        # Check if enemy is not in any house (main house or neighbor houses)
        not_in_neighbor1 = not check_neighbor1_collision(enemy_x, enemy_y)
        not_in_neighbor2 = not check_neighbor2_collision(enemy_x, enemy_y)
        not_in_neighbor3 = not check_neighbor3_collision(enemy_x, enemy_y)

        if far_player and not_in_house and not_in_cave and not_in_neighbor1 and not_in_neighbor2 and not_in_neighbor3:
            # Z-coordinate (always 0 for now)
            enemy_z = enem_rad_bottom

            # Create enemy tuple in steps
            enemy_position = (enemy_x, enemy_y, enemy_z)
            new_enemy = enemy_position

            # Append to list
            enemy_list.append(new_enemy)

            # Mark spawn success
            enemy_spawned = True
        else:
            print(f"Enemy too close to player on attempt {tries + 1}, trying again...")

        # Increment attempt counter
        tries = tries + 1

        # Redundant safety check: break if already spawned
        if enemy_spawned:
            break

    # Extra redundant final check
    if enemy_spawned is False:
        # Do nothing, just verbose
        spawn_failed = True
        if spawn_failed:
            pass  # filler line


def draw_scaled_cuboid(length=200, width=100, height=80):
    glPushMatrix()

    # Scale factors relative to cube size
    # glutSolidCube(1) makes a unit cube, we scale it to desired size
    glScalef(length, width, height)
    glutSolidCube(1)

    glPopMatrix()


def draw_chicken(x, y, z):
    """Draw a chicken with white sphere body, red cone beak, and cylindrical legs"""
    global chicken_bob_angle

    glPushMatrix()
    glTranslatef(x, y, z)

    # Add bobbing animation
    bob_offset = math.sin(math.radians(chicken_bob_angle)) * 3
    glTranslatef(0, 0, bob_offset)

    # Chicken body (white sphere)
    glPushMatrix()
    glTranslatef(0, 0, 15)  # Lift body above ground
    glColor3f(1.0, 1.0, 1.0)  # White color
    gluSphere(gluNewQuadric(), 12, 16, 16)
    glPopMatrix()

    # Chicken head (smaller white sphere)
    glPushMatrix()
    glTranslatef(0, 8, 22)  # Position head in front and above body
    glColor3f(1.0, 1.0, 1.0)  # White color
    gluSphere(gluNewQuadric(), 6, 12, 12)
    glPopMatrix()

    # Chicken beak (red cone)
    glPushMatrix()
    glTranslatef(0, 12, 22)  # Position beak in front of head
    glRotatef(90, 1, 0, 0)  # Point cone forward
    glColor3f(1.0, 0.2, 0.2)  # Red color
    gluCylinder(gluNewQuadric(), 2, 0, 4, 8, 8)
    glPopMatrix()

    # Left leg (cylindrical)
    glPushMatrix()
    glTranslatef(-4, 0, 0)  # Position left leg
    glColor3f(1.0, 0.8, 0.0)  # Yellow/orange color
    gluCylinder(gluNewQuadric(), 1.5, 1.5, 8, 8, 8)
    glPopMatrix()

    # Right leg (cylindrical)
    glPushMatrix()
    glTranslatef(4, 0, 0)  # Position right leg
    glColor3f(1.0, 0.8, 0.0)  # Yellow/orange color
    gluCylinder(gluNewQuadric(), 1.5, 1.5, 8, 8, 8)
    glPopMatrix()

    # Left foot (small flat cylinder)
    glPushMatrix()
    glTranslatef(-4, 2, 0)
    glColor3f(1.0, 0.8, 0.0)  # Yellow/orange color
    gluCylinder(gluNewQuadric(), 3, 3, 1, 8, 8)
    glPopMatrix()

    # Right foot (small flat cylinder)
    glPushMatrix()
    glTranslatef(4, 2, 0)
    glColor3f(1.0, 0.8, 0.0)  # Yellow/orange color
    gluCylinder(gluNewQuadric(), 3, 3, 1, 8, 8)
    glPopMatrix()

    glPopMatrix()


def draw_chicken_coop(x, y, z):
    """Draw a chicken coop with cylindrical fences and multiple chickens"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # Coop dimensions
    coop_width = 80
    coop_depth = 80
    fence_height = 25
    fence_radius = 2

    # Draw fence posts around the perimeter
    fence_posts = [
        # Front fence
        (-coop_width/2, coop_depth/2, 0),
        (-coop_width/4, coop_depth/2, 0),
        (0, coop_depth/2, 0),
        (coop_width/4, coop_depth/2, 0),
        (coop_width/2, coop_depth/2, 0),
        # Back fence
        (-coop_width/2, -coop_depth/2, 0),
        (-coop_width/4, -coop_depth/2, 0),
        (0, -coop_depth/2, 0),
        (coop_width/4, -coop_depth/2, 0),
        (coop_width/2, -coop_depth/2, 0),
        # Left fence
        (-coop_width/2, -coop_depth/4, 0),
        (-coop_width/2, 0, 0),
        (-coop_width/2, coop_depth/4, 0),
        # Right fence
        (coop_width/2, -coop_depth/4, 0),
        (coop_width/2, 0, 0),
        (coop_width/2, coop_depth/4, 0),
    ]

    # Draw cylindrical fence posts
    for post_x, post_y, post_z in fence_posts:
        glPushMatrix()
        glTranslatef(post_x, post_y, post_z)
        glColor3f(0.6, 0.4, 0.2)  # Brown fence color
        gluCylinder(gluNewQuadric(), fence_radius, fence_radius, fence_height, 8, 8)
        glPopMatrix()

    # Draw horizontal fence rails
    rail_positions = [8, 16]  # Two horizontal rails at different heights
    for rail_height in rail_positions:
        # Front and back rails
        for side_y in [-coop_depth/2, coop_depth/2]:
            glPushMatrix()
            glTranslatef(0, side_y, rail_height)
            glRotatef(90, 0, 1, 0)  # Rotate to horizontal
            glColor3f(0.6, 0.4, 0.2)  # Brown fence color
            gluCylinder(gluNewQuadric(), fence_radius*0.7, fence_radius*0.7, coop_width, 8, 8)
            glPopMatrix()

        # Left and right rails
        for side_x in [-coop_width/2, coop_width/2]:
            glPushMatrix()
            glTranslatef(side_x, 0, rail_height)
            glRotatef(90, 1, 0, 0)  # Rotate to horizontal
            glColor3f(0.6, 0.4, 0.2)  # Brown fence color
            gluCylinder(gluNewQuadric(), fence_radius*0.7, fence_radius*0.7, coop_depth, 8, 8)
            glPopMatrix()

    # Draw chickens inside the coop
    chicken_positions = [
        (-20, -20, 0),
        (15, -15, 0),
        (-10, 20, 0),
        (25, 10, 0),
        (0, 0, 0)
    ]

    for chicken_x, chicken_y, chicken_z in chicken_positions:
        draw_chicken(chicken_x, chicken_y, chicken_z)

    glPopMatrix()


def draw_cow(x, y, z):
    """Draw a cow with black and white spotted body"""
    global cow_tail_angle

    glPushMatrix()
    glTranslatef(x, y, z)

    # Cow body (main white body)
    glPushMatrix()
    glTranslatef(0, 0, 25)  # Lift body above ground
    glColor3f(1.0, 1.0, 1.0)  # White base color
    glScalef(40, 20, 15)  # Elongated body
    glutSolidCube(1)
    glPopMatrix()

    # Black spots on body
    spot_positions = [
        (-8, 0, 28, 4),   # Left side spot
        (10, 0, 30, 5),   # Right side spot
        (-5, 0, 22, 3),   # Lower left spot
        (8, 0, 24, 4),    # Lower right spot
        (0, 0, 32, 3),    # Top center spot
    ]

    for spot_x, spot_y, spot_z, spot_size in spot_positions:
        glPushMatrix()
        glTranslatef(spot_x, spot_y, spot_z)
        glColor3f(0.0, 0.0, 0.0)  # Black spots
        gluSphere(gluNewQuadric(), spot_size, 8, 8)
        glPopMatrix()

    # Cow head (white)
    glPushMatrix()
    glTranslatef(0, 15, 30)  # Position head in front
    glColor3f(1.0, 1.0, 1.0)  # White color
    glScalef(12, 8, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Cow snout (pink)
    glPushMatrix()
    glTranslatef(0, 19, 28)
    glColor3f(1.0, 0.7, 0.7)  # Pink snout
    glScalef(8, 4, 6)
    glutSolidCube(1)
    glPopMatrix()

    # Cow ears (black)
    glPushMatrix()
    glTranslatef(-6, 15, 35)
    glColor3f(0.0, 0.0, 0.0)  # Black ears
    glScalef(3, 2, 6)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(6, 15, 35)
    glColor3f(0.0, 0.0, 0.0)  # Black ears
    glScalef(3, 2, 6)
    glutSolidCube(1)
    glPopMatrix()

    # Cow horns (white)
    glPushMatrix()
    glTranslatef(-3, 15, 38)
    glColor3f(0.9, 0.9, 0.8)  # Off-white horns
    gluCylinder(gluNewQuadric(), 1, 0, 6, 6, 6)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(3, 15, 38)
    glColor3f(0.9, 0.9, 0.8)  # Off-white horns
    gluCylinder(gluNewQuadric(), 1, 0, 6, 6, 6)
    glPopMatrix()

    # Cow legs (white with black hooves)
    leg_positions = [
        (-12, 6, 0),   # Front left
        (12, 6, 0),    # Front right
        (-12, -6, 0),  # Back left
        (12, -6, 0),   # Back right
    ]

    for leg_x, leg_y, leg_z in leg_positions:
        # White leg
        glPushMatrix()
        glTranslatef(leg_x, leg_y, leg_z)
        glColor3f(1.0, 1.0, 1.0)  # White leg
        gluCylinder(gluNewQuadric(), 3, 3, 15, 8, 8)
        glPopMatrix()

        # Black hoof
        glPushMatrix()
        glTranslatef(leg_x, leg_y, 0)
        glColor3f(0.0, 0.0, 0.0)  # Black hoof
        gluCylinder(gluNewQuadric(), 4, 4, 2, 8, 8)
        glPopMatrix()

    # Cow tail (animated)
    tail_sway = math.sin(math.radians(cow_tail_angle)) * 15
    glPushMatrix()
    glTranslatef(-20, 0, 20)
    glRotatef(tail_sway, 0, 0, 1)  # Sway tail
    glColor3f(0.0, 0.0, 0.0)  # Black tail
    gluCylinder(gluNewQuadric(), 1.5, 0.5, 12, 6, 6)
    glPopMatrix()

    # Udder (pink)
    glPushMatrix()
    glTranslatef(0, -5, 15)
    glColor3f(1.0, 0.7, 0.7)  # Pink udder
    gluSphere(gluNewQuadric(), 6, 8, 8)
    glPopMatrix()

    glPopMatrix()


def draw_milk_cans(x, y, z):
    """Draw milk cans for the cow neighbor's offering"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # Draw multiple milk cans in a group
    can_positions = [
        (-15, 0, 0),
        (0, 0, 0),
        (15, 0, 0),
        (-7, 15, 0),
        (7, 15, 0)
    ]

    for can_x, can_y, can_z in can_positions:
        glPushMatrix()
        glTranslatef(can_x, can_y, can_z)

        # Milk can body (silver/metallic)
        glColor3f(0.8, 0.8, 0.9)  # Silver color
        gluCylinder(gluNewQuadric(), 6, 6, 20, 12, 12)

        # Milk can lid (darker silver)
        glPushMatrix()
        glTranslatef(0, 0, 20)
        glColor3f(0.6, 0.6, 0.7)  # Darker silver
        gluCylinder(gluNewQuadric(), 7, 7, 2, 12, 12)
        glPopMatrix()

        # Handle on the side
        glPushMatrix()
        glTranslatef(8, 0, 15)
        glRotatef(90, 0, 1, 0)
        glColor3f(0.5, 0.5, 0.6)  # Dark handle
        # Replace torus with cylinder for handle
        gluCylinder(gluNewQuadric(), 2.5, 2.5, 2, 8, 1)
        glPopMatrix()

        glPopMatrix()

    glPopMatrix()


def draw_apple_tree(x, y, z):
    """Draw an apple tree with red apples on branches"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # Tree trunk
    trunk_height = 120
    trunk_radius = 8
    glColor3f(0.55, 0.27, 0.07)  # Brown trunk
    gluCylinder(gluNewQuadric(), trunk_radius, trunk_radius * 0.8, trunk_height, 16, 16)

    # Main foliage (green sphere)
    glPushMatrix()
    glTranslatef(0, 0, trunk_height + 30)
    glColor3f(0.2, 0.7, 0.2)  # Green foliage
    gluSphere(gluNewQuadric(), 40, 16, 16)
    glPopMatrix()

    # Additional foliage clusters for fuller tree
    foliage_positions = [
        (-20, 20, trunk_height + 20, 25),
        (25, -15, trunk_height + 25, 28),
        (-15, -25, trunk_height + 30, 22),
        (20, 25, trunk_height + 35, 26),
        (0, 0, trunk_height + 50, 20)
    ]

    for foliage_x, foliage_y, foliage_z, foliage_size in foliage_positions:
        glPushMatrix()
        glTranslatef(foliage_x, foliage_y, foliage_z)
        glColor3f(0.1, 0.6, 0.1)  # Slightly darker green
        gluSphere(gluNewQuadric(), foliage_size, 12, 12)
        glPopMatrix()

    # Draw apples scattered throughout the tree - more apples added
    apple_positions = [
        # Lower apples (easier to see)
        (-25, 15, trunk_height + 10, 3),
        (20, -10, trunk_height + 15, 3),
        (-10, -20, trunk_height + 20, 3),
        (15, 20, trunk_height + 25, 3),
        (-30, -5, trunk_height + 18, 3),
        (25, 25, trunk_height + 22, 3),
        (-35, 25, trunk_height + 12, 3),
        (35, -15, trunk_height + 16, 3),
        (-5, -35, trunk_height + 14, 3),
        (30, 5, trunk_height + 19, 3),
        # Middle apples
        (-15, 25, trunk_height + 35, 3),
        (30, -20, trunk_height + 30, 3),
        (-20, -30, trunk_height + 40, 3),
        (10, 15, trunk_height + 45, 3),
        (0, -25, trunk_height + 38, 3),
        (-25, 0, trunk_height + 42, 3),
        (-35, -15, trunk_height + 32, 3),
        (35, 10, trunk_height + 36, 3),
        (-12, 35, trunk_height + 41, 3),
        (18, -35, trunk_height + 33, 3),
        (-28, -28, trunk_height + 39, 3),
        (32, 32, trunk_height + 37, 3),
        # Higher apples
        (-10, 10, trunk_height + 55, 3),
        (15, -15, trunk_height + 60, 3),
        (0, 20, trunk_height + 65, 3),
        (-20, -10, trunk_height + 58, 3),
        (-25, 30, trunk_height + 52, 3),
        (28, -25, trunk_height + 56, 3),
        (-8, -30, trunk_height + 62, 3),
        (22, 18, trunk_height + 59, 3),
        (-32, -8, trunk_height + 54, 3),
        (12, 35, trunk_height + 61, 3),
        # Top apples
        (-5, 5, trunk_height + 70, 3),
        (8, -8, trunk_height + 72, 3),
        (-12, 15, trunk_height + 68, 3),
        (18, -5, trunk_height + 74, 3)
    ]

    for apple_x, apple_y, apple_z, apple_size in apple_positions:
        glPushMatrix()
        glTranslatef(apple_x, apple_y, apple_z)
        glColor3f(0.9, 0.1, 0.1)  # Red apple
        gluSphere(gluNewQuadric(), apple_size, 8, 8)

        # Apple stem (small brown cylinder)
        glPushMatrix()
        glTranslatef(0, 0, apple_size)
        glColor3f(0.4, 0.2, 0.1)  # Brown stem
        gluCylinder(gluNewQuadric(), 0.5, 0.5, 2, 4, 4)
        glPopMatrix()

        glPopMatrix()

    glPopMatrix()


def draw_apple_basket(x, y, z):
    """Draw a basket filled with apples"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # Basket base (brown woven look)
    basket_radius = 12
    basket_height = 8

    # Draw basket bottom
    glPushMatrix()
    glColor3f(0.6, 0.4, 0.2)  # Brown basket color
    gluCylinder(gluNewQuadric(), basket_radius, basket_radius * 0.9, basket_height, 16, 16)
    glPopMatrix()

    # Draw basket rim
    glPushMatrix()
    glTranslatef(0, 0, basket_height)
    glColor3f(0.5, 0.3, 0.1)  # Darker brown rim
    # Replace torus with cylinder for rim
    gluCylinder(gluNewQuadric(), basket_radius + 0.5, basket_radius + 0.5, 2, 16, 1)
    glPopMatrix()

    # Draw basket handle
    glPushMatrix()
    glTranslatef(0, 0, basket_height + 5)
    glRotatef(90, 1, 0, 0)
    glColor3f(0.5, 0.3, 0.1)  # Brown handle
    # Replace torus with cylinder for handle
    gluCylinder(gluNewQuadric(), 6.5, 6.5, 3, 12, 1)
    glPopMatrix()

    # Draw apples in the basket
    apple_in_basket_positions = [
        # Bottom layer
        (-6, -6, basket_height + 2, 2.5),
        (6, -6, basket_height + 2, 2.5),
        (-6, 6, basket_height + 2, 2.5),
        (6, 6, basket_height + 2, 2.5),
        (0, 0, basket_height + 2, 2.5),
        # Middle layer
        (-3, -3, basket_height + 6, 2.5),
        (3, -3, basket_height + 6, 2.5),
        (-3, 3, basket_height + 6, 2.5),
        (3, 3, basket_height + 6, 2.5),
        # Top layer
        (0, -2, basket_height + 10, 2.5),
        (0, 2, basket_height + 10, 2.5),
        # Extra apples for fullness
        (-8, 0, basket_height + 3, 2.5),
        (8, 0, basket_height + 3, 2.5),
        (0, -8, basket_height + 3, 2.5),
        (0, 8, basket_height + 3, 2.5)
    ]

    for apple_x, apple_y, apple_z, apple_size in apple_in_basket_positions:
        glPushMatrix()
        glTranslatef(apple_x, apple_y, apple_z)

        # Vary apple colors slightly
        if (apple_x + apple_y) % 3 == 0:
            glColor3f(0.9, 0.1, 0.1)  # Bright red
        elif (apple_x + apple_y) % 3 == 1:
            glColor3f(0.8, 0.3, 0.1)  # Red-orange
        else:
            glColor3f(0.7, 0.1, 0.1)  # Dark red

        gluSphere(gluNewQuadric(), apple_size, 8, 8)

        # Small apple stem
        glPushMatrix()
        glTranslatef(0, 0, apple_size)
        glColor3f(0.4, 0.2, 0.1)  # Brown stem
        gluCylinder(gluNewQuadric(), 0.3, 0.3, 1, 4, 4)
        glPopMatrix()

        glPopMatrix()

    glPopMatrix()


def draw_neighbor_house(x, y, z, house_color=(0.8, 0.7, 0.5)):
    """Draw a neighbor house with courtyard"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # House dimensions
    house_width = 300
    house_depth = 300
    house_height = 160
    wall_thickness = 15

    # Draw house foundation/floor
    glPushMatrix()
    glTranslatef(0, 0, 5)
    glColor3f(0.5, 0.5, 0.5)  # Gray foundation
    glScalef(house_width, house_depth, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Draw house walls
    # Front wall
    glPushMatrix()
    glTranslatef(0, house_depth/2 - wall_thickness/2, house_height/2)
    glColor3f(house_color[0], house_color[1], house_color[2])  # Custom house color
    glScalef(house_width, wall_thickness, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Back wall
    glPushMatrix()
    glTranslatef(0, -house_depth/2 + wall_thickness/2, house_height/2)
    glColor3f(house_color[0], house_color[1], house_color[2])
    glScalef(house_width, wall_thickness, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Left wall
    glPushMatrix()
    glTranslatef(-house_width/2 + wall_thickness/2, 0, house_height/2)
    glColor3f(house_color[0], house_color[1], house_color[2])
    glScalef(wall_thickness, house_depth, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Right wall
    glPushMatrix()
    glTranslatef(house_width/2 - wall_thickness/2, 0, house_height/2)
    glColor3f(house_color[0], house_color[1], house_color[2])
    glScalef(wall_thickness, house_depth, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Draw roof (triangular)
    glBegin(GL_TRIANGLES)
    glColor3f(0.6, 0.2, 0.2)  # Red roof

    # Front triangle
    glVertex3f(-house_width/2, house_depth/2, house_height)
    glVertex3f(house_width/2, house_depth/2, house_height)
    glVertex3f(0, house_depth/2, house_height + 40)

    # Back triangle
    glVertex3f(-house_width/2, -house_depth/2, house_height)
    glVertex3f(house_width/2, -house_depth/2, house_height)
    glVertex3f(0, -house_depth/2, house_height + 40)

    glEnd()

    # Roof sides
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.15, 0.15)  # Darker red for sides

    # Left roof side
    glVertex3f(-house_width/2, -house_depth/2, house_height)
    glVertex3f(-house_width/2, house_depth/2, house_height)
    glVertex3f(0, house_depth/2, house_height + 40)
    glVertex3f(0, -house_depth/2, house_height + 40)

    # Right roof side
    glVertex3f(house_width/2, -house_depth/2, house_height)
    glVertex3f(house_width/2, house_depth/2, house_height)
    glVertex3f(0, house_depth/2, house_height + 40)
    glVertex3f(0, -house_depth/2, house_height + 40)

    glEnd()

    # Draw door
    glPushMatrix()
    glTranslatef(house_width/3, house_depth/2 - wall_thickness/2, 30)
    glColor3f(0.4, 0.2, 0.1)  # Brown door
    glScalef(25, wall_thickness + 2, 60)
    glutSolidCube(1)
    glPopMatrix()

    # Draw windows
    window_positions = [
        (-house_width/3, house_depth/2 - wall_thickness/2, 50),  # Front left window
        (house_width/3, -house_depth/2 + wall_thickness/2, 50),  # Back right window
        (-house_width/2 + wall_thickness/2, house_depth/4, 50),  # Left side window
        (house_width/2 - wall_thickness/2, -house_depth/4, 50),  # Right side window
    ]

    for win_x, win_y, win_z in window_positions:
        glPushMatrix()
        glTranslatef(win_x, win_y, win_z)
        glColor3f(0.7, 0.9, 1.0)  # Light blue window
        glScalef(20, wall_thickness + 1, 20)
        glutSolidCube(1)
        glPopMatrix()

    # Draw courtyard fence around the house
    courtyard_size = 280
    fence_height = 20
    fence_posts = []

    # Generate fence posts around courtyard perimeter
    for i in range(20):  # Front fence
        post_x = -courtyard_size/2 + (i * courtyard_size/19)
        fence_posts.append((post_x, courtyard_size/2, 0))

    for i in range(20):  # Back fence
        post_x = -courtyard_size/2 + (i * courtyard_size/19)
        fence_posts.append((post_x, -courtyard_size/2, 0))

    for i in range(1, 19):  # Left fence (skip corners)
        post_y = -courtyard_size/2 + (i * courtyard_size/19)
        fence_posts.append((-courtyard_size/2, post_y, 0))

    for i in range(1, 19):  # Right fence (skip corners)
        post_y = -courtyard_size/2 + (i * courtyard_size/19)
        fence_posts.append((courtyard_size/2, post_y, 0))

    # Draw fence posts
    for post_x, post_y, post_z in fence_posts:
        glPushMatrix()
        glTranslatef(post_x, post_y, post_z)
        glColor3f(0.6, 0.4, 0.2)  # Brown fence
        gluCylinder(gluNewQuadric(), 2, 2, fence_height, 6, 6)
        glPopMatrix()

    glPopMatrix()


def draw_text(x, y, text):
    """Simple text rendering without glutBitmapCharacter to avoid font errors"""
    # For now, just print to console instead of rendering on screen
    # This prevents the font errors while maintaining functionality
    pass


def update_merchants():
    """Update merchant movement inside houses"""
    global merchant1_x, merchant1_y, merchant1_move_timer, merchant1_direction
    global merchant2_x, merchant2_y, merchant2_move_timer, merchant2_direction
    global merchant3_x, merchant3_y, merchant3_move_timer, merchant3_direction

    move_range = 80  # How far merchants move inside house
    move_speed = 0.5

    # Update merchant 1 (horizontal movement)
    merchant1_move_timer += 1
    if merchant1_move_timer % 120 == 0:  # Change direction every 2 seconds
        merchant1_direction *= -1
    merchant1_x = neighbor1_x + merchant1_direction * move_range * math.sin(merchant1_move_timer * 0.02)

    # Update merchant 2 (vertical movement)
    merchant2_move_timer += 1
    if merchant2_move_timer % 150 == 0:  # Change direction every 2.5 seconds
        merchant2_direction *= -1
    merchant2_y = neighbor2_y + merchant2_direction * move_range * math.sin(merchant2_move_timer * 0.015)

    # Update merchant 3 (diagonal movement)
    merchant3_move_timer += 1
    if merchant3_move_timer % 180 == 0:  # Change direction every 3 seconds
        merchant3_direction *= -1
    merchant3_x = neighbor3_x + merchant3_direction * move_range * 0.7 * math.sin(merchant3_move_timer * 0.01)
    merchant3_y = neighbor3_y + merchant3_direction * move_range * 0.7 * math.cos(merchant3_move_timer * 0.01)


def draw_merchant(merchant_x, merchant_y, merchant_angle):
    """Draw a merchant NPC similar to the player character"""
    glPushMatrix()
    # Move and rotate the entire merchant
    glTranslatef(merchant_x, merchant_y, 0)  # Base position at ground
    glRotatef(merchant_angle, 0, 0, 1)

    # --- BODY ---
    glPushMatrix()
    glTranslatef(0, 0, 60)  # body center above ground
    glColor3f(0, 0, 1)  # Blue body to distinguish from player
    draw_scaled_cuboid(50, 20, 60)
    glPopMatrix()

    # --- LEFT LEG ---
    glPushMatrix()
    glTranslatef(-15, 0, 0)  # relative to body
    glColor3f(0.5, 0.3, 0.1)  # Brown legs
    gluCylinder(gluNewQuadric(), 5, 10, 40, 20, 20)
    glPopMatrix()

    # --- RIGHT LEG ---
    glPushMatrix()
    glTranslatef(15, 0, 0)
    glColor3f(0.5, 0.3, 0.1)  # Brown legs
    gluCylinder(gluNewQuadric(), 5, 10, 40, 20, 20)
    glPopMatrix()

    # --- LEFT ARM ---
    glPushMatrix()
    glTranslatef(-15, 0, 75)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.8, 0.6, 0.4)  # Skin color
    gluCylinder(gluNewQuadric(), 7, 5, 35, 20, 20)
    glPopMatrix()

    # --- RIGHT ARM ---
    glPushMatrix()
    glTranslatef(15, 0, 75)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.8, 0.6, 0.4)  # Skin color
    gluCylinder(gluNewQuadric(), 7, 5, 35, 20, 20)

    # Add basket to merchant3's hand (apple merchant)
    if abs(merchant_x - neighbor3_x) < 200 and abs(merchant_y - neighbor3_y) < 200:  # Check if this is merchant3
        glPushMatrix()
        glTranslatef(0, -40, 0)  # Position basket at end of arm
        glRotatef(90, 1, 0, 0)  # Rotate basket to hang properly

        # Basket base (brown woven look)
        basket_radius = 8
        basket_height = 6

        # Draw basket bottom
        glColor3f(0.6, 0.4, 0.2)  # Brown basket color
        gluCylinder(gluNewQuadric(), basket_radius, basket_radius * 0.9, basket_height, 16, 16)

        # Draw basket rim
        glPushMatrix()
        glTranslatef(0, 0, basket_height)
        glColor3f(0.5, 0.3, 0.1)  # Darker brown rim
        # Replace torus with cylinder for rim
        gluCylinder(gluNewQuadric(), basket_radius + 0.4, basket_radius + 0.4, 1.6, 16, 1)
        glPopMatrix()

        # Draw basket handle (connected to hand)
        glPushMatrix()
        glTranslatef(0, 0, basket_height + 3)
        glRotatef(90, 1, 0, 0)
        glColor3f(0.5, 0.3, 0.1)  # Brown handle
        # Replace torus with cylinder for handle
        gluCylinder(gluNewQuadric(), 5, 5, 2, 12, 1)
        glPopMatrix()

        # Draw apples in the basket
        apple_positions = [
            (-4, -4, basket_height + 1, 2),
            (4, -4, basket_height + 1, 2),
            (-4, 4, basket_height + 1, 2),
            (4, 4, basket_height + 1, 2),
            (0, 0, basket_height + 1, 2),
            (-2, -2, basket_height + 4, 2),
            (2, -2, basket_height + 4, 2),
            (0, 2, basket_height + 4, 2)
        ]

        for apple_x, apple_y, apple_z, apple_size in apple_positions:
            glPushMatrix()
            glTranslatef(apple_x, apple_y, apple_z)
            glColor3f(0.9, 0.1, 0.1)  # Red apple
            gluSphere(gluNewQuadric(), apple_size, 8, 8)
            glPopMatrix()

        glPopMatrix()

    glPopMatrix()

    # --- HEAD ---
    glPushMatrix()
    glTranslatef(0, 0, 100)  # top of body
    glColor3f(0.9, 0.7, 0.5)  # Skin color for head
    gluSphere(gluNewQuadric(), 15, 10, 10)
    glPopMatrix()

    glPopMatrix()  # End merchant transformations


def update_enemies():
    global enem_rad_bottom, enem_rad_top, enem_growing
    global enemy_list, player_x, player_y
    global player_hit_count, count, player_lives

    # Animate bottom sphere
    if enem_growing:
        enem_rad_bottom += 0.125
        if enem_rad_bottom >= 40:
            enem_growing = False
    else:
        enem_rad_bottom -= 0.125
        if enem_rad_bottom <= 35:
            enem_growing = True

    enem_rad_top = 2 * enem_rad_bottom - 55

    # Zombie movement speed - controls how fast zombies chase the player
    # Lower values = slower zombies, higher values = faster zombies
    # Current value 0.1 provides moderate zombie speed for balanced gameplay
    enemy_speed = 0.8
    updated_enemies = []
    enemies_to_respawn = []

    for enemy_num, enemy in enumerate(enemy_list):
        enemy_x, enemy_y, enemy_z = enemy
        diff_x = player_x - enemy_x
        diff_y = player_y - enemy_y
        distance = math.sqrt(diff_x**2 + diff_y**2)

        if distance > 10:
            if distance != 0:
                direction_x = diff_x / distance
                direction_y = diff_y / distance
            else:
                direction_x, direction_y = 0, 0

            new_x = enemy_x + direction_x * enemy_speed
            new_y = enemy_y + direction_y * enemy_speed

            # Prevent enemies from entering ANY house, cave, or merchant houses - stay within bounds
            # Enemies are NEVER allowed in ANY house, regardless of door state
            if (-GRID_LENGTH < new_x < GRID_LENGTH and -GRID_LENGTH < new_y < GRID_LENGTH
                and not check_house_collision(new_x, new_y) and not check_cave_collision(new_x, new_y)
                and not check_neighbor1_collision(new_x, new_y) and not check_neighbor2_collision(new_x, new_y)
                and not check_neighbor3_collision(new_x, new_y)):
                enemy_x = new_x
                enemy_y = new_y

        # Check collision with player
        player_radius = 15
        if collision_detector(enemy_x, enemy_y, enem_rad_bottom, player_x, player_y, player_radius):
            player_hit_count += 1
            if player_hit_count % 2 == 0:
                player_lives -= 1
                print(player_lives)
                print(f"Player Hit! Total contacts: {player_hit_count}")

            enemies_to_respawn.append(enemy_num)
        else:
            updated_enemies.append((enemy_x, enemy_y, enemy_z))

    #Selection sort in descending order
    for i in range(len(enemies_to_respawn)):
        max_idx = i
        for j in range(i+1, len(enemies_to_respawn)):
            if enemies_to_respawn[j] > enemies_to_respawn[max_idx]:
                max_idx = j
        # Swap
        enemies_to_respawn[i], enemies_to_respawn[max_idx] = enemies_to_respawn[max_idx], enemies_to_respawn[i]

    # Remove enemies safely
    for index in enemies_to_respawn:
        if index < len(enemy_list):
            enemy_list.pop(index)
            make_new_enemy()

    enemy_list = updated_enemies

def cheat_mode_behavior():
    global player_cam_angle, bullets_x, bullets_y, bullets_z, bullets_direction_x, bullets_direction_y, bullets_angle
    global enemy_list, imp_val, angle_hacks

    if not cheat_mode:
        return

    # Ensure at least 5 enemies
    while len(enemy_list) < 5:
        make_new_enemy()

    # Spin player continuously
    player_cam_angle = (player_cam_angle + 5) % 360

    # Gun tip coordinates
    angle_rad = math.radians(player_cam_angle)
    gun_length = 65
    bullet_start_x = player_x - math.sin(angle_rad) * gun_length
    bullet_start_y = player_y + math.cos(angle_rad) * gun_length
    direction_x = -math.sin(angle_rad)
    direction_y = math.cos(angle_rad)

    # Angle tolerance in radians

    # Initialize boolean list for this frame
    cheat_frame_fired = []

    # Find out how many enemies currently exist
    num_enemies = len(enemy_list)

    # Temporary variable for loop
    index = 0

    # Loop through each enemy and mark it as not fired
    while index < num_enemies:
        # Each enemy starts as not yet targeted
        fired_status = False

        # Append to the cheat_frame_fired list
        cheat_frame_fired.append(fired_status)

        # Reset temporary variable (redundant, just for verbosity)
        fired_status = None

        # Increment loop counter
        index += 1

    # Loop through all enemies
    enemy_num = 0
    while enemy_num < len(enemy_list):
        # Skip if already fired at this enemy this frame
        if cheat_frame_fired[enemy_num]:
            enemy_num += 1
            continue

        enemy_x, enemy_y, _ = enemy_list[enemy_num]

        # Vector from gun tip to enemy
        vec_x = enemy_x - bullet_start_x
        vec_y = enemy_y - bullet_start_y
        vec_length = math.sqrt(vec_x**2 + vec_y**2)

        # Skip if distance is zero
        if vec_length == 0:
            enemy_num += 1
            continue

        # Normalize vector
        vec_x /= vec_length
        vec_y /= vec_length

        # Calculate angle difference between gun direction and vector to enemy
        dot = direction_x * vec_x + direction_y * vec_y
        angle_diff = math.acos(max(min(dot, 1), -1))  # clamp dot to avoid math errors

        if angle_diff <= angle_hacks:
            # Fire only on every other frame
            if imp_val % 2 == 0:
                bullets_x.append(bullet_start_x)
                bullets_y.append(bullet_start_y)
                bullets_z.append(75)
                bullets_direction_x.append(direction_x)
                bullets_direction_y.append(direction_y)
                bullets_angle.append(player_cam_angle)
            imp_val += 1

            # Mark this enemy as fired at
            cheat_frame_fired[enemy_num] = True

            # Fire only one bullet per frame
            break

        enemy_num += 1


def draw_house(x, y, z):
    """Draw a house made of cubes with a bed inside"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # House dimensions
    house_width = 350
    house_depth = 350
    house_height = 200
    wall_thickness = 20

    # Draw house foundation/floor
    glPushMatrix()
    glTranslatef(0, 0, 5)
    glColor3f(0.6, 0.6, 0.6)  # Gray foundation
    glScalef(house_width, house_depth, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Draw house walls
    # Front wall
    glPushMatrix()
    glTranslatef(0, house_depth/2 - wall_thickness/2, house_height/2)
    glColor3f(0.8, 0.7, 0.5)  # Beige wall color
    glScalef(house_width, wall_thickness, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Back wall
    glPushMatrix()
    glTranslatef(0, -house_depth/2 + wall_thickness/2, house_height/2)
    glColor3f(0.8, 0.7, 0.5)  # Beige wall color
    glScalef(house_width, wall_thickness, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Left wall
    glPushMatrix()
    glTranslatef(-house_width/2 + wall_thickness/2, 0, house_height/2)
    glColor3f(0.8, 0.7, 0.5)  # Beige wall color
    glScalef(wall_thickness, house_depth - 2*wall_thickness, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Right wall
    glPushMatrix()
    glTranslatef(house_width/2 - wall_thickness/2, 0, house_height/2)
    glColor3f(0.8, 0.7, 0.5)  # Beige wall color
    glScalef(wall_thickness, house_depth - 2*wall_thickness, house_height)
    glutSolidCube(1)
    glPopMatrix()

    # Roof
    glPushMatrix()
    glTranslatef(0, 0, house_height + 15)
    glColor3f(0.6, 0.2, 0.1)  # Brown roof
    glScalef(house_width + 40, house_depth + 40, 30)
    glutSolidCube(1)
    glPopMatrix()

    # Door opening (cut from front wall)
    door_width = 100
    door_height = 150
    glPushMatrix()
    glTranslatef(house_width/3, house_depth/2 - wall_thickness/2, door_height/2)
    glColor3f(0.3, 0.2, 0.1)  # Dark brown door
    glScalef(door_width, wall_thickness + 2, door_height)
    glutSolidCube(1)
    glPopMatrix()

    # Window
    glPushMatrix()
    glTranslatef(-house_width/3, house_depth/2 - wall_thickness/2, house_height/2 + 20)
    glColor3f(0.7, 0.9, 1.0)  # Light blue window
    glScalef(50, wall_thickness + 2, 50)
    glutSolidCube(1)
    glPopMatrix()

    # Draw bed inside the house
    bed_x = -house_width/3
    bed_y = -house_depth/3
    bed_z = 30

    # Bed base
    glPushMatrix()
    glTranslatef(bed_x, bed_y, bed_z)
    glColor3f(0.5, 0.3, 0.1)  # Brown bed frame
    glScalef(120, 80, 20)
    glutSolidCube(1)
    glPopMatrix()

    # Mattress
    glPushMatrix()
    glTranslatef(bed_x, bed_y, bed_z + 15)
    glColor3f(0.9, 0.9, 0.9)  # White mattress
    glScalef(115, 75, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Pillow
    glPushMatrix()
    glTranslatef(bed_x, bed_y - 25, bed_z + 25)
    glColor3f(0.8, 0.8, 1.0)  # Light blue pillow
    glScalef(50, 25, 15)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


def draw_boss(x, y, z):
    """Draw the boss enemy with 2 horns"""
    if not boss_alive:
        return
   
    quad = gluNewQuadric()

    glPushMatrix()
    glTranslatef(x, y, z)
   
    if boss_standing:
        # Standing boss
        glTranslatef(0, 0, 40)  # Raise boss when standing
   
    # Boss body (larger than regular enemies)
    glColor3f(0.8, 0.1, 0.1)  # Dark red color
    glPushMatrix()
    glScalef(1.5, 1.5, 2.0)  # Make boss larger
    glutSolidSphere(30, 20, 20)
    glPopMatrix()
   
    # Boss head
    glColor3f(0.9, 0.2, 0.2)  # Slightly lighter red
    glPushMatrix()
    glTranslatef(0, 0, 50)
    glutSolidSphere(20, 15, 15)
    glPopMatrix()
   
    # Horn 1
    glColor3f(0.3, 0.3, 0.3)  # Dark gray horns
    glPushMatrix()
    glTranslatef(-10, 0, 65)
    glRotatef(-20, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 3, 0, 15, 8, 8)
    glPopMatrix()
   
    # Horn 2
    glPushMatrix()
    glTranslatef(10, 0, 65)
    glRotatef(20, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 3, 0, 15, 8, 8)
    glPopMatrix()
   
    # Eyes
    glColor3f(1.0, 0.0, 0.0)  # Red glowing eyes
    glPushMatrix()
    glTranslatef(-8, 15, 55)
    glutSolidSphere(2, 8, 8)
    glPopMatrix()
   
    glPushMatrix()
    glTranslatef(8, 15, 55)
    glutSolidSphere(2, 8, 8)
    glPopMatrix()
   
    glPopMatrix()

def update_boss():
    """Update boss behavior based on player position"""
    global boss_standing, boss_x, boss_y, boss_animation_timer, player_hit_count
   
    if not boss_alive:
        return
   
    # Check if player is in cave
    player_in_cave = is_inside_cave(player_x, player_y)
   
    if player_in_cave and not boss_standing:
        boss_standing = True
        print("Boss awakens!")
    elif not player_in_cave:
        boss_standing = False
   
    # Boss movement when standing
    if boss_standing:
        # Move boss towards player
        diff_x = player_x - boss_x
        diff_y = player_y - boss_y
        distance = math.sqrt(diff_x**2 + diff_y**2)
       
        if distance > 5:  # Don't move if too close
            if distance != 0:
                direction_x = diff_x / distance
                direction_y = diff_y / distance
               
                # Boss moves slower than regular enemies
                boss_speed = 0.5
                new_x = boss_x + direction_x * boss_speed
                new_y = boss_y + direction_y * boss_speed
               
                # Keep boss within cave bounds
                cave_x = -2500
                cave_y = -2500
                cave_width = 1000
                cave_depth = 1000
               
                if (new_x >= cave_x - cave_width/2 and new_x <= cave_x + cave_width/2 and
                    new_y >= cave_y - cave_depth/2 and new_y <= cave_y + cave_depth/2):
                    boss_x = new_x
                    boss_y = new_y
       
        # Check boss-player collision
        # Calculate actual boss z position (boss stands up when player enters cave)
        actual_boss_z = boss_z + (40 if boss_standing else 0)
        if collision_detector_3d(player_x, player_y, player_z, 20, boss_x, boss_y, actual_boss_z, 50):
            player_hit_count += 1
            print("Boss touched player! Game Over!")

def draw_cave(x, y, z):
    """Draw a large cave with crystals, mushrooms, and rocks"""
    glPushMatrix()
    glTranslatef(x, y, z)

    # Cave dimensions - much larger
    cave_width = 1000
    cave_depth = 1000
    cave_height = 300

    # Draw cave floor - dark grey stone
    glPushMatrix()
    glTranslatef(0, 0, 5)
    glColor3f(0.15, 0.15, 0.15)  # Dark grey floor
    glScalef(cave_width, cave_depth, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Draw cave walls - solid walls
    wall_thickness = 40
    # Back wall
    glPushMatrix()
    glTranslatef(0, -cave_depth/2, cave_height/2)
    glColor3f(0.1, 0.1, 0.1)
    glScalef(cave_width, wall_thickness, cave_height)
    glutSolidCube(1)
    glPopMatrix()

    # Left wall
    glPushMatrix()
    glTranslatef(-cave_width/2, 0, cave_height/2)
    glColor3f(0.1, 0.1, 0.1)
    glScalef(wall_thickness, cave_depth, cave_height)
    glutSolidCube(1)
    glPopMatrix()

    # Right wall
    glPushMatrix()
    glTranslatef(cave_width/2, 0, cave_height/2)
    glColor3f(0.1, 0.1, 0.1)
    glScalef(wall_thickness, cave_depth, cave_height)
    glutSolidCube(1)
    glPopMatrix()

    # Front wall with opening
    opening_width = 100
    # Left part of front wall
    glPushMatrix()
    glTranslatef(-cave_width/4 - opening_width/4, cave_depth/2, cave_height/2)
    glColor3f(0.1, 0.1, 0.1)
    glScalef(cave_width/2 - opening_width/2, wall_thickness, cave_height)
    glutSolidCube(1)
    glPopMatrix()

    # Right part of front wall
    glPushMatrix()
    glTranslatef(cave_width/4 + opening_width/4, cave_depth/2, cave_height/2)
    glColor3f(0.1, 0.1, 0.1)
    glScalef(cave_width/2 - opening_width/2, wall_thickness, cave_height)
    glutSolidCube(1)
    glPopMatrix()

    # Top part of front wall
    glPushMatrix()
    glTranslatef(0, cave_depth/2, cave_height - 40)
    glColor3f(0.1, 0.1, 0.1)
    glScalef(opening_width, wall_thickness, 80)
    glutSolidCube(1)
    glPopMatrix()

    # Cave ceiling
    glPushMatrix()
    glTranslatef(0, 0, cave_height)
    glColor3f(0.2, 0.2, 0.2)
    glScalef(cave_width, cave_depth, wall_thickness)
    glutSolidCube(1)
    glPopMatrix()

    # Add CRYSTALS - various colors and sizes
    crystal_positions = [
        (-150, -150, 30, 0.8, 0.2, 1.0),  # Purple crystal
        (100, -100, 35, 0.2, 0.8, 1.0),   # Cyan crystal
        (-50, 120, 25, 1.0, 0.3, 0.8),    # Pink crystal
        (120, 80, 40, 0.3, 1.0, 0.3),     # Green crystal
        (-120, 50, 28, 1.0, 1.0, 0.2),    # Yellow crystal
        (50, -150, 32, 1.0, 0.5, 0.0),    # Orange crystal
        (-80, -80, 38, 0.5, 0.2, 1.0),    # Blue-purple crystal
        (150, 150, 30, 1.0, 0.2, 0.2),    # Red crystal
    ]

    for cx, cy, cz, r, g, b in crystal_positions:
        # Crystal base
        glPushMatrix()
        glTranslatef(cx, cy, cz)
        glColor3f(r, g, b)
        glScalef(20, 20, 50)
        glutSolidCube(1)
        glPopMatrix()

        # Crystal tip
        glPushMatrix()
        glTranslatef(cx, cy, cz + 35)
        glColor3f(r + 0.2, g + 0.2, b + 0.2)  # Slightly brighter tip
        glScalef(15, 15, 20)
        glutSolidCube(1)
        glPopMatrix()

    # Add MUSHROOMS - various sizes and colors
    mushroom_positions = [
        (-100, 0, 15, 0.8, 0.4, 0.2),     # Brown mushroom
        (30, 50, 12, 0.9, 0.1, 0.1),      # Red mushroom
        (-30, -50, 18, 0.6, 0.3, 0.8),    # Purple mushroom
        (80, -30, 10, 0.2, 0.8, 0.2),     # Green mushroom
        (-60, 90, 20, 1.0, 0.8, 0.0),     # Yellow mushroom
        (110, 20, 14, 0.9, 0.5, 0.1),     # Orange mushroom
    ]

    for mx, my, stem_height, r, g, b in mushroom_positions:
        # Mushroom stem
        glPushMatrix()
        glTranslatef(mx, my, stem_height/2)
        glColor3f(0.9, 0.9, 0.8)  # Light stem color
        glScalef(8, 8, stem_height)
        glutSolidCube(1)
        glPopMatrix()

        # Mushroom cap
        glPushMatrix()
        glTranslatef(mx, my, stem_height + 8)
        glColor3f(r, g, b)
        gluSphere(gluNewQuadric(), 15, 12, 12)
        glPopMatrix()

        # Mushroom spots (for some mushrooms)
        if r > 0.8:  # Red mushrooms get white spots
            for spot in range(4):
                spot_angle = spot * 90
                spot_x = mx + 10 * math.cos(math.radians(spot_angle))
                spot_y = my + 10 * math.sin(math.radians(spot_angle))
                glPushMatrix()
                glTranslatef(spot_x, spot_y, stem_height + 12)
                glColor3f(1.0, 1.0, 1.0)  # White spots
                gluSphere(gluNewQuadric(), 3, 6, 6)
                glPopMatrix()

    # Add ROCKS - various sizes scattered around
    rock_positions = [
        (60, 120, 25, 30),   # Large rock
        (-140, 100, 15, 20), # Medium rock
        (140, -120, 20, 25), # Medium-large rock
        (-20, -120, 12, 15), # Small rock
        (90, 60, 18, 22),    # Medium rock
        (-90, -30, 10, 18),  # Small rock
        (20, -80, 22, 28),   # Large rock
        (-110, -90, 16, 20), # Medium rock
        (130, 40, 14, 19),   # Small-medium rock
    ]

    for rx, ry, rz, size in rock_positions:
        glPushMatrix()
        glTranslatef(rx, ry, rz)
        # Vary rock colors from dark grey to brown
        rock_shade = (size % 10) / 10.0
        glColor3f(0.3 + rock_shade * 0.2, 0.25 + rock_shade * 0.15, 0.2 + rock_shade * 0.1)

        # Make rocks slightly irregular by scaling differently on each axis
        scale_x = size + (size % 3) * 2
        scale_y = size + (size % 5) * 1.5
        scale_z = size + (size % 7) * 1
        glScalef(scale_x, scale_y, scale_z)
        glutSolidCube(1)
        glPopMatrix()

    # Add BLACK BIG ROCKS - large dark rocks scattered around cave
    black_rock_positions = [
        (-180, -100, 40, 60),   # Extra large black rock
        (120, 150, 35, 55),     # Large black rock
        (-80, 180, 45, 65),     # Extra large black rock
        (180, -80, 30, 50),     # Large black rock
        (-120, -180, 50, 70),   # Huge black rock
        (80, -150, 25, 45),     # Medium-large black rock
        (-200, 120, 40, 60),    # Extra large black rock
    ]

    for brx, bry, brz, size in black_rock_positions:
        glPushMatrix()
        glTranslatef(brx, bry, brz)
        # Very dark black/charcoal color
        glColor3f(0.1, 0.1, 0.1)  # Almost black
       
        # Make rocks irregular and imposing
        scale_x = size + (size % 4) * 3
        scale_y = size + (size % 6) * 2
        scale_z = size + (size % 8) * 1.5
        glScalef(scale_x, scale_y, scale_z)
        glutSolidCube(1)
        glPopMatrix()

    # Add LAVA BLOCKS - red glowing blocks scattered around cave
    lava_positions = [
        (-200, -200, 25, 40),  # Large lava block
        (150, -150, 20, 35),   # Medium lava block
        (-100, 150, 30, 45),   # Large lava block
        (200, 100, 15, 30),    # Small lava block
        (-50, -100, 25, 40),   # Medium lava block
        (100, 200, 20, 35),    # Medium lava block
        (-150, 0, 35, 50),     # Extra large lava block
        (50, -200, 18, 32),    # Small-medium lava block
    ]

    for lx, ly, lz, size in lava_positions:
        glPushMatrix()
        glTranslatef(lx, ly, lz)
        # Bright red lava color with slight glow effect
        glColor3f(1.0, 0.2, 0.0)  # Bright red-orange
        glScalef(size, size, size * 0.8)  # Slightly flattened blocks
        glutSolidCube(1)
        glPopMatrix()
       
        # Add a brighter core for glow effect
        glPushMatrix()
        glTranslatef(lx, ly, lz + 5)
        glColor3f(1.0, 0.4, 0.1)  # Brighter orange core
        glScalef(size * 0.7, size * 0.7, size * 0.6)
        glutSolidCube(1)
        glPopMatrix()

    # Add some stalactites hanging from ceiling
    for i in range(8):
        stalactite_x = -cave_width/3 + (i * cave_width/8)
        stalactite_y = -cave_depth/4 + ((i % 3) * cave_depth/3)
        glPushMatrix()
        glTranslatef(stalactite_x, stalactite_y, cave_height - 30)
        glColor3f(0.05, 0.05, 0.05)  # Almost black
        glScalef(12, 12, 60)
        glutSolidCube(1)
        glPopMatrix()

    # Add SILVER BATS floating attached to ceiling
    global bat_animation_timer, bat_wing_angle
    bat_animation_timer += 1
    bat_wing_angle = math.sin(bat_animation_timer * 0.3) * 30  # Wing flapping animation
   
    bat_positions = [
        (-150, -80, cave_height - 40, 0),    # Bat 1
        (100, 120, cave_height - 35, 45),   # Bat 2
        (-200, 150, cave_height - 45, 90),  # Bat 3
        (180, -120, cave_height - 38, 135), # Bat 4
        (-80, 200, cave_height - 42, 180),  # Bat 5
        (50, -180, cave_height - 36, 225),  # Bat 6
    ]
   
    for bx, by, bz, rotation in bat_positions:
        glPushMatrix()
        glTranslatef(bx, by, bz)
        glRotatef(rotation, 0, 0, 1)  # Rotate bat for variety
       
        # Bat body (silver/gray)
        glColor3f(0.7, 0.7, 0.8)  # Silver color
        glScalef(8, 12, 6)
        glutSolidCube(1)
        glPopMatrix()
       
        # Bat head
        glPushMatrix()
        glTranslatef(bx, by + 8, bz + 2)
        glRotatef(rotation, 0, 0, 1)
        glColor3f(0.6, 0.6, 0.7)  # Slightly darker silver
        gluSphere(gluNewQuadric(), 4, 8, 8)
        glPopMatrix()
       
        # Left wing
        glPushMatrix()
        glTranslatef(bx - 12, by, bz)
        glRotatef(rotation + bat_wing_angle, 0, 0, 1)
        glColor3f(0.5, 0.5, 0.6)  # Dark silver for wings
        glScalef(15, 8, 2)
        glutSolidCube(1)
        glPopMatrix()
       
        # Right wing
        glPushMatrix()
        glTranslatef(bx + 12, by, bz)
        glRotatef(rotation - bat_wing_angle, 0, 0, 1)
        glColor3f(0.5, 0.5, 0.6)  # Dark silver for wings
        glScalef(15, 8, 2)
        glutSolidCube(1)
        glPopMatrix()
       
        # Bat eyes (small red dots)
        glPushMatrix()
        glTranslatef(bx - 2, by + 10, bz + 3)
        glRotatef(rotation, 0, 0, 1)
        glColor3f(1.0, 0.2, 0.2)  # Red eyes
        gluSphere(gluNewQuadric(), 1, 4, 4)
        glPopMatrix()
       
        glPushMatrix()
        glTranslatef(bx + 2, by + 10, bz + 3)
        glRotatef(rotation, 0, 0, 1)
        glColor3f(1.0, 0.2, 0.2)  # Red eyes
        gluSphere(gluNewQuadric(), 1, 4, 4)
        glPopMatrix()

    glPopMatrix()


def initialize_clouds():
    global cloud_positions
    cloud_positions = []
    for _ in range(20):
        x = random.uniform(-2000, 2000)
        y = random.uniform(-2000, 2000)
        z = random.uniform(500, 700)
        color = random.choice([(0.9, 0.9, 1.0), (0.8, 0.8, 1.0), (1.0, 1.0, 1.0)])

        spheres = []
        for _ in range(6):
            x_offset = (random.random() - 0.5) * 100
            y_offset = (random.random() - 0.5) * 100
            z_offset = (random.random() - 0.5) * 20
            radius = 30 + random.random() * 20
            spheres.append({'offset': [x_offset, y_offset, z_offset], 'radius': radius})

        cloud_positions.append({'pos': [x, y, z], 'color': color, 'spheres': spheres})

def draw_clouds():
    for cloud in cloud_positions:
        glPushMatrix()
        glTranslatef(cloud['pos'][0], cloud['pos'][1], cloud['pos'][2])
        glColor3f(cloud['color'][0], cloud['color'][1], cloud['color'][2])
        for sphere in cloud['spheres']:
            glPushMatrix()
            glTranslatef(sphere['offset'][0], sphere['offset'][1], sphere['offset'][2])
            glutSolidSphere(sphere['radius'], 20, 20)
            glPopMatrix()
        glPopMatrix()


def draw_shapes():
    """Draw all game shapes including enemies and player"""
    global player_x, player_y, player_z, player_cam_angle, enem_rad_top, enem_rad_bottom, enem_growing, game_over

    # Update and draw boss
    update_boss()
    if boss_alive:
        draw_boss(boss_x, boss_y, boss_z)

    # Only maintain 5 enemies if not game over
    if not game_over:
        if is_day:
            enemy_list.clear() # Despawn all enemies during the day
        else:
            while len(enemy_list) < 5:
                make_new_enemy()

    # Rearrange world objects according to user's drawing
    # Trees positioned around the expanded map (3000x3000 grid) - removed trees inside enlarged houses
    tree_positions = [
        (-1200, 1200, 0),   # Far top-left
        (-300, 1300, 0),    # Top area
        (300, 1400, 0),     # Top area
        (-1400, 800, 0),    # Far left side
        (-1200, 300, 0),    # Left side
        (-1100, -300, 0),   # Left side
        (-1300, -800, 0),   # Far left bottom
        (-300, -1200, 0),   # Bottom area
        (300, -1300, 0),    # Bottom area
        (1400, -800, 0),    # Far right bottom
        (1200, -300, 0),    # Right side
        (1300, 300, 0),     # Right side
        (1400, 800, 0),     # Far right side
        (-1200, -300, 0),   # Left side (moved away from houses)
        (1200, 300, 0),     # Right side (moved away from houses)
        (-1100, 600, 0),    # Left-top area (moved away from neighbor1)
        (1100, 600, 0),     # Right-top area (moved away from neighbor2)
        (-1100, -1100, 0),  # Left-bottom area (moved away from main house)
        (1100, -1100, 0),   # Right-bottom area (moved away from neighbor3)
        # Additional trees
        (-1500, 1500, 0),   # Far corners
        (1500, 1500, 0),
        (-1500, -1500, 0),
        (1500, -1500, 0),
        (-800, 1500, 0),    # More top area
        (0, 1500, 0),
        (800, 1500, 0),
        (-1500, 0, 0),      # More side areas
        (1500, 0, 0),
        (-800, -1500, 0),   # More bottom area
        (0, -1500, 0),
        (800, -1500, 0),
        (-600, 900, 0),     # Fill in gaps
        (600, 900, 0),
        (-900, 600, 0),
        (900, 600, 0),
        (-600, -900, 0),
        (600, -900, 0),
        (-900, -600, 0),
        (900, -600, 0),
    ]

    # (SAMANIA): CODE FOR SEASONAL TREES
    #  leaf color palette for the current season
    leaf_color_palette = season_leaf_colors.get(current_season, [])


    for tree_x, tree_y, tree_z in tree_positions:
        # Enhanced tree with many branches and varied leaf clusters
        glPushMatrix()
        glTranslatef(tree_x, tree_y, tree_z)

        trunk_length = 200
        trunk_radius = 10
        leaf_radius = 35  # Smaller base leaf size

        # Draw trunk (solid cylinder)
        glColor3f(0.55, 0.27, 0.07)  # Brown
        quadric = gluNewQuadric()
        gluCylinder(quadric, trunk_radius, trunk_radius * 0.6, trunk_length, 24, 24)


        # (SAMANIA): CODE FOR SEASONAL TREES (LEAF RENDERING LOGIC)

        # Only draw leaves if it is not winter
        if len(leaf_color_palette) > 0:
        # ===================================
            # Draw fewer layers of branches for simpler trees
            branch_levels = 3  # Reduced number of vertical levels
            branch_count = 8  # Reduced base number of branches
            for level in range(branch_levels):
                level_height = trunk_length * (0.5 + level * 0.2)  # Different heights for each level
                branches_per_level = branch_count - level * 2  # Fewer branches at higher levels
                level_branch_length = trunk_length * (0.6 - level * 0.05)  # Longer branches for more spread

                for i in range(branches_per_level):
                    angle = 360.0 * i / branches_per_level
                    # Add more randomness to branch angles for natural look
                    angle_variation = (i % 5) * 20 - 40  # Varies between -40 and 40 degrees
                    final_angle = angle + angle_variation

                    glPushMatrix()
                    # Move to branch attachment point on trunk
                    glTranslatef(0, 0, level_height)
                    glRotatef(final_angle, 0, 0, 1)  # Spread branches around Z
                    glRotatef(20 + level * 8, 1, 0, 0)  # Tilt upward, more for higher levels

                    # Draw branch (solid cylinder)
                    glColor3f(0.4, 0.3, 0.1)
                    branch_radius = trunk_radius * (0.25 - level * 0.03)
                    branch_quad = gluNewQuadric()
                    gluCylinder(branch_quad, branch_radius, branch_radius * 0.3, level_branch_length, 12, 12)

                    # Draw multiple leaf clusters at end of branch for more spread
                    glTranslatef(0, 0, level_branch_length)

                    # Create 2-3 leaf clusters per branch tip for simpler appearance
                    num_leaf_clusters = 2 + (i % 2)  # 2-3 clusters per branch
                    for cluster in range(num_leaf_clusters):
                        glPushMatrix()

                        # Spread leaf clusters around the branch tip
                        cluster_angle = (360.0 * cluster / num_leaf_clusters) + (i * 13)  # Offset for variation
                        cluster_distance = leaf_radius * 0.8  # How far from branch tip

                        # Position each leaf cluster
                        cluster_x = math.cos(math.radians(cluster_angle)) * cluster_distance
                        cluster_y = math.sin(math.radians(cluster_angle)) * cluster_distance
                        cluster_z = -leaf_radius * 0.3 + (cluster % 2) * leaf_radius * 0.6  # Vertical spread

                        glTranslatef(cluster_x, cluster_y, cluster_z)

                        # Vary leaf size and color based on branch level and position
                        size_variation = 0.6 + (cluster % 3) * 0.3  # Size varies from 0.6 to 1.2
                        current_leaf_radius = leaf_radius * size_variation * (1.2 - level * 0.1)


                        # (SAMANIA): MODIFICATION FOR SEASONAL LEAF COLOR

                        # dynamic seasonal palette.
                        green_variations = leaf_color_palette


                        green_color = green_variations[(i + cluster) % len(green_variations)]
                        glColor3f(green_color[0], green_color[1], green_color[2])

                        leaf_quad = gluNewQuadric()
                        gluSphere(leaf_quad, current_leaf_radius, 20, 20)

                        glPopMatrix()

                    glPopMatrix()

            # Add a large top leaf cluster with multiple spheres
            for top_cluster in range(4):
                glPushMatrix()
                cluster_angle = 90.0 * top_cluster
                cluster_radius = leaf_radius * 0.6
                top_x = math.cos(math.radians(cluster_angle)) * cluster_radius
                top_y = math.sin(math.radians(cluster_angle)) * cluster_radius
                top_z = trunk_length + leaf_radius * (0.2 + top_cluster * 0.1)

                glTranslatef(top_x, top_y, top_z)

                # (samania new): MODIFICATION FOR SEASONAL LEAF COLOR

                # dynamic seasonal palette.
                green_variations = leaf_color_palette

                top_green_color = green_variations[(i + top_cluster) % len(green_variations)]
                glColor3f(*top_green_color)
                top_leaf_quad = gluNewQuadric()
                gluSphere(top_leaf_quad, leaf_radius * (1.2 + top_cluster * 0.2), 24, 24)
                glPopMatrix()

        glPopMatrix()

    # Draw the house in bottom-left corner (opposite from cave)
    house_x = -800  # Bottom-left corner
    house_y = -800  # Bottom-left corner
    draw_house(house_x, house_y, 0)

    # Draw the large cave in bottom-left corner with crystals, mushrooms, and rocks
    cave_x = -2500   # Bottom-left corner
    cave_y = -2500
    draw_cave(cave_x, cave_y, 0)

    # Draw neighbor houses with their features
    # Neighbor 1 (top-left): Chicken coop
    draw_neighbor_house(neighbor1_x, neighbor1_y, 0, (0.9, 0.8, 0.6))  # Light yellow house
    draw_merchant(merchant1_x, merchant1_y, merchant1_angle)  # Merchant inside house 1
    draw_chicken_coop(neighbor1_x - 50, neighbor1_y - 50, 0)

    # Neighbor 2 (top-right): Cow and milk cans
    draw_neighbor_house(neighbor2_x, neighbor2_y, 0, (0.8, 0.9, 0.7))  # Light green house
    draw_merchant(merchant2_x, merchant2_y, merchant2_angle)  # Merchant inside house 2
    draw_cow(neighbor2_x - 30, neighbor2_y - 30, 0)
    draw_milk_cans(neighbor2_x + 40, neighbor2_y - 60, 0)

    # Neighbor 3 (bottom-right): Apple trees and basket
    draw_neighbor_house(neighbor3_x, neighbor3_y, 0, (0.9, 0.7, 0.8))  # Light pink house
    draw_merchant(merchant3_x, merchant3_y, merchant3_angle)  # Merchant inside house 3 (now carrying basket)
    # Move apple trees outside the house boundaries
    draw_apple_tree(neighbor3_x - 300, neighbor3_y + 250, 0)  # Far left from house
    draw_apple_tree(neighbor3_x + 250, neighbor3_y - 300, 0)  # Far right from house
    draw_apple_tree(neighbor3_x + 300, neighbor3_y + 300, 0)  # Far top-right from house

    # Draw all enemies - only if not game over
    if not game_over:
        for enemy in enemy_list:
            enemy_x, enemy_y, enemy_z = enemy
            glPushMatrix()
            glTranslatef(enemy_x, enemy_y, enemy_z)

            # Zombie body (torso) - pale sickly green
            glColor3f(0.4, 0.5, 0.3) # Pale sickly green
            gluSphere(gluNewQuadric(), enem_rad_bottom, 20, 20)

            # Zombie arms - hanging down
            glPushMatrix()
            glTranslatef(-enem_rad_bottom * 0.8, 0, enem_rad_bottom * 0.5)
            glRotatef(-30, 1, 0, 0)  # Slightly forward hanging
            glColor3f(0.3, 0.4, 0.2) # Darker zombie skin
            gluCylinder(gluNewQuadric(), 5, 3, enem_rad_bottom * 0.8, 8, 8)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(enem_rad_bottom * 0.8, 0, enem_rad_bottom * 0.5)
            glRotatef(-30, 1, 0, 0)  # Slightly forward hanging
            glColor3f(0.3, 0.4, 0.2) # Darker zombie skin
            gluCylinder(gluNewQuadric(), 5, 3, enem_rad_bottom * 0.8, 8, 8)
            glPopMatrix()

            # Zombie legs - standing
            glPushMatrix()
            glTranslatef(-enem_rad_bottom * 0.4, 0, -enem_rad_bottom * 0.8)
            glColor3f(0.2, 0.3, 0.1) # Dark zombie leg color
            gluCylinder(gluNewQuadric(), 8, 6, enem_rad_bottom * 0.8, 8, 8)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(enem_rad_bottom * 0.4, 0, -enem_rad_bottom * 0.8)
            glColor3f(0.2, 0.3, 0.1) # Dark zombie leg color
            gluCylinder(gluNewQuadric(), 8, 6, enem_rad_bottom * 0.8, 8, 8)
            glPopMatrix()

            # Move up for zombie head
            glTranslatef(0, 0, enem_rad_bottom)
            # Zombie head - pale decaying skin
            glColor3f(0.35, 0.45, 0.25) # Pale decaying green
            gluSphere(gluNewQuadric(), enem_rad_top, 20, 20)

            # Zombie eyes - bright red glowing
            glPushMatrix()
            glTranslatef(-enem_rad_top * 0.3, enem_rad_top * 0.7, enem_rad_top * 0.2)
            glColor3f(1.0, 0.0, 0.0) # Bright red eyes
            gluSphere(gluNewQuadric(), 3, 8, 8)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(enem_rad_top * 0.3, enem_rad_top * 0.7, enem_rad_top * 0.2)
            glColor3f(1.0, 0.0, 0.0) # Bright red eyes
            gluSphere(gluNewQuadric(), 3, 8, 8)
            glPopMatrix()

            glPopMatrix()

    glPushMatrix()
    # Move and rotate the entire player
    glTranslatef(player_x, player_y, player_z)  # Base position with jump height
    glRotatef(player_cam_angle, 0, 0, 1)

    # Apply death rotation if game over
    if game_over:
        glRotatef(death_rotation, 1, 0, 0)  # Rotate around X-axis to fall

    # --- BODY ---
    glPushMatrix()
    glTranslatef(0, 0, 60)  # body center above ground
    glColor3f(0.2, 0.6, 1.0)  # Nice blue color for body
    draw_scaled_cuboid(50, 20, 60)
    glPopMatrix()

    # --- LEFT LEG ---
    glPushMatrix()
    glTranslatef(-15, 0, 0)  # relative to body
    glColor3f(0.4, 0.2, 0.8)  # Purple color for legs
    gluCylinder(gluNewQuadric(), 5, 10, 40, 20, 20)
    glPopMatrix()

    # --- RIGHT LEG ---
    glPushMatrix()
    glTranslatef(15, 0, 0)
    glColor3f(0.4, 0.2, 0.8)  # Purple color for legs
    gluCylinder(gluNewQuadric(), 5, 10, 40, 20, 20)
    glPopMatrix()

    # --- LEFT SHOE ---
    glPushMatrix()
    glTranslatef(-15, 0, -5)  # At the bottom of left leg
    glColor3f(0.1, 0.1, 0.1)  # Black shoes
    draw_scaled_cuboid(15, 25, 8)
    glPopMatrix()

    # --- RIGHT SHOE ---
    glPushMatrix()
    glTranslatef(15, 0, -5)  # At the bottom of right leg
    glColor3f(0.1, 0.1, 0.1)  # Black shoes
    draw_scaled_cuboid(15, 25, 8)
    glPopMatrix()

    # --- LEFT ARM ---
    glPushMatrix()
    glTranslatef(-15, 0, 75)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1.0, 0.8, 0.6)  # Skin color for arms
    gluCylinder(gluNewQuadric(), 7, 5, 35, 20, 20)
    glPopMatrix()

    # --- SWORD (positioned at hands with rotation) ---
    if current_weapon == "sword":
        if camera_mode == 2:  # First person mode - draw sword at hand position
            # Draw sword within player's transformation matrix so it moves with player
            # Save current matrix state
            glPushMatrix()

            # Position sword at center between hands
            glTranslatef(0, 0, 75)  # Center position at hand height
            glTranslatef(0, 40, 0)  # Forward position

            # Rotate sword based on sword_rotation
            if sword_rotation == 0:
                # Handle at right hand, blade extends to left
                glRotatef(0, 0, 0, 1)  # No rotation
                glTranslatef(15, 0, 0)  # Offset to right hand
            else:
                # Handle at left hand, blade extends to right
                glRotatef(180, 0, 0, 1)  # Rotate 180 degrees around Z axis
                glTranslatef(-15, 0, 0)  # Offset to left hand

            glRotatef(90, 0, 1, 0)  # Rotate to be horizontal

            # Draw sword with handle and blade
            # Handle
            glColor3f(0.4, 0.2, 0.1)  # Brown handle
            gluCylinder(gluNewQuadric(), 5, 5, 15, 20, 20)  # Draw handle

            # Blade
            glTranslatef(0, 0, 15)  # Move to end of handle
            glColor3f(0.75, 0.75, 0.75)  # Silver blade
            gluCylinder(gluNewQuadric(), 5, 2, 65, 20, 20)  # Draw tapered blade

            # Restore matrix state
            glPopMatrix()

            if game_over:
                glRotatef(death_rotation, 1, 0, 0)
        else:  # Third person or top view - draw sword at hand position
            glPushMatrix()
            # Position sword at center between hands
            glTranslatef(0, 0, 75)  # Center position at hand height

            # Rotate sword based on sword_rotation
            if sword_rotation == 0:
                # Handle at right hand, blade extends to left
                glRotatef(0, 0, 0, 1)  # No rotation
                glTranslatef(15, 0, 0)  # Offset to right hand
            else:
                # Handle at left hand, blade extends to right
                glRotatef(180, 0, 0, 1)  # Rotate 180 degrees around Z axis
                glTranslatef(-15, 0, 0)  # Offset to left hand

            glRotatef(90, 0, 1, 0)  # Rotate to be horizontal

            # Draw sword with handle and blade
            # Handle
            glColor3f(0.4, 0.2, 0.1)  # Brown handle
            gluCylinder(gluNewQuadric(), 5, 5, 15, 20, 20)  # Draw handle

            # Blade
            glTranslatef(0, 0, 15)  # Move to end of handle
            glColor3f(0.75, 0.75, 0.75)  # Silver blade
            gluCylinder(gluNewQuadric(), 5, 2, 65, 20, 20)  # Draw tapered blade

            glPopMatrix()

    # --- RIGHT ARM + GUN ---
    glPushMatrix()
    glTranslatef(15, 0, 75)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1.0, 0.8, 0.6)  # Skin color for arms
    gluCylinder(gluNewQuadric(), 7, 5, 35, 20, 20)

    # WEAPON LOGIC
    if current_weapon == "gun":
        glPushMatrix() # Save current matrix for gun
        glTranslatef(-15, 0, 0)  # Move to gun position
        glColor3f(0.5, 0.3, 0.1) # Wood color for gun body
        gluCylinder(gluNewQuadric(), 10, 3, 80, 20, 20) # Main gun body, larger

        # Add a scope
        glPushMatrix() # Save matrix for scope
        glTranslatef(0, 7, 40) # Position scope on top of gun body
        glRotatef(90, 1, 0, 0) # Rotate to be horizontal
        glColor3f(0.0, 0.0, 0.0) # Black color for scope
        gluCylinder(gluNewQuadric(), 3, 3, 20, 10, 10) # Scope cylinder, larger
        glPopMatrix() # Restore matrix for gun body

        # Add a barrel
        glPushMatrix() # Save matrix for barrel
        glTranslatef(0, 0, 80) # Position barrel at the end of the gun body
        glColor3f(0.0, 0.0, 0.0) # Black color for barrel
        gluCylinder(gluNewQuadric(), 2, 2, 25, 10, 10) # Barrel cylinder, larger
        glPopMatrix() # Restore matrix for gun body

        glPopMatrix() # Restore matrix for right arm
    elif current_weapon == "fishing_rod":
        # Fishing Rod
        glTranslatef(0, 0, 20)
        glRotatef(45, 1, 0, 0)
        glColor3f(0.5, 0.35, 0.05)
        gluCylinder(gluNewQuadric(), 2, 2, 150, 10, 10)
        # Fishing line
        glPushMatrix()
        glTranslatef(0, 0, 150)
        glColor3f(0.8, 0.8, 0.8)
        glLineWidth(1)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 20, -20)
        glEnd()
        glPopMatrix()

    glPopMatrix()

    # --- HEAD OR SPHERE ---
    glPushMatrix()
    glTranslatef(0, 0, 100)  # top of body
    glColor3f(1.0, 0.8, 0.6)  # Skin color for head
    gluSphere(gluNewQuadric(), 15, 10, 10)
    glPopMatrix()

    # --- HAT ---
    glPushMatrix()
    glTranslatef(0, 0, 115)  # On top of head
    glColor3f(0.8, 0.1, 0.1)  # Red hat
    gluCylinder(gluNewQuadric(), 18, 12, 15, 20, 20)  # Hat cylinder
    # Hat brim
    glTranslatef(0, 0, -2)
    glColor3f(0.6, 0.05, 0.05)  # Darker red for brim
    gluCylinder(gluNewQuadric(), 22, 22, 3, 20, 20)
    glPopMatrix()

    glPopMatrix()  # End player transformations

    # Draw bullets separately (outside player transformations)
    for i in range(len(bullets_x)):
        glPushMatrix()
        glTranslatef(bullets_x[i], bullets_y[i], bullets_z[i])
        glColor3f(1, 0, 0)  # Red bullet
        glRotatef(bullets_angle[i], 0, 0, 1)  # Rotate bullet to match firing direction
        glutSolidCube(20)  # Small cube as bullet
        glPopMatrix()

def keyboardListener(key, x, y):
    """Handle keyboard input"""
    global player_x, player_y, player_z, player_cam_angle, game_over, score, enemy_list, bullets_x, bullets_y, bullets_z
    global bullets_direction_x, bullets_direction_y, bullets_angle, missed, cheat_mode, cam_spinner, first_person
    global player_lives, player_hit_count, death_rotation, is_jumping, jump_velocity, jump_speed, move_speed, current_weapon, is_sprinting

    # (samania new): ## MODIFIED ## - ADDED player_stamina to globals  

    global day_night_target, player_stamina

    # Don't allow movement if game over
    if game_over and key != b'r':
        return

    if player_cam_angle < 0:
        player_cam_angle += 360
    if player_cam_angle >= 360:
        player_cam_angle = 0

    if key == b'r':
        player_x = 0
        player_y = 0
        player_z = 0
        score = 0
        player_lives = 5
        player_hit_count = 0
        death_rotation = 0
        is_jumping = False
        jump_velocity = 0
        current_weapon = "gun"
        is_sprinting = False
        player_stamina = 100.0
        enemy_list = []
        game_over = False
        print("Game reset!")

    if key == b'z':
        if current_weapon == "gun":
            current_weapon = "sword"
            print("Switched to Sword")
        elif current_weapon == "sword":
            current_weapon = "gun"
            print("Switched to Gun")
        else:
            current_weapon = "gun"
            print("Switched to Gun")

    if key == b'w':  # Move forward
        if player_stamina > 0: # Cannot move if stamina is zero
            player_cam_angle_rad = math.radians(player_cam_angle)
            dx = -math.sin(player_cam_angle_rad) * move_speed
            dy = math.cos(player_cam_angle_rad) * move_speed
            new_x = player_x + dx
            new_y = player_y + dy

            # Check door collision and house entry
            if check_door_collision(new_x, new_y):
                open_door()

            # Only allow movement if position is valid
            if can_move_to_position(new_x, new_y):
                player_x = new_x
                player_y = new_y
                # Decrease stamina for W movement
                player_stamina -= STAMINA_DRAIN_RATE
                player_stamina = max(0, player_stamina)

    if key == b's':  # Move backward
        if player_stamina > 0: # Cannot move if stamina is zero
            player_cam_angle_rad = math.radians(player_cam_angle)
            dx = -math.sin(player_cam_angle_rad) * move_speed
            dy = math.cos(player_cam_angle_rad) * move_speed
            new_x = player_x - dx
            new_y = player_y - dy

            # Check door collision and house entry
            if check_door_collision(new_x, new_y):
                open_door()

            # Only allow movement if position is valid
            if can_move_to_position(new_x, new_y):
                player_x = new_x
                player_y = new_y
                # Decrease stamina for S movement
                player_stamina -= STAMINA_DRAIN_RATE
                player_stamina = max(0, player_stamina)

    if key == b'a':  # Rotate left
        player_cam_angle += 5

    if key == b'd':  # Rotate right
        player_cam_angle -= 5

    # (SAMANIA): CODE FOR DAY/NIGHT KEY LISTENERS
    if key == b'L' or key == b'l': # Press L for Light (Day)
        day_night_target = 1.0
        print("Transitioning to Day...")

    if key == b'N' or key == b'n': # Press N for Night
        day_night_target = 0.0
        print("Transitioning to Night...")


    # Reset game with R key
    if key == b'r':
        print("Reset to Life remaining 5, Game Score 0 and Bullets Missed 0")
        score = 0
        missed = 0
        player_lives = 5

        # (samania new): ## ADDED ## - Reset stamina on game reset    
        player_stamina = MAX_STAMINA
        # ====================
        player_hit_count = 0
        game_over = False
        death_rotation = 0
        enemy_list.clear()
        bullets_x.clear()
        bullets_y.clear()
        bullets_z.clear()
        bullets_direction_x.clear()
        bullets_direction_y.clear()
        bullets_angle.clear()

    if key == b'c':
        cheat_mode = not cheat_mode
        print(f"Cheat Mode {'ON' if cheat_mode else 'OFF'}")

    if key == b'v':
        cam_spinner = not cam_spinner
        print(f"Camera Spinner {'ON' if cam_spinner else 'OFF'}")


    # (samania new): ## MODIFIED ## - Added stamina check for jumping    
    # Space bar for jumping
    if key == b' ':
        # Can only jump when on ground and has enough stamina
        if not is_jumping and player_z <= 0 and player_stamina >= STAMINA_COST_JUMP:
            is_jumping = True
            jump_velocity = jump_speed
            player_stamina -= STAMINA_COST_JUMP # Deduct stamina for jumping
            print("Player jumped!")
        elif player_stamina < STAMINA_COST_JUMP:
            print("Not enough stamina to jump!")
    # ====================================


    # Speed control
    if key == b'q':  # Increase speed (Sprint)
        if player_stamina > 10: # Need some stamina to start sprinting
            is_sprinting = True
            move_speed += 2
            if move_speed > 30:  # Maximum speed limit
                move_speed = 30
            print(f"Speed increased to: {move_speed}")
        else:
            print("Not enough stamina to sprint!")

    if key == b'e':  # Decrease speed (Walk)
        is_sprinting = False # Stop sprinting when slowing down
        move_speed -= 2
        if move_speed < 2:  # Minimum speed limit
            move_speed = 2
        print(f"Speed decreased to: {move_speed}")


def specialKeyListener(key, x, y):
    """
    Rotate camera around the player with LEFT/RIGHT arrow keys at fixed radius.
    UP/DOWN moves camera height.
    """
    global camera_offset,angle_inc

    # Don't allow camera movement if game over
    if game_over:
        return

    offset_x, offset_y, offset_z = camera_offset

    # Compute current angle and radius from offset
    angle = math.atan2(offset_y, offset_x)
    radius = math.sqrt(offset_x**2 + offset_y**2)

    # Angle increment for rotation

    if key == GLUT_KEY_LEFT:
        # Rotate counter-clockwise around player
        angle += angle_inc
    elif key == GLUT_KEY_RIGHT:
        # Rotate clockwise around player
        angle -= angle_inc
    elif key == GLUT_KEY_UP:
        # Move camera up with height limit
        if offset_z < 1000:  # Maximum height limit
            offset_z += 10
    elif key == GLUT_KEY_DOWN:
        # Move camera down with ground limit
        if offset_z > 50:  # Minimum height above ground
            offset_z -= 10

    # Update camera offset using polar coordinates
    offset_x = radius * math.cos(angle)
    offset_y = radius * math.sin(angle)
    camera_offset = (offset_x, offset_y, offset_z)


def mouseListener(button, state, x, y):
    global mouse_left, bullets_x, bullets_y, bullets_z, bullets_direction_x, bullets_direction_y, bullets_angle
    global player_x, player_y, player_cam_angle, first_person, cam_spinner, game_over, camera_mode, current_weapon, sword_rotation

    # Don't allow shooting if game over
    if game_over and button == GLUT_LEFT_BUTTON:
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if current_weapon == "gun":
            # Create a new bullet
            player_cam_angle_rad = math.radians(player_cam_angle)
            bullet_direction_x = -math.sin(player_cam_angle_rad)
            bullet_direction_y = math.cos(player_cam_angle_rad)

            # Position bullet at gun tip
            gun_length = 65
            bullet_x = player_x + bullet_direction_x * gun_length
            bullet_y = player_y + bullet_direction_y * gun_length

            # Add new bullet to lists
            bullets_x.append(bullet_x)
            bullets_y.append(bullet_y)
            bullets_z.append(75)
            bullets_direction_x.append(bullet_direction_x)
            bullets_direction_y.append(bullet_direction_y)
            bullets_angle.append(player_cam_angle)
        elif current_weapon == "sword":
            # Rotate sword more slowly by using smaller increments
            # We'll use a counter to slow down the rotation
            global sword_swing_counter

            # Only rotate the sword every 3 clicks
            sword_swing_counter = sword_swing_counter

            if sword_swing_counter == 0:
                # Toggle between 0 and 90 degrees only
                if sword_rotation == 0:
                    sword_rotation = 90
                else:
                    sword_rotation = 0

                # Check for sword-enemy collisions when swinging
                check_sword_enemy_collisions()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        # Cycle through camera modes: 0 (top view) -> 1 (third person) -> 2 (first person) -> 0
        camera_mode = (camera_mode + 1) % 3

        if camera_mode == 0:
            first_person = False
            print("Camera Mode: Top View")
        elif camera_mode == 1:
            first_person = False
            print("Camera Mode: Third Person")
        elif camera_mode == 2:
            first_person = True
            print("Camera Mode: First Person")

        # Reset camera spinner when leaving first-person
        if not first_person and cam_spinner:
            cam_spinner = False
            print("Camera Spinner OFF")


def update_bullet():
    global bullets_x, bullets_y, bullets_z, bullets_direction_x, bullets_direction_y, bullets_angle, missed

    # Set bullet movement speed
    bullet_speed = 20
    bullet_bag = []

    # Check each bullet individually
    for i in range(len(bullets_x)):
        # Calculate new position for current bullet
        new_x = bullets_x[i] + bullets_direction_x[i] * bullet_speed
        new_y = bullets_y[i] + bullets_direction_y[i] * bullet_speed

        # Update bullet position
        bullets_x[i] = new_x
        bullets_y[i] = new_y

        # Boundary checking for X coordinate
        if bullets_x[i] > GRID_LENGTH:
            bullet_bag.append(i)
            missed+=1
        elif bullets_x[i] < -GRID_LENGTH:
            bullet_bag.append(i)
            missed+=1

        # Boundary checking for Y coordinate
        if bullets_y[i] > GRID_LENGTH:
            if i not in bullet_bag:
                bullet_bag.append(i)
                missed+=1
        elif bullets_y[i] < -GRID_LENGTH:
            if i not in bullet_bag:
                bullet_bag.append(i)
                missed+=1

    # Remove bullets that went out of bounds
    # We need to remove in reverse order to avoid index shifting issues
    # ---------------------------------------------------------
    # Step 1: Manually create a reversed copy of bullet_bag
    # ---------------------------------------------------------

    # First, copy all elements into a new list
    bullet_indices_copy = []
    for index in bullet_bag:
        bullet_indices_copy.append(index)

    # Now build a reversed list manually
    bullet_indices_reversed = []
    copy_length = len(bullet_indices_copy)
    current_position = copy_length - 1

    while current_position >= 0:
        bullet_indices_reversed.append(bullet_indices_copy[current_position])
        current_position = current_position - 1

    for i in bullet_indices_reversed:

        #Remove from bullets_x
        if i < len(bullets_x):
            temp_x = bullets_x[i]
            dummy_x = temp_x
            bullets_x.pop(i)
            temp_x = None
            dummy_x = None

        #Remove from bullets_y
        if i < len(bullets_y):
            temp_y = bullets_y[i]
            dummy_y = temp_y
            bullets_y.pop(i)
            temp_y = None
            dummy_y = None

        #Remove from bullets_z
        if i < len(bullets_z):
            temp_z = bullets_z[i]
            dummy_z = temp_z
            bullets_z.pop(i)
            temp_z = None
            dummy_z = None

        #Remove from bullets_direction_x
        if i < len(bullets_direction_x):
            temp_dx = bullets_direction_x[i]
            dummy_dx = temp_dx
            bullets_direction_x.pop(i)
            temp_dx = None
            dummy_dx = None

        #Remove from bullets_direction_y
        if i < len(bullets_direction_y):
            temp_dy = bullets_direction_y[i]
            dummy_dy = temp_dy
            bullets_direction_y.pop(i)
            temp_dy = None
            dummy_dy = None

        #Remove from bullets_angle
        if i < len(bullets_angle):
            temp_angle = bullets_angle[i]
            dummy_angle = temp_angle
            bullets_angle.pop(i)
            temp_angle = None
            dummy_angle = None


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Works for free camera or first-person mode.
    This version is intentionally verbose with redundant steps
    for clarity and padding purposes.
    """
    global player_x, player_y, player_z, player_cam_angle, first_person, cheat_mode, cam_spinner, camera_pos, camera_offset, fovY, camera_mode

    # ------------------ Projection Setup ------------------
    # Switch to projection matrix mode
    glMatrixMode(GL_PROJECTION)

    # Clear previous projection settings
    glLoadIdentity()

    # Set perspective projection
    aspect_ratio = 1.25  # Width / Height
    near_plane = 0.1
    far_plane = 1500

    # Temporary variables (redundant)
    temp_fov = fovY
    temp_aspect = aspect_ratio
    temp_near = near_plane
    temp_far = far_plane

    gluPerspective(temp_fov, temp_aspect, temp_near, temp_far)

    # Reset temporary variables
    temp_fov = None
    temp_aspect = None
    temp_near = None
    temp_far = None

    # ------------------ Modelview Setup ------------------
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Temporary modelview reset variable (redundant)
    modelview_reset = True
    if modelview_reset:
        _ = modelview_reset
    modelview_reset = None

    # ------------------ Camera Positioning ------------------
    if camera_mode == 2:  # First Person Mode
        # Determine camera height (including jump height)
        if cheat_mode:
            cam_z = 110 + player_z  # Higher camera in cheat mode + jump height
        else:
            cam_z = 90 + player_z   # Normal first-person height + jump height

        # Assign player coordinates
        cam_x = player_x
        cam_y = player_y

        # Redundant temporary variables
        temp_cam_x = cam_x
        temp_cam_y = cam_y
        temp_cam_z = cam_z

        # ------------------ Back Offset ------------------
        back_offset = 15  # Move camera slightly backward
        angle_rad = math.radians(player_cam_angle)

        offset_x = math.sin(angle_rad) * back_offset
        offset_y = math.cos(angle_rad) * back_offset

        # Apply back offset
        cam_x = cam_x - offset_x
        cam_y = cam_y + offset_y

        # Reset temporary offset variables
        offset_x = None
        offset_y = None

        # ------------------ Look Target ------------------
        look_distance = 300
        look_x = 0
        look_y = 0
        look_z = cam_z  # Straight ahead

        # Determine look direction based on cheat mode and spinner
        if cheat_mode:
            if cam_spinner:
                # Spin camera with player
                look_x = cam_x - math.sin(angle_rad) * look_distance
                look_y = cam_y + math.cos(angle_rad) * look_distance
            else:
                # Fixed direction in cheat mode without spinner
                fixed_angle = math.radians(0)  # North
                look_x = cam_x - math.sin(fixed_angle) * look_distance
                look_y = cam_y + math.cos(fixed_angle) * look_distance
                fixed_angle = None  # reset redundant variable
        else:
            # Normal first-person (follows player angle)
            look_x = cam_x - math.sin(angle_rad) * look_distance
            look_y = cam_y + math.cos(angle_rad) * look_distance

        # Temporary variables for clarity
        temp_look_x = look_x
        temp_look_y = look_y
        temp_look_z = look_z

        # ------------------ Set Camera ------------------
        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 0, 1)

        # Reset temporary variables
        temp_cam_x = None
        temp_cam_y = None
        temp_cam_z = None
        temp_look_x = None
        temp_look_y = None
        temp_look_z = None
    elif camera_mode == 0:  # Top View Mode
        # ------------------ Top View Camera Directly Above Player ------------------
        # Position camera directly above the player
        cam_x = player_x
        cam_y = player_y
        cam_z = 800  # High above the player for top view

        # Look straight down at the player
        target_x = player_x
        target_y = player_y
        target_z = 0  # Ground level

        # Set camera orientation (Y-axis forward for top view)
        up_x = 0
        up_y = 1
        up_z = 0

        # Set camera
        gluLookAt(cam_x, cam_y, cam_z,
                  target_x, target_y, target_z,
                  up_x, up_y, up_z)
    else:  # Third Person Mode (camera_mode == 1)
        # ------------------ Slanted Third Person Camera Following Player with Arrow Key Control ------------------
        # Get camera offset relative to player
        offset_x, offset_y, offset_z = camera_offset

        # Calculate actual camera position by applying offset to player position
        cam_x = player_x + offset_x
        cam_y = player_y + offset_y
        cam_z = offset_z  # Use arrow key controlled height

        # Redundant temporary variables
        temp_x = cam_x
        temp_y = cam_y
        temp_z = cam_z

        # Look slightly ahead of the player position for slanted view, with higher target to show more of the top
        target_x, target_y, target_z = player_x + 50, player_y + 50, 200
        up_x, up_y, up_z = 0, 0, 1  # Z-axis up for slanted orientation

        # Set camera
        gluLookAt(temp_x, temp_y, temp_z,
                  target_x, target_y, target_z,
                  up_x, up_y, up_z)

        # Reset temporary variables
        temp_x = None
        temp_y = None
        temp_z = None
        target_x = None
        target_y = None
        target_z = None
        up_x = None
        up_y = None
        up_z = None
def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    global chicken_bob_angle, cow_tail_angle, cloud_animation_timer

    cloud_animation_timer += 1
    if cloud_animation_timer > 1:
        for cloud in cloud_positions:
            cloud['pos'][0] += 0.5  # Move clouds slowly to the right
            if cloud['pos'][0] > 2000:
                cloud['pos'][0] = -2000
        cloud_animation_timer = 0

    glutPostRedisplay()


    # (SAMANIA): CODE - CALL CYCLE UPDATE
    update_day_night_cycle() # Update the day/night transition


    # (samania new): CALL UPDATES FOR STAMINA AND WEATHER                  
    update_stamina()
    update_weather()
    # =====================

    update_bullet()
    update_player_jump()  # Update jumping physics
    if not game_over and not is_day:  # Only update enemies if not game over and it's not day
        update_enemies()  # Update enemy animations and positions
        check_bullet_enemy_collisions()  # Check for collisions each frame
        cheat_mode_behavior()  # Handle cheat mode
    check_game_over()  # Check for game over conditions
    update_player_death_animation()  # Update death animation

    # Update village animations
    chicken_bob_angle = (chicken_bob_angle + 3) % 360  # Chicken bobbing
    cow_tail_angle = (cow_tail_angle + 2) % 360        # Cow tail swaying


def reshape(width, height):
    """Handle window reshape events for proper fullscreen support"""
    if height == 0:
        height = 1

    # Set viewport to cover the entire window
    glViewport(0, 0, width, height)

    # Set projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Calculate aspect ratio
    aspect_ratio = float(width) / float(height)
    gluPerspective(fovY, aspect_ratio, 0.1, 2000.0)

    glMatrixMode(GL_MODELVIEW)


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """

    #  (SAMANIA): CODE FOR DYNAMIC SKY COLOR

    # Interpolate between day and night color based on time_of_day
    day_color = sky_colors[0]
    night_color = sky_colors[1]

    sky_r = night_color[0] + (day_color[0] - night_color[0]) * time_of_day
    sky_g = night_color[1] + (day_color[1] - night_color[1]) * time_of_day
    sky_b = night_color[2] + (day_color[2] - night_color[2]) * time_of_day

    # (SAMANIA) This line is to use the dynamic sky color.
    glClearColor(sky_r, sky_g, sky_b, 1.0)
    # ==============================================================================



    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor) - larger with green sand and green patches
    glBegin(GL_QUADS)
    square_len = 100
    grid_size = 60  # Increased to cover the full 3000x3000 grid
    x_val = -GRID_LENGTH
    y_val = GRID_LENGTH


    # (SAMANIA)): CODE FOR SEASONAL GRASS COLOR

    grass_palette = season_grass_colors.get(current_season)
    base_color = grass_palette[0]
    patch1_color = grass_palette[1]
    patch2_color = grass_palette[2]


    for i in range(grid_size):          # rows
        for j in range(grid_size):      # cols

            # (SAMANIA) Create a pattern of green sand with green grass patches
            #  MODIFICATION FOR SEASONAL GRASS COLOR
            # seasonal palette instead of fixed colors.
            if (i + j) % 7 == 0 or (i * 3 + j * 2) % 11 == 0:  # Green grass patches
                glColor3f(patch1_color[0], patch1_color[1], patch1_color[2])
            elif (i + j) % 3 == 0:  # Some lighter green patches
                glColor3f(patch2_color[0], patch2_color[1], patch2_color[2])
            else:  # Base green sand color
                glColor3f(base_color[0], base_color[1], base_color[2])


            # corners using incremental x_val, y_val
            glVertex3f(x_val, y_val, 0)
            glVertex3f(x_val + square_len, y_val, 0)
            glVertex3f(x_val + square_len, y_val - square_len, 0)
            glVertex3f(x_val, y_val - square_len, 0)

            # move right
            x_val += square_len

        # reset x and move down after row ends
        x_val = -GRID_LENGTH
        y_val -= square_len

    glEnd()

    wall_height = 100

    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.0)  # Black wall color

    # Top wall (along X, at y = GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)

    glColor3f(0.0, 0.0, 0.0)  # Black wall color
    # Bottom wall (along X, at y = -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    glColor3f(0.0, 0.0, 0.0)  # Black wall color
    # Left wall (along Y, at x = -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    glColor3f(0.0, 0.0, 0.0)  # Black wall color
    # Right wall (along Y, at x = GRID_LENGTH)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)

    glEnd()

    # Update door system
    update_door_system()

    # Print game stats periodically instead of constant on-screen text
    if hasattr(showScreen, 'frame_count'):
        showScreen.frame_count += 1
    else:
        showScreen.frame_count = 0

    if showScreen.frame_count % 180 == 0:  # Print every 3 seconds
        print(f"Score: {score} | Lives: {player_lives} | Enemies: {len(enemy_list)} | Position: ({player_x:.0f}, {player_y:.0f})")
        print(f"Door Open: {door_open} | In House: {check_house_collision(player_x, player_y)}")

    # Only draw minimal essential text to avoid font errors
    if not game_over:
        draw_text(10, 770, f"Score: {score}")
        draw_text(10, 740, f"Lives: {player_lives}")
        draw_text(10, 710, f"WASD to move, R to reset, F for fullscreen")

    update_merchants()
    draw_clouds()

    # (samania new): CALL WEATHER DRAWING FUNCTION              
    draw_weather()
    draw_shapes()

    # (samania new): CALL HUD DRAWING FUNCTION      
    # Draw the HUD on top of everything else
    draw_hud()
    # ==========

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    initialize_clouds()
    # (samania new): INITIALIZE THE WEATHER SYSTEM          
    initialize_weather()
    # =============
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D Shooter Game")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutReshapeFunc(reshape)  # Register reshape function for fullscreen support
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()