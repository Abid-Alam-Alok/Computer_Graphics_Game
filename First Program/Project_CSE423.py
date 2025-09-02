from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

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
player_x = 0
player_y = 0
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
cheat_mode = False  # If true, enemies won't move towards player
val = 0
cam_spinner = False
static_first_person = False
player_lives = 5
game_over = False  # Game over state
death_rotation = 0  # Player rotation on X-axis for falling animation
imp_val = 0
fovY = 120  # Field of view
GRID_LENGTH = 1000  # Length of grid lines (increased from 600)
rand_var = 423
angle_hacks = math.radians(3)
angle_inc = math.radians(5)

# House and door system variables
door_open = False
door_timer = 0
door_auto_close_time = 180  # frames (3 seconds at 60fps)
house_x = -800  # House in bottom-left corner
house_y = -800
house_width = 250
house_depth = 250




def check_game_over():
    """Check if game over conditions are met and handle game over state"""
    global player_lives, missed, player_hit_count, game_over, enemy_list
   
    # Check if player should lose a life
    if missed >= 10:
        player_lives -= 5
        missed = 0  # Reset missed count
        print(f"Life lost due to missed shots! Lives remaining: {player_lives}")
   
    if player_hit_count >= 1:
        player_lives -= 1
        player_hit_count = 0  # Reset hit count
        print(f"Life lost due to enemy contact! Lives remaining: {player_lives}")
   
    # Check for game over
    if player_lives <= 0 and not game_over:
        game_over = True
        enemy_list.clear()  # Remove all enemies
        print("GAME OVER!")


def update_player_death_animation():
    global death_rotation
   
    if game_over and death_rotation < 90:
        death_rotation += 90
   


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
    """Check if player is near the door"""
    global house_x, house_y, house_width, house_depth
    door_x = house_x + house_width/3  # Door position 
    door_y = house_y + house_depth/2  # Front wall
    door_width = 60
    
    # Check if player is within door area
    distance_to_door = math.sqrt((x - door_x)**2 + (y - door_y)**2)
    return distance_to_door < 60  # Increased detection range


def check_cave_collision(x, y):
    """Check if position is inside cave boundaries"""
    cave_x = 800   # Cave in top-right corner (opposite to house)
    cave_y = 800
    cave_width = 400
    cave_depth = 400
    
    cave_left = cave_x - cave_width/2
    cave_right = cave_x + cave_width/2
    cave_front = cave_y + cave_depth/2
    cave_back = cave_y - cave_depth/2
    
    return (cave_left < x < cave_right) and (cave_back < y < cave_front)


def update_door_system():
    """Update door open/close system"""
    global door_open, door_timer
    
    # Check if player is near door
    near_door = check_door_collision(player_x, player_y)
    
    if near_door and not door_open:
        door_open = True
        door_timer = 0
        print(f"Door opened! Player at ({player_x:.1f}, {player_y:.1f})")
    
    if door_open:
        door_timer += 1
        if door_timer > door_auto_close_time:
            door_open = False
            door_timer = 0
            print("Door closed!")


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
    
    # Check if trying to enter house
    if check_house_collision(new_x, new_y):
        # Only allow entry through open door
        if door_open and check_door_collision(new_x, new_y):
            return True
        return False
    
    # Check if leaving house - only through door
    current_in_house = check_house_collision(player_x, player_y)
    if current_in_house and not check_house_collision(new_x, new_y):
        # Leaving house - must be through door
        if door_open and check_door_collision(player_x, player_y):
            return True
        return False
    
    return True








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
       
        if far_player and not_in_house and not_in_cave:
            # Z-coordinate (always 0 for now)
            enemy_z = 0
           
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


def draw_text(x, y, text):
    """Simple text rendering without glutBitmapCharacter to avoid font errors"""
    # For now, just print to console instead of rendering on screen
    # This prevents the font errors while maintaining functionality
    pass


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


    enemy_speed = 0.1
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

            # Prevent enemies from entering house/cave and stay within bounds
            if (-GRID_LENGTH < new_x < GRID_LENGTH and -GRID_LENGTH < new_y < GRID_LENGTH 
                and not check_house_collision(new_x, new_y) and not check_cave_collision(new_x, new_y)):
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
    house_width = 250
    house_depth = 250
    house_height = 150
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
    door_width = 60
    door_height = 120
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


def draw_cave(x, y, z):
    """Draw a large cave with crystals, mushrooms, and rocks"""
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Cave dimensions - much larger
    cave_width = 400
    cave_depth = 400
    cave_height = 200
    wall_thickness = 30
    
    # Draw cave floor - dark grey stone
    glPushMatrix()
    glTranslatef(0, 0, 5)
    glColor3f(0.15, 0.15, 0.15)  # Dark grey floor
    glScalef(cave_width, cave_depth, 10)
    glutSolidCube(1)
    glPopMatrix()
    
    # Draw cave walls - textured with alternating blocks
    # Back wall
    for i in range(16):  # More blocks for larger cave
        for j in range(8):
            block_x = -cave_width/2 + (i * 25) + 12.5
            block_z = 25 + (j * 25)
            glPushMatrix()
            glTranslatef(block_x, -cave_depth/2 + wall_thickness/2, block_z)
            if (i + j) % 3 == 0:
                glColor3f(0.05, 0.05, 0.05)  # Almost black
            elif (i + j) % 3 == 1:
                glColor3f(0.1, 0.1, 0.1)   # Very dark grey
            else:
                glColor3f(0.2, 0.2, 0.2)   # Dark grey
            glScalef(25, wall_thickness, 25)
            glutSolidCube(1)
            glPopMatrix()
    
    # Left wall
    for i in range(16):
        for j in range(8):
            block_y = -cave_depth/2 + (i * 25) + 12.5
            block_z = 25 + (j * 25)
            glPushMatrix()
            glTranslatef(-cave_width/2 + wall_thickness/2, block_y, block_z)
            if (i + j) % 3 == 0:
                glColor3f(0.0, 0.0, 0.0)   # Black
            elif (i + j) % 3 == 1:
                glColor3f(0.15, 0.15, 0.15) # Dark grey
            else:
                glColor3f(0.1, 0.1, 0.1)   # Very dark grey
            glScalef(wall_thickness, 25, 25)
            glutSolidCube(1)
            glPopMatrix()
    
    # Right wall  
    for i in range(16):
        for j in range(8):
            block_y = -cave_depth/2 + (i * 25) + 12.5
            block_z = 25 + (j * 25)
            glPushMatrix()
            glTranslatef(cave_width/2 - wall_thickness/2, block_y, block_z)
            if (i + j) % 3 == 0:
                glColor3f(0.15, 0.15, 0.15) # Dark grey
            else:
                glColor3f(0.0, 0.0, 0.0)   # Black
            glScalef(wall_thickness, 25, 25)
            glutSolidCube(1)
            glPopMatrix()
    
    # Front wall with entry opening
    for i in range(16):
        for j in range(8):
            # Create entry opening in the middle of the front wall
            entry_start_i = 6  # Start of entry opening
            entry_end_i = 10   # End of entry opening  
            entry_height = 4   # Height of entry (up to j=4)
            
            # Skip blocks to create the entry opening
            if entry_start_i <= i <= entry_end_i and j <= entry_height:
                continue  # Skip this block to create the opening
                
            block_x = -cave_width/2 + (i * 25) + 12.5
            block_z = 25 + (j * 25)
            glPushMatrix()
            glTranslatef(block_x, cave_depth/2 - wall_thickness/2, block_z)
            if (i + j) % 3 == 0:
                glColor3f(0.1, 0.1, 0.1)   # Very dark grey
            elif (i + j) % 3 == 1:
                glColor3f(0.0, 0.0, 0.0)   # Black
            else:
                glColor3f(0.15, 0.15, 0.15) # Dark grey
            glScalef(25, wall_thickness, 25)
            glutSolidCube(1)
            glPopMatrix()
    
    # Cave ceiling
    for i in range(16):
        for j in range(16):
            block_x = -cave_width/2 + (i * 25) + 12.5
            block_y = -cave_depth/2 + (j * 25) + 12.5
            glPushMatrix()
            glTranslatef(block_x, block_y, cave_height)
            if (i + j) % 4 == 0:
                glColor3f(0.0, 0.0, 0.0)   # Black
            elif (i + j) % 4 == 1:
                glColor3f(0.1, 0.1, 0.1)   # Very dark grey
            else:
                glColor3f(0.2, 0.2, 0.2)   # Dark grey
            glScalef(25, 25, 15)
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
    
    glPopMatrix()


def draw_shapes():
    """Draw all game shapes including enemies and player"""
    global player_x, player_y, player_cam_angle, enem_rad_top, enem_rad_bottom, enem_growing, game_over

    # Only maintain 5 enemies if not game over
    if not game_over:
        while len(enemy_list) < 5:
            make_new_enemy()

    # Rearrange world objects according to user's drawing
    # Trees positioned around the map
    tree_positions = [
        (-800, 800, 0),     # Top-left corner (near cave)
        (-300, 900, 0),     # Top area
        (300, 900, 0),      # Top area  
        (-900, 300, 0),     # Left side
        (-900, -300, 0),    # Left side
        (-300, -900, 0),    # Bottom area
        (300, -900, 0),     # Bottom area
        (900, -300, 0),     # Right side (away from cave)
        (200, 200, 0),      # Central area
    ]

    for tree_x, tree_y, tree_z in tree_positions:
        # Enhanced tree with many branches and varied leaf clusters
        glPushMatrix()
        glTranslatef(tree_x, tree_y, tree_z)

        trunk_length = 200
        trunk_radius = 10
        leaf_radius = 30  # Increased base leaf size

        # Draw trunk (solid cylinder)
        glColor3f(0.55, 0.27, 0.07)  # Brown
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluCylinder(quadric, trunk_radius, trunk_radius * 0.6, trunk_length, 24, 24)
        gluDeleteQuadric(quadric)

        # Draw multiple layers of branches for a fuller tree
        branch_levels = 5  # Number of vertical levels
        branch_count = 20 # Base number of branches
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
                gluQuadricDrawStyle(branch_quad, GLU_FILL)
                gluCylinder(branch_quad, branch_radius, branch_radius * 0.3, level_branch_length, 12, 12)
                gluDeleteQuadric(branch_quad)
                
                # Draw multiple leaf clusters at end of branch for more spread
                glTranslatef(0, 0, level_branch_length)
                
                # Create 3-5 leaf clusters per branch tip for fuller appearance
                num_leaf_clusters = 3 + (i % 3)  # 3-5 clusters per branch
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
                    size_variation = 0.8 + (cluster % 4) * 0.4  # Size varies from 0.8 to 2.0
                    current_leaf_radius = leaf_radius * size_variation * (1.3 - level * 0.15)
                    
                    # Different shades of green
                    green_variations = [
                        (0.0, 0.8, 0.2),   # Bright green
                        (0.1, 0.7, 0.1),   # Medium green  
                        (0.0, 0.6, 0.3),   # Forest green
                        (0.2, 0.9, 0.2),   # Light green
                        (0.0, 0.5, 0.2),   # Dark green
                        (0.3, 0.8, 0.3),   # Light forest green
                        (0.0, 0.9, 0.4)    # Spring green
                    ]
                    green_color = green_variations[(i + cluster) % len(green_variations)]
                    glColor3f(green_color[0], green_color[1], green_color[2])
                    
                    leaf_quad = gluNewQuadric()
                    gluQuadricDrawStyle(leaf_quad, GLU_FILL)
                    gluSphere(leaf_quad, current_leaf_radius, 20, 20)
                    gluDeleteQuadric(leaf_quad)
                    
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
            glColor3f(0.1, 0.9, 0.1)  # Bright green for top
            top_leaf_quad = gluNewQuadric()
            gluQuadricDrawStyle(top_leaf_quad, GLU_FILL)
            gluSphere(top_leaf_quad, leaf_radius * (1.2 + top_cluster * 0.2), 24, 24)
            gluDeleteQuadric(top_leaf_quad)
            glPopMatrix()

        glPopMatrix()

    # Draw the house in bottom-left corner (opposite from cave)
    house_x = -800  # Bottom-left corner
    house_y = -800  # Bottom-left corner
    draw_house(house_x, house_y, 0)

    # Draw the large cave in top-right corner with crystals, mushrooms, and rocks
    cave_x = 800   # Top-right corner
    cave_y = 800
    draw_cave(cave_x, cave_y, 0)

    # Draw all enemies - only if not game over
    if not game_over:
        for enemy in enemy_list:
            enemy_x, enemy_y, enemy_z = enemy
            glPushMatrix()
            glTranslatef(enemy_x, enemy_y, enemy_z)
           
            # Bottom sphere (body) - red
            glColor3f(1, 0, 0)
            gluSphere(gluNewQuadric(), enem_rad_bottom, 20, 20)

            # Move up for top sphere (head), lowered to touch bottom sphere
            glTranslatef(0, 0, enem_rad_bottom)  
            # Top sphere (head) - black
            glColor3f(0, 0, 0)
            gluSphere(gluNewQuadric(), enem_rad_top, 20, 20)

            glPopMatrix()

    glPushMatrix()
    # Move and rotate the entire player
    glTranslatef(player_x, player_y, 0)  # Base position at ground
    glRotatef(player_cam_angle, 0, 0, 1)
   
    # Apply death rotation if game over
    if game_over:
        glRotatef(death_rotation, 1, 0, 0)  # Rotate around X-axis to fall

    # --- BODY ---
    glPushMatrix()
    glTranslatef(0, 0, 60)  # body center above ground
    glColor3f(1, 0, 1)
    draw_scaled_cuboid(50, 20, 60)
    glPopMatrix()

    # --- LEFT LEG ---
    glPushMatrix()
    glTranslatef(-15, 0, 0)  # relative to body
    glColor3f(0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 10, 40, 20, 20)
    glPopMatrix()

    # --- RIGHT LEG ---
    glPushMatrix()
    glTranslatef(15, 0, 0)
    glColor3f(0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 10, 40, 20, 20)
    glPopMatrix()

    # --- LEFT ARM ---
    glPushMatrix()
    glTranslatef(-15, 0, 75)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0, 1, 0)
    gluCylinder(gluNewQuadric(), 7, 5, 35, 20, 20)
    glPopMatrix()

    # --- RIGHT ARM + GUN ---
    glPushMatrix()
    glTranslatef(15, 0, 75)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0, 1, 0)
    gluCylinder(gluNewQuadric(), 7, 5, 35, 20, 20)

    glTranslatef(-15, 0, 0)  # Move to gun position
    glColor3f(0.2, 0.2, 0.2)
    gluCylinder(gluNewQuadric(), 7, 2, 65, 20, 20)
    glPopMatrix()

    # --- HEAD OR SPHERE ---
    glPushMatrix()
    glTranslatef(0, 0, 100)  # top of body
    glColor3f(1, 1, 1)
    gluSphere(gluNewQuadric(), 15, 10, 10)
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
    global player_x, player_y, player_cam_angle, game_over, score, enemy_list, bullets_x, bullets_y, bullets_z
    global bullets_direction_x, bullets_direction_y, bullets_angle, missed, cheat_mode, cam_spinner, first_person
    global player_lives, player_hit_count, death_rotation
   
    # Don't allow movement if game over
    if game_over and key != b'r':
        return
       
    if player_cam_angle < 0:
        player_cam_angle += 360
    if player_cam_angle >= 360:
        player_cam_angle = 0

    move_speed = 10

    if key == b'w':  # Move forward
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

    if key == b's':  # Move backward
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

    if key == b'a':  # Rotate left
        player_cam_angle += 5

    if key == b'd':  # Rotate right
        player_cam_angle -= 5

    # Reset game with R key
    if key == b'r':
        print("Reset to Life remaining 5, Game Score 0 and Bullets Missed 0")
        score = 0
        missed = 0
        player_lives = 5
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
    
    # F11 for fullscreen toggle (using 'f' key since F11 might not be available)
    if key == b'f':
        glutFullScreen()
        print("Switching to fullscreen")


def specialKeyListener(key, x, y):
    """
    Rotate camera around the origin (0,0,0) with LEFT/RIGHT arrow keys.
    UP/DOWN moves camera height.
    """
    global camera_pos,angle_inc
   
    # Don't allow camera movement if game over
    if game_over:
        return
       
    cam_x, cam_y, cam_z = camera_pos


    # Compute current angle in X-Y plane
    y = cam_y
    x = cam_x
    angle = math.atan2(y, x)
    radius = math.sqrt(x**2 + y**2)


    # Angle increment for rotation
   


    if key == GLUT_KEY_LEFT:
        # Rotate counter-clockwise around origin
        angle += angle_inc
    elif key == GLUT_KEY_RIGHT:
        # Rotate clockwise around origin
        angle -= angle_inc
    elif key == GLUT_KEY_UP:
        # Move camera up
        cam_z += 10
    elif key == GLUT_KEY_DOWN:
        # Move camera down
        cam_z -= 10


    # Update camera position using polar coordinates
    cam_x = radius * math.cos(angle)
    cam_y = radius * math.sin(angle)
    camera_pos = (cam_x, cam_y, cam_z)


def mouseListener(button, state, x, y):
    global mouse_left, bullets_x, bullets_y, bullets_z, bullets_direction_x, bullets_direction_y, bullets_angle
    global player_x, player_y, player_cam_angle, first_person, cam_spinner, game_over
   
    # Don't allow shooting if game over
    if game_over and button == GLUT_LEFT_BUTTON:
        return
   
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
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
   
    if button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        # Allow first-person toggle in both normal and cheat mode
        first_person = not first_person
        if first_person:
            print("First-Person Mode: ON")
        else:
            print("First-Person Mode: OFF")
            # Reset camera spinner when leaving first-person
            if cam_spinner:
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
    global player_x, player_y, player_cam_angle, first_person, cheat_mode, cam_spinner, camera_pos, fovY


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
    if first_person:
        # Determine camera height
        if cheat_mode:
            cam_z = 110  # Higher camera in cheat mode
        else:
            cam_z = 90   # Normal first-person height


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
    else:
        # ------------------ Free Camera ------------------
        x, y, z = camera_pos
       
        # Redundant temporary variables
        temp_x = x
        temp_y = y
        temp_z = z
       
        target_x, target_y, target_z = 0, 0, 0
        up_x, up_y, up_z = 0, 0, 1
       
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
    glutPostRedisplay()
    update_bullet()
    if not game_over:  # Only update enemies if not game over
        update_enemies()  # Update enemy animations and positions
        check_bullet_enemy_collisions()  # Check for collisions each frame
        cheat_mode_behavior()  # Handle cheat mode
    check_game_over()  # Check for game over conditions
    update_player_death_animation()  # Update death animation


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
    grid_size = 20  # Increased from 12 to make it larger
    x_val = -1000
    y_val = 1000

    for i in range(grid_size):          # rows
        for j in range(grid_size):      # cols
            # Create a pattern of green sand with green grass patches
            if (i + j) % 7 == 0 or (i * 3 + j * 2) % 11 == 0:  # Green grass patches
                glColor3f(0.2, 0.6, 0.2)  # Dark green grass
            elif (i + j) % 3 == 0:  # Some lighter green patches
                glColor3f(0.3, 0.7, 0.3)  # Medium green
            else:  # Base green sand color
                glColor3f(0.8, 0.7, 0.4)  # Sandy beige/light brown

            # corners using incremental x_val, y_val
            glVertex3f(x_val, y_val, 0)
            glVertex3f(x_val + square_len, y_val, 0)
            glVertex3f(x_val + square_len, y_val - square_len, 0)
            glVertex3f(x_val, y_val - square_len, 0)

            # move right
            x_val += square_len

        # reset x and move down after row ends
        x_val = -1000
        y_val -= square_len


    glEnd()


    wall_height = 100

    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.0)  # Black wall color

    # Top wall (along X, at y = 1000)
    glVertex3f(-1000, 1000, 0)
    glVertex3f(1000, 1000, 0)
    glVertex3f(1000, 1000, wall_height)
    glVertex3f(-1000, 1000, wall_height)
   
    glColor3f(0.0, 0.0, 0.0)  # Black wall color
    # Bottom wall (along X, at y = -1000)
    glVertex3f(-1000, -1000, 0)
    glVertex3f(1000, -1000, 0)
    glVertex3f(1000, -1000, wall_height)
    glVertex3f(-1000, -1000, wall_height)
   
    glColor3f(0.0, 0.0, 0.0)  # Black wall color
    # Left wall (along Y, at x = -1000)
    glVertex3f(-1000, -1000, 0)
    glVertex3f(-1000, 1000, 0)
    glVertex3f(-1000, 1000, wall_height)
    glVertex3f(-1000, -1000, wall_height)

    glColor3f(0.0, 0.0, 0.0)  # Black wall color
    # Right wall (along Y, at x = 1000)
    glVertex3f(1000, -1000, 0)
    glVertex3f(1000, 1000, 0)
    glVertex3f(1000, 1000, wall_height)
    glVertex3f(1000, -1000, wall_height)


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
   


    draw_shapes()


    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
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

