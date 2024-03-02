import pygame, sys, random, math, time, threading, csv
from datetime import datetime

#TODO: Create random "boost/perk drops" (extra health, new gun etc)

#TODO: Create enemy damage to player

#TODO: Create shooting enemies (different enemies in general)

#TODO: Add more music, and pick random songs

#TODO: Add boss and designated song (big task)

#TODO: Add walkthrough if no games have been played yet (using CSV list)

#TODO: Add different "woosh" sound effects for different enemies

#TODO: Add vignette effect

#TODO: Add "score counter" or some sort of "progress tracking" slider

#TODO: Add inventory (big task)

#TODO: Add more setteling background music/random dramatic sounds

#TODO: Add sound effects when picking up guns and healing

#TODO: Add sound effects when boosting



pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)

# Define images and gifs for the main game loop
images = {
    "loading_image": "assets/images/loadingScreenImage.png",
    "icon": "assets/images/windowIcon.png",
    "playerImage": "assets/images/player.png",
    "bullet_image": "assets/images/bullet.png",
    "pointer_image": "assets/images/Pointer.png",
    "close_icon_image": "assets/images/closeIcon.png",
    "red_close_icon_image": "assets/images/redCloseIcon.png",
    "full_heart": "assets/images/full_heart.png",
    "shield_heart": "assets/images/shield_heart.png",
    "paused_text": "assets/images/paused_text.png",
    "particles_off_image": "assets/images/particles_off_image.png",
    "particles_on_image": "assets/images/particles_on_image.png",
    "sound_sfx_off_image": "assets/images/sound_sfx_off_image.png",
    "sound_sfx_on_image": "assets/images/sound_sfx_on_image.png",
    "music_off_image": "assets/images/music_off_image.png",
    "music_on_image": "assets/images/music_on_image.png",
    "volume_scroller_bar": "assets/images/volume_scroller_bar.png",
    "volume_scroller_bar_overlay": "assets/images/volume_bar_overlay.png",
    "volume_scroller_knob": "assets/images/volume_scroller_knob.png",
    "volume_icon_high": "assets/images/volume_icon_high.png",
    "volume_icon_medium": "assets/images/volume_icon_medium.png",
    "volume_icon_low": "assets/images/volume_icon_low.png",
    "volume_icon_off": "assets/images/volume_icon_off.png",
    "ascend_image": "assets/images/ascend_image.png",
    "ascend_hover_image": "assets/images/ascend_hover_image.png",
    "game_image": "assets/images/game_image.png",
    "game_stats": "assets/images/game_stats.png",
}

guns = {
    'small_pistol': {'file': 'assets/guns/small_pistol.png', 'level': 1, 'damage': 10, 'spread': 1, 'speed': 1.2, 'spread_angle': 0},
    'medium_rifle': {'file': 'assets/guns/medium_rifle.png', 'level': 2, 'damage': 15, 'spread': 1, 'speed': 1.7, 'spread_angle': 0},
    'assault_rifle': {'file': 'assets/guns/assault_rifle.png', 'level': 3, 'damage': 20, 'spread': 1, 'speed': 1.5, 'spread_angle': 0},
    'shotgun': {'file': 'assets/guns/shotgun.png', 'level': 4, 'damage': 5, 'spread': 5, 'speed': 2, 'spread_angle': .6},
    'thompson': {'file': 'assets/guns/thompson.png', 'level': 5, 'damage': 30, 'spread': 1, 'speed': 1, 'spread_angle': .1},
    'combat_shotgun': {'file': 'assets/guns/combat_shotgun.png', 'level': 6, 'damage': 10, 'spread': 5, 'speed': 2, 'spread_angle': .4},
    'sniper_rifle': {'file': 'assets/guns/sniper_rifle.png', 'level': 7, 'damage': 120, 'spread': 1, 'speed': 3, 'spread_angle': 0},
    'steyer_AUG': {'file': 'assets/guns/steyer_AUG.png', 'level': 8, 'damage': 25, 'spread': 1, 'speed': .5, 'spread_angle': .15},
    'm249': {'file': 'assets/guns/m249.png', 'level': 9, 'damage': 60, 'spread': 1, 'speed': .8, 'spread_angle': .05},
}

sound_effects = {
    'explosion': pygame.mixer.Sound('assets/sounds/enemy_explode.mp3'),
    'thud': pygame.mixer.Sound('assets/sounds/thud_sound.mp3'),
    'suicide': pygame.mixer.Sound('assets/sounds/enemy_suicide.mp3'),
    'click': pygame.mixer.Sound('assets/sounds/mouse_click.mp3'),
    'bass': pygame.mixer.Sound('assets/sounds/bass_drop.mp3'),
    'bass_impact': pygame.mixer.Sound('assets/sounds/Bass_Impact.mp3'),
    'woosh1': pygame.mixer.Sound('assets/sounds/woosh1.mp3'),
    'woosh2': pygame.mixer.Sound('assets/sounds/woosh2.mp3'),
    'woosh3': pygame.mixer.Sound('assets/sounds/woosh3.mp3'),
    'pistol_cocking': pygame.mixer.Sound('assets/sounds/pistol_cocking.mp3'),
    'drone_sound': pygame.mixer.Sound('assets/sounds/drone_sound.mp3'),
}

music = {
    'Mountain_Trials': {'file': 'assets/music/Mountain_Trials.mp3', 'base_volume': 1, 'original_volume': 1},
    'Dungeon_Boss': {'file': 'assets/music/Dungeon_Boss.mp3', 'baise_volume': 1, 'original_volume': 1},
    'drone_sound': {'file': 'assets/music/drone_sound.mp3', 'base_volume': 1, 'original_volume': 1},
}

enemy_lib = {
    'enemy1': {
        'speed': 3,
        'min_spawn_dist': 700,
        'spawn_rate': 0.8,  # seconds
        'damage': 1,
        'hp': 10,
        'rarity': 70,
        'size': (100, 85),
        'image': pygame.image.load("assets/images/enemy1.png"),
        'pool': 1
    },
    'enemy2': {
        'speed': 2,
        'min_spawn_dist': 700,
        'spawn_rate': 2,  # seconds
        'damage': 2,
        'hp': 40,
        'rarity': 20,
        'size': (100, 85),
        'image': pygame.image.load("assets/images/enemy1.png"),
        'pool': 2
    },
    'enemy3': {
        'speed': 1.8,
        'min_spawn_dist': 900,
        'spawn_rate': 4,  # seconds
        'damage': 4,
        'hp': 80,
        'rarity': 10,
        'size': (100, 85),
        'image': pygame.image.load("assets/images/enemy1.png"),
        'pool': 3
    }
}

# Define amount of levels in the game, and required kills to reach each level
game_stages = {
    1: {'kills': 0},
    2: {'kills': 5},
    3: {'kills': 15},
}

# Track the current level
current_game_stage = 1

# Define window icon and title
pygame.display.set_caption('Game')  # Replace with your desired window title

# Define colors
gray = (26, 26, 26)

# Get the screen dimensions
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Initialize the position and width of the progress bar
progress_bar_width = 0  # Start with an empty progress bar

# Calculate the center position for the progress bar
progress_bar_x = (screen_width - 1500) // 2  # Centered horizontally
progress_bar_y = 25

# Initialize the main game window (without reinitializing pygame)
mainGameScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
mainGameScreen.fill(gray)

# Semi-transparrent overlay when game is paused/stopped
overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
alpha = 128  # Initial alpha value for semi-transparency

# Initialize player position and velocity
player_x = screen_width/2
player_y = screen_height/2
player_vel_x = 0
player_vel_y = 0
total_player_health = 10
player_shield = 5
player_speed = 4
player_damage = 10
angle = 0

# Keep track of guns, inventory and random drops
current_gun = "small_pistol" # Name of the gun in usage
current_gun_data = guns[current_gun] # Dictionary values of current gun
current_gun_image = pygame.image.load(current_gun_data['file']).convert_alpha() # PNG of current gun
gun_position_x = 0
gun_position_y = 0
draw_random_drop = False # Define if to draw a random drop

# Track guns in inventory, their size in the inventory and position in inventory
inventory = ["small_pistol"]

# Define player speed (pixels moved per frame) and boost speed
boost_speed = 15
boost_bank = 1500
boost_loss = 5

# Globalize jitter effect fo player and displays
jitter_x = 0
jitter_y = 0

# Initialize last shooting time
last_shoot_time = 0
shoot_interval = current_gun_data['speed']  # seconds between shots

# Initialize boost state and acceleration
boosting = False
check_boosting = False
player_acceleration = 0.1  # Base acceleration rate
boost_acceleration = 0.3  # Increased acceleration when boosting

# Initialize clock to control frame rate
clock = pygame.time.Clock()

# Define a list to store bullets
bullets = []
bullet_speed = 20

# Define a list to store enemy objects
enemies = []
enemy_cap = 100

# Define statistics (shows after every game)
enemies_killed = 0
enemies_alive = 0
rounds_played = 0
time_survived = 0
times_boosted = 0

# Damage effect variables
fading = False
fade_rate = 3  # Adjust this value to control the speed of the fade

# Define variables for viewing previous games using CSV file
viewing_previous_games = False # Update logic if viewing previous games
previous_games_page = 5 # Which page if the previous games the user is on
game_stats = [] # List containing every game stat (updates dynamicly)

# Define main game variables
Paused = False # When the game is paused
Game = False # If the game is running (player can move and shoot etc)
Dead = True # Specified version of (Game = False) allows for "new game" display
running = True # Main loop (running = False closes the game)

# Define variables for displaying game stats
stat_animation = False # hinder things from being rendered while animation is ongoing
stat_speed = 15
stat_wait_time = 2 #(secs)
stat_reveal_time = 4 #(secs)
stat_reavealed = True
stat_current_xpos = screen_width/2
stat_enemies_killed = 0 # Becomes font to be displayed
stat_time_survived = 0 # Becomes font to be displayed
stat_times_boosted = 0 # Becomes font to be displayed
stat_score = 0 # Becomes font to be displayed
stat_popup_time = 0

# Damage effect
jitter_active = False
jitter_duration = 0.5  # Duration of the jitter in seconds
jitter_timer = 0  # Tracks how long the jitter has been active
jitter_intensity = 5  # How far the player sprite moves during a jitter
enemy_jitter_intensity = 2  # How far the enemy sprite moves during a jitter

# Define different settings variables
particles_on = True
difficulity = "Normal"
volume = 0.2 # Float bewteen 0 and 1
sound_sfx_on = True
music_on = True
current_music_track_key = None

# Track boosting
space_bar_pressed = False

# Load CSV file for stats (log game statistics)
filename = '/mnt/data/game_stats.csv'

# Global dictionary to hold loaded images
global_images = {}

# Define the volume controll section
volume_knob_xposition = (400*volume+170) # display knob at desired start position (dynamic)
volume_controll_yposition = screen_height - 350
volume_scroller_knob_move = False

# Hovering variables (paused screen)
hover_amplitude = 10  # Max number of pixels the image moves up and down
hover_frequency = 0.5  # How fast the image hovers

# Moves, draws and handles enemy logic
class Enemy:
    def __init__(self, x, y, size, hp, damage, speed, image):
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.image = image # Determine which enemy image to use
        self.jitter_active = False  # Renamed from 'jitter' to 'jitter_active'
        self.jitter_timer = 0
        self.active = True

    def move_towards(self, target_x, target_y):
        global player_x, player_y, enemies_alive

        # Calculate the angle between the enemy and the player
        angle = math.atan2(target_y - self.y, target_x - self.x)

        # Calculate the velocity components based on the angle
        velocity_x = math.cos(angle)
        velocity_y = math.sin(angle)

        # Move the enemy towards the player with a fixed speed
        self.x += self.speed * velocity_x
        self.y += self.speed * velocity_y

        if self.x > player_x - 30 and self.x < player_x + 30 and self.y > player_y - 30 and self.y < player_y + 30:
            if particles_on:
                for i in range(60):
                    # Create new particle
                    particles.append(Particle(position=(self.x, self.y),
                                              velocity=(random.randint(-4, 4), random.randint(-4, 4)),
                                              color=(255, random.randint(100, 150), random.randint(30, 80)),
                                              lifespan=random.randint(20, 40),
                                              radius=random.randint(3, 8)))

            if sound_sfx_on:
                channel = pygame.mixer.find_channel(True)
                if channel:
                    sound_effects['suicide'].play()

            self.active = False
            enemies_alive -= 1
            player_hit()

    def apply_jitter(self):
        if self.jitter_active:
            # Temporarily adjust enemy's position for this frame
            jitter_x = random.randint(-enemy_jitter_intensity, enemy_jitter_intensity)
            jitter_y = random.randint(-enemy_jitter_intensity, enemy_jitter_intensity)
            self.x += jitter_x
            self.y += jitter_y

    def check_hit(self, hostile_x, hostile_y):
        global player_damage, enemies_killed, enemies_alive

        if hostile_x > self.x and hostile_x <= self.x + 30 and hostile_y > self.y and hostile_y < self.y + 30:
            if self.hp <= player_damage:
                self.active = False
                enemies_killed += 1
                enemies_alive -= 1
                check_game_stage()
                print("enemy dead!")
                return True
            else:
                self.hp -= player_damage
                self.jitter_active = True  # Activate jitter effect
                self.jitter_timer = 0.5  # Set how long the jitter effect should last, for example, 0.5 seconds
                self.apply_jitter()  # Correctly call the renamed jitter method

                if sound_sfx_on:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        sound_effects['thud'].play()

    def draw(self, screen):
        mainGameScreen.blit(self.image, (self.x, self.y), (0, 0, self.width, self.height))

# (Dynamic) Handles particles of all colors, sizes and lifespan etc
class Particle:
    def __init__(self, position, velocity, color, lifespan, radius):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.lifespan = lifespan
        self.radius = radius

    def update(self):
        self.position = (self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1])
        self.lifespan -= 1

    def draw(self):
        if self.lifespan > 0:
            pygame.draw.circle(mainGameScreen, self.color, self.position, self.radius)

    def is_dead(self):
        # Check if particle is dead
        return self.lifespan <= 0



# ---------- core game logic section -----------

# Ensures that enemies don't spawn too close to the player
def generate_enemy_position(player_x, player_y, min_distance):
    global running

    while running:
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)

        # Calculate the distance between the enemy spawn position and the player
        distance = math.hypot(x - player_x, y - player_y)

        # Check if the distance is greater than the minimum allowed distance
        if distance >= min_distance:
            return x, y

# (Threaded) Randomly spawns enemies of different variants depending on "game_level"
def enemy_spawning():
    global running, enemies_alive, Game

    while running:
        if Game:
            if enemies_alive < enemy_cap and Paused == False:
                if running:  # Ensure error-free closing of the game
                    pool = [enemy for enemy, attributes in enemy_lib.items() if attributes['pool'] <= current_game_stage]

                    # Prepare lists for the population and weights
                    weights = [enemy_lib[enemy]["rarity"] for enemy in pool]

                    # Select an enemy based on the defined rarity
                    selected_enemy_key = random.choices(pool, weights, k=1)[0]
                    selected_enemy = enemy_lib[selected_enemy_key]

                    # Define variables of the chosen enemy
                    min_spawn_dist = selected_enemy['min_spawn_dist']
                    hp = selected_enemy['hp']
                    spawn_rate = selected_enemy['spawn_rate']
                    damage = selected_enemy['damage']
                    speed = selected_enemy['speed']
                    size = selected_enemy['size']
                    image = selected_enemy['image']


                    print(f"Selected Enemy: {selected_enemy}")
                    print(f"Selected Enemy Spawn Rate: {spawn_rate}")

                if running: # prevent excessive waiting time to shut down after closing game
                    time.sleep(spawn_rate)

                if running: # Ensure error-free closing of the game
                    # Use the latest player position for enemy spawning
                    player_pos = (player_x, player_y)  # Assuming these are updated in the main loop

                    x, y = generate_enemy_position(*player_pos, min_spawn_dist)

                    if Game: # Ensure that the game is still running before spawning
                        # Ensure that access to the enemies list is thread-safe
                        with threading.Lock():
                            enemies.append(Enemy(x, y, size, hp, damage, speed, image))
                            enemies_alive += 1

                        if sound_sfx_on:
                            channel = pygame.mixer.find_channel(True)
                            if channel:
                                sound_effects['woosh3'].play()

                if running: # prevent excessive waiting time to shut down after closing game
                    time.sleep(spawn_rate)

# Random drops include (guns, healing etc)
def random_drop_spawning():
    global running, Game, enemies_killed, guns

    while running:
        time.sleep(random.randint(10,20))

        if Game:
            for _ in guns:
                if guns[_]['level'] == current_game_stage and current_game_stage != 1:
                    print(guns[_])

# Check if hit, and handle death logic.
def player_hit():
    # define global variables
    global player_shield, total_player_health, \
        fading, alpha, jitter_active, jitter_timer, jitter_duration

    # prioritize taking shield first
    if player_shield != 0:
        player_shield -= 1
        total_player_health -= 1
    else: # if player doesn't have
        total_player_health -= 1

    fading = True
    alpha = 220  # Reset to semi-transparent
    if sound_sfx_on:
        channel = pygame.mixer.find_channel(True)
        if channel:
            sound_effects['bass_impact'].play()

    jitter_active = True
    jitter_timer = jitter_duration

    # check if player is dead
    if (total_player_health == 0):

        reset_game()

        if sound_sfx_on:
            channel = pygame.mixer.find_channel(True)
            if channel:
                sound_effects['bass_impact'].play()

# Marks player as "dead" and continues to statistics animation
def reset_game():
    # define global variables
    global player_shield, total_player_health, \
        Dead, Game, enemies, enemies_killed, \
        stat_animation, stat_enemies_killed, \
        stat_popup_time, time_passed, stat_time_survived, \
        time_survived, times_boosted, stat_times_boosted, \
        stat_score, fading, alpha

    Dead = True
    Game = False
    stat_animation = True
    font = pygame.font.Font(None, 36)
    stat_enemies_killed = font.render(f'{enemies_killed} enemies killed!', True, (255, 255, 255))
    stat_time_survived = font.render(f'{math.ceil(time_survived)} seconds survived!', True, (255, 255, 255))
    stat_times_boosted = font.render(f'{times_boosted} times boosted!', True, (255, 255, 255))
    stat_score = font.render(f'score: {math.ceil(time_survived + enemies_killed * 2)}!', True, (255, 255, 255))
    stat_popup_time = time_passed
    toggle_music_off()
    alpha = 128  # Reset to semi-transparent
    fading = False
    update_CSV_file()  # Write new stats into CSV file (offline save)

    # ------ reset all status -----
    for enemy in enemies:
        enemy.active = False
    enemies = []
    enemies_alive = 0

    total_player_health = 10
    player_shield = 5

# Update and log game stats in main CSV file
def update_CSV_file():
    global time_survived, times_boosted, enemies_killed

    score = time_survived + enemies_killed * 2
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Data to write
    data = [
        [math.ceil(score),math.ceil(time_survived), current_date, times_boosted, enemies_killed],
    ]

    filename = r"stats.csv"

    # Open the CSV file for writing
    with open(filename, mode='a', newline='') as file:
        # Create a CSV writer
        csv_writer = csv.writer(file)

        # Write each row
        for row in data:
            csv_writer.writerow(row)

# Define which game stats are to be shown when looking at previous game-stats
def update_viewing_game_stats():
    global game_stats, games, viewing_previous_games

    line_count = 0
    line_count2 = 0
    game_stats = []
    games_per_page = 9

    # iterate each game stat and append to list for better performance
    with open('stats.csv', 'r') as file:
        for line in file:
            line_count += 1

            if line_count > previous_games_page * games_per_page - games_per_page + 1 and line_count <= previous_games_page * games_per_page + 1:
                game_stats.append(line[:-1])
                line_count2 += 1

                font = pygame.font.Font(None, 36)
                stat = font.render(f'{line}', True, (255, 255, 255))

                x_position = screen_width / 2
                y_position = screen_height / 3 + line_count2 * 50
                mainGameScreen.blit(stat, (x_position, y_position))

    print(game_stats)

# Define which game stats are to be shown when looking at previous game-stats
def display_viewing_game_stats():
    pass
# Adds an instance of a bullet/bullets to the "bullets" list
def create_bullet():
    global cursor_x, cursor_y, current_gun_data, gun_position_x, gun_position_y

    # Calculate the angle between player and cursor
    dx = cursor_x - player_x
    dy = cursor_y - player_y
    angle = math.atan2(dy, dx)  # Define 'angle' here
    pellets = current_gun_data['spread']
    spread_angle = current_gun_data['spread_angle']
    amount = current_gun_data['spread']

    # Calculate the tip of the player (triangle) where particles should originate
    tip_distance = 85  # Adjust based on the size of your player sprite
    tip_x = gun_position_x + tip_distance * math.cos(angle)
    tip_y = gun_position_y + tip_distance * math.sin(angle)

    # Create bullet(s)
    for _ in range(amount):
        new_bullet = {
            'x': tip_x,
            'y': tip_y,
            'angle': angle + random.uniform(-spread_angle / 2, spread_angle / 2)
        }
        bullets.append(new_bullet)

    if particles_on:
        for i in range(15):
            # Adjust particles to emit from the tip of the player
            particle_angle = random.uniform(-math.pi / 4, math.pi / 4) + angle
            particle_velocity = (random.randint(-2, 2) + 5 * math.cos(particle_angle),
                                 random.randint(-2, 2) + 5 * math.sin(particle_angle))
            particles.append(Particle(position=(tip_x, tip_y),
                                      velocity=particle_velocity,
                                      color=(255, random.randint(200, 255), 0),
                                      lifespan=random.randint(5, 10),
                                      radius=random.randint(4, 6)))

# Handles player angle, speed and movement logic
def update_player():
    global player_vel_x, player_vel_y, player_acceleration, boost_acceleration, player_x, player_y

    # Update acceleration based on boost state
    acceleration = player_acceleration if not boosting else boost_acceleration

    # Calculate player velocity components with acceleration
    player_vel_x += acceleration * math.cos(angle)
    player_vel_y += acceleration * math.sin(angle)

    # Limit player speed to boost speed
    player_speed_limit = boost_speed if boosting else player_speed
    player_speed_actual = math.hypot(player_vel_x, player_vel_y)
    if player_speed_actual > player_speed_limit:
        factor = player_speed_limit / player_speed_actual
        player_vel_x *= factor
        player_vel_y *= factor

    # Update player position based on velocity
    player_x += player_vel_x
    player_y += player_vel_y

# Handles enemy speed, hp and movement logic
def update_enemy():
    global enemies, Game, Paused

    # Move and draw each active enemy
    for enemy in enemies:
        if enemy.active and Game or Paused:
            if Game:  # Only move the enemy if the game is running

                enemy.move_towards(player_x, player_y)
                if enemy.jitter_active:
                    enemy.apply_jitter()  # Apply jitter if active
                enemy.draw(mainGameScreen)  # Draw the enemy

                if enemy.jitter_active:
                    enemy.jitter_timer -= clock.get_time() / 1000.0  # Decrease jitter timer
                    if enemy.jitter_timer <= 0:
                        enemy.jitter_active = False  # Stop jittering
                    else:
                        enemy.apply_jitter()  # Apply jitter

            enemy.draw(mainGameScreen)

    # Remove inactive enemies (Optional)
    enemies = [enemy for enemy in enemies if enemy.active]

# Calculates gun position and angle based on player position and draws the gun
def update_player_gun():
    global gun_position_x, gun_position_y

    # Draw the rotated player image at the updated position
    draw_player()

    # Distance from the player's center to where the gun should be
    offset_distance = 30  # More realistic distance

    # Adjust angle to position gun to the right of the player
    right_angle_offset = angle + math.pi / 2  # Adding π/2 radians to offset to the right

    # Calculate offset positions with adjusted angle
    offset_x = math.cos(right_angle_offset) * offset_distance
    offset_y = math.sin(right_angle_offset) * offset_distance

    # Rotate the gun image to match the player's rotation
    gun_rotated = pygame.transform.rotate(current_gun_image, math.degrees(-angle))

    # Calculate the new position for the gun, placing it to the right of the player based on the player's rotation
    gun_position_x = player_x + offset_x
    gun_position_y = player_y + offset_y

    # Adjust the gun's rectangle for proper alignment
    gun_rect = gun_rotated.get_rect(center=(gun_position_x, gun_position_y))

    # Blit the rotated gun to the screen at the calculated position
    mainGameScreen.blit(gun_rotated, gun_rect.topleft)

# Function to load images into the global dictionary
def load_images(dictionary):
    global global_images  # Declare the global dictionary
    for key, path in dictionary.items():
        global_images[key] = pygame.image.load(path).convert_alpha()  # Use convert_alpha() for images with transparency

# Apply boosting if possible, increase "boost_bank" etc
def handle_boosting():
    global check_boosting, boost_bank, boosting, boost_loss

    # Decrement boost_bank continuously while boosting and check if it's greater than 0
    if check_boosting:
        if boost_bank > boost_loss:
            boosting = True
            boost_bank -= boost_loss
            if particles_on:
                # Create new particle
                particles.append(Particle(position=(player_x, player_y),
                                          velocity=(
                                          random.randint(-5, 5) - player_vel_x, random.randint(-5, 5) - player_vel_y),
                                          color=(255, random.randint(200, 255), 0),
                                          lifespan=random.randint(10, 30),
                                          radius=random.randint(4, 8)))

        # Increment boost_bank every frame if not boosting and boost_bank is less than 1500
        elif boost_bank <= boost_bank:
            boosting = False
    if space_bar_pressed == False and Game and boost_bank < 1500:
        boost_bank += 2

# Resets variables, player health, volume etc
def start_new_game():
    global Game, Dead, Paused, rounds_played, stat_current_xpos, screen_width, enemies_killed, \
        time_survived, times_boosted, sound_effects, music_on, fading, stat_reavealed

    # display "ascend" option
    Game = True
    Dead = False
    Paused = False

    rounds_played += 1
    stat_current_xpos = screen_width / 2
    enemies_killed = 0
    time_survived = 0
    times_boosted = 0

    if sound_sfx_on:
        channel = pygame.mixer.find_channel(True)
        if channel:
            sound_effects['woosh2'].play()

    time.sleep(.3)
    reset_track_volume_to_original("drone_sound")
    manage_menu_sound()

    if music_on == False:
        toggle_music_off()

    stat_reavealed = False
    fading = True

# Check if the player has rached a new stage, and update accordingly
def check_game_stage():
    global enemies_killed, game_stages, current_game_stage

    if current_game_stage < len(game_stages): # Check if the max level is reached
        if enemies_killed >= game_stages[current_game_stage+1]['kills']:
            current_game_stage += 1
            print(f"changes game_state to: {current_game_stage}")
    else:
        print("Max level reached!")



# ---------- music/volume section -----------

def adjust_sound_effects_volume(volume):
    for sound_effect in sound_effects.values():
        sound_effect.set_volume(volume)

def set_volume(sent_volume):
    global volume
    volume = sent_volume
    # Only adjust volume if there's a track currently playing or selected
    if current_music_track_key and pygame.mixer.music.get_busy():
        # Apply the new volume to the currently playing track
        track_info = music.get(current_music_track_key)
        if track_info:
            effective_volume = track_info['base_volume'] * volume
            pygame.mixer.music.set_volume(effective_volume)

def play_music(track_key):
    global current_music_track_key
    current_music_track_key = track_key  # Update the current track key
    track_info = music.get(track_key)
    if track_info:
        pygame.mixer.music.load(track_info['file'])
        effective_volume = track_info['base_volume'] * volume
        pygame.mixer.music.set_volume(effective_volume)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    else:
        print(f"Music track {track_key} not found.")

def switch_track(new_track_key):
    pygame.mixer.music.stop()  # Stop the current track
    play_music(new_track_key)  # Play the new track

def change_track_volume(track_key, volume):
    if track_key in music:
        music[track_key]['volume'] = volume
        # If this track is currently playing, update the volume immediately
        if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > -1:
            pygame.mixer.music.set_volume(volume)
            print("changed track volume!")

def adjust_track_volume_quieter(track_key, adjustment_factor):
    global music, current_music_track_key, volume

    if track_key in music:
        # Apply an adjustment factor to decrease the base volume
        new_base_volume = music[track_key]['base_volume'] * adjustment_factor

        # Ensure the new volume does not exceed 1.0
        new_base_volume = max(0, min(new_base_volume, 1.0))

        # Update the track's base volume
        music[track_key]['base_volume'] = new_base_volume

        # If the track is currently playing, adjust its volume
        if current_music_track_key == track_key and pygame.mixer.music.get_busy():
            effective_volume = new_base_volume * volume
            pygame.mixer.music.set_volume(effective_volume)
            print(f"Adjusted volume for {track_key}. New effective volume: {effective_volume}")
    else:
        print(f"Track {track_key} not found.")

def adjust_track_volume_louder(track_key, adjustment_factor):
    global music, current_music_track_key, volume

    if track_key in music:
        # Apply an adjustment factor to increase the base volume
        new_base_volume = music[track_key]['base_volume'] * adjustment_factor

        # Ensure the new volume does not exceed 1.0
        new_base_volume = max(0, min(new_base_volume, 1.0))

        # Update the track's base volume
        music[track_key]['base_volume'] = new_base_volume

        # If the track is currently playing, adjust its volume
        if current_music_track_key == track_key and pygame.mixer.music.get_busy():
            effective_volume = new_base_volume * volume
            pygame.mixer.music.set_volume(effective_volume)
            print(f"Adjusted volume for {track_key}. New effective volume: {effective_volume}")
    else:
        print(f"Track {track_key} not found.")

def reset_track_volume_to_original(track_key):
    if track_key in music:
        music[track_key]['base_volume'] = music[track_key]['original_volume']
        if current_music_track_key == track_key and pygame.mixer.music.get_busy():
            effective_volume = music[track_key]['base_volume'] * volume
            pygame.mixer.music.set_volume(effective_volume)
            print(f"Reset volume for {track_key} to original. Effective volume: {effective_volume}")
    else:
        print(f"Track {track_key} not found.")

def toggle_music_on():
    #if pygame.mixer.music.get_busy():
    pygame.mixer.music.unpause()  # Resume the music if it's paused
    #else:
    #    play_music(current_music_track_key)  # Play the music if it's not playing at all
    print("Music resumed")

def toggle_music_off():
    pygame.mixer.music.pause()  # Pauses the music without stopping it completely
    print("Music paused")

# Function to manage sound based on game state
def manage_menu_sound():
    global Paused, Dead, sound_sfx_on

    if Paused or Dead:
        sound_effects['drone_sound'].play(-1)  # Loop the sound indefinitely
    else:
        sound_effects['drone_sound'].stop()

    if sound_sfx_on == False:
        sound_effects['drone_sound'].stop()

    print("manage menu sound")



# ---------- drawing section -----------

def draw_bullets():

    for bullet in bullets:
        bullet['x'] += bullet_speed * math.cos(bullet['angle'])
        bullet['y'] += bullet_speed * math.sin(bullet['angle'])

        # Check if the bullet hits any enemy
        for enemy in enemies:
            if enemy.active and enemy.check_hit(bullet['x'], bullet['y']):
                if particles_on:
                    for i in range(30):
                        # Create new particle
                        particles.append(Particle(position=(enemy.x, enemy.y),
                                                  velocity=(random.randint(-3, 3), random.randint(-3, 3)),
                                                  color=(255, random.randint(100, 150), random.randint(30, 80)),
                                                  lifespan=random.randint(10, 20),
                                                  radius=random.randint(4, 7)))

                if sound_sfx_on:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        sound_effects['explosion'].play()

        # Check if the bullet is out of bounds
        if bullet['x'] < 0 or bullet['x'] > screen_width or bullet['y'] < 0 or bullet['y'] > screen_height:
            if particles_on:
                for i in range(30):
                    # Create new particle
                    particles.append(Particle(position=(bullet['x'], bullet['y']),
                                              velocity=(random.randint(-1, 1), random.randint(-1, 1)),
                                              color=(255, random.randint(150, 250), 0),
                                              lifespan=random.randint(10, 20),
                                              radius=random.randint(2, 5)))

            if sound_sfx_on:
                channel = pygame.mixer.find_channel(True)
                if channel:
                    sound_effects['thud'].play()

            bullets.remove(bullet)
        else:
            # Rotate the bullet image based on the bullet's angle
            bullet_rotated = pygame.transform.rotate(global_images["bullet_image"], math.degrees(-bullet['angle']))
            bullet_rect = bullet_rotated.get_rect()
            bullet_rect.center = (bullet['x'], bullet['y'])
            mainGameScreen.blit(bullet_rotated, bullet_rect.topleft)

def draw_player():
    player_rotated = pygame.transform.rotate(global_images["playerImage"], math.degrees(-angle))
    player_rect = player_rotated.get_rect()
    player_rect.center = (player_x, player_y)
    mainGameScreen.blit(player_rotated, player_rect.topleft)

def draw_pointer():
    if player_x < 0:
        pointer_rotated = pygame.transform.rotate(global_images["pointer_image"], 180)
        mainGameScreen.blit(pointer_rotated, (10, player_y), (0, 0, 30, 30))
    elif player_x > screen_width:
        mainGameScreen.blit(global_images["pointer_image"], (screen_width - 40, player_y), (0, 0, 30, 30))
    elif player_y < 0:
        pointer_rotated = pygame.transform.rotate(global_images["pointer_image"], 90)
        mainGameScreen.blit(pointer_rotated, (player_x, 10), (0, 0, 30, 30))
    elif player_y > screen_height:
        pointer_rotated = pygame.transform.rotate(global_images["pointer_image"], 270)
        mainGameScreen.blit(pointer_rotated, (player_x, screen_height - 40), (0, 0, 30, 30))

def draw_menu():
    # Display particle and sounds sfx options in menu
    if particles_on:
        mainGameScreen.blit(global_images["particles_on_image"], (100, screen_height - 100), (0, 0, 500, 100))
    else:
        mainGameScreen.blit(global_images["particles_off_image"], (100, screen_height - 100), (0, 0, 500, 100))

    if sound_sfx_on:
        mainGameScreen.blit(global_images["sound_sfx_on_image"], (100, screen_height - 200), (0, 0, 500, 100))
    else:
        mainGameScreen.blit(global_images["sound_sfx_off_image"], (100, screen_height - 200), (0, 0, 500, 100))

    if music_on:
        mainGameScreen.blit(global_images["music_on_image"], (100, screen_height - 300), (0, 0, 500, 100))
    else:
        mainGameScreen.blit(global_images["music_off_image"], (100, screen_height - 300), (0, 0, 500, 100))

    # Displaying volume status icon
    if volume > .66:
        mainGameScreen.blit(global_images["volume_icon_high"], (100, volume_controll_yposition - 15), (0, 0, 500, 100))
    elif volume > .33:
        mainGameScreen.blit(global_images["volume_icon_medium"], (100, volume_controll_yposition - 15), (0, 0, 500, 100))
    elif volume < .33 and volume > 0:
        mainGameScreen.blit(global_images["volume_icon_low"], (100, volume_controll_yposition - 15), (0, 0, 500, 100))
    else:
        mainGameScreen.blit(global_images["volume_icon_off"], (100, volume_controll_yposition - 15), (0, 0, 500, 100))

    # Displaying volume bar and knob
    mainGameScreen.blit(global_images["volume_scroller_bar"], (170, volume_controll_yposition), (0, 0, 500, 100))
    mainGameScreen.blit(global_images["volume_scroller_bar_overlay"], (170, volume_controll_yposition), (0, 0, volume * 400 + 15, 100))
    mainGameScreen.blit(global_images["volume_scroller_knob"], (volume_knob_xposition, volume_controll_yposition - 9), (0, 0, 500, 100))

def draw_heart():
    global total_player_health, jitter_y, jitter_x, global_images

    # Draw hearts and shield hearts and apply jitter effect if it's on
    for _ in range(total_player_health):
        if Paused == False:
            hover_offset = math.sin(time_passed * hover_frequency) * 4
        else:
            hover_offset = 0  # remove animation when the game is paused

        # Space out each heart accordingly
        position = _ * 55 + 210

        # Add jitter effect to each heart if it's active
        if jitter_active:
            hover_offset += jitter_y
            position += jitter_x

        # Decide if a "shield_heart" of a "full_heart" should be drawn
        if _ < total_player_health - player_shield:
            mainGameScreen.blit(global_images["full_heart"], (position, hover_offset + 70), (0, 0, 40, 40))
        else:
            mainGameScreen.blit(global_images["shield_heart"], (position, hover_offset + 70), (0, 0, 40, 40))

def display_stats():
    # Display stats after death
    text_rect = stat_enemies_killed.get_rect()
    x_position = stat_current_xpos - text_rect.width / 2
    mainGameScreen.blit(stat_enemies_killed, (x_position, screen_height / 2 + 300))

    text_rect = stat_time_survived.get_rect()
    x_position = stat_current_xpos - text_rect.width / 2
    mainGameScreen.blit(stat_time_survived, (x_position, screen_height / 2 + 350))

    text_rect = stat_times_boosted.get_rect()
    x_position = stat_current_xpos - text_rect.width / 2
    mainGameScreen.blit(stat_times_boosted, (x_position, screen_height / 2 + 400))

    text_rect = stat_score.get_rect()
    x_position = stat_current_xpos - text_rect.width / 2
    mainGameScreen.blit(stat_score, (x_position, screen_height / 2 + 450))

    mainGameScreen.blit(global_images["game_stats"], (stat_current_xpos - 150, screen_height / 2 + 200))

def display_close_icon():
    global running

    mainGameScreen.blit(global_images["close_icon_image"], (screen_width - 60, 20), (0, 0, 40, 40))
    # Logic for closing the game using "close" option
    if cursor_x > screen_width - 60 and cursor_x < screen_width - 20 and cursor_y > 20 and cursor_y < 60:
        mainGameScreen.blit(global_images["red_close_icon_image"], (screen_width - 60, 20), (0, 0, 40, 40))
        if event.type == pygame.MOUSEBUTTONDOWN:
            running = False
    else:
        mainGameScreen.blit(global_images["close_icon_image"], (screen_width - 60, 20), (0, 0, 40, 40))

# Display progress bar (player boost left)
def display_progress_bar():
    global jitter_active, global_images, progress_bar_x, progress_bar_y, jitter_x, jitter_y, boost_bank, boosting
    rect_width = 200
    rect_height = 12
    rect_x = player_x - rect_width/2
    rect_y = player_y - 100

    rect2_max_width = boost_bank/1500
    rect2_width = rect_width*rect2_max_width

    # apply jitter effect (if it's activated) and draw "progress_bar" or "player_boost_bank"
    if boosting or boost_bank < 1500: # only display "progress_bar" when boosting
        if jitter_active:
            pygame.draw.rect(mainGameScreen, (179, 71, 0), (rect_x + jitter_x, rect_y + jitter_y, rect_width, rect_height))
            pygame.draw.rect(mainGameScreen, (255, 128, 0), (rect_x + jitter_x, rect_y + jitter_y, rect2_width, rect_height))
        else:
            pygame.draw.rect(mainGameScreen, (179, 71, 0), (rect_x, rect_y, rect_width, rect_height))
            pygame.draw.rect(mainGameScreen, (255, 128, 0), (rect_x, rect_y, rect2_width, rect_height))

def draw_random_drop():


    mainGameScreen.blit(gun_rotated, gun_rect.topleft)


# Create and start threading
enemy_spawning_thread = threading.Thread(target=enemy_spawning)
enemy_spawning_thread.start()

random_drop_thread = threading.Thread(target=random_drop_spawning)
random_drop_thread.start()


# Particle list
particles = []

# Ensure right master volume at startup
set_volume(volume)

# Load the images
load_images(images) # Loading the main dicitionary

# Initiate setteling drone sound at startup
manage_menu_sound()

while running:
    mainGameScreen.fill(gray)

    current_time = time.time()
    time_passed = pygame.time.get_ticks() / 100  # Get time in seconds

    # Handle input events
    for event in pygame.event.get():
        cursor_x, cursor_y = pygame.mouse.get_pos()  # Only update cursor position when moving

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to open menu
                if Dead == False:
                    if Paused:
                        Paused = False
                        fading = True
                        alpha = 128  # Reset to semi-transparent
                        Game = True
                        reset_track_volume_to_original("drone_sound")
                        manage_menu_sound()
                    elif Paused == False:
                        Paused = True
                        Game = False
                        toggle_music_off()

                    if sound_sfx_on:
                        manage_menu_sound()

            elif event.key == pygame.K_SPACE:  # Press SPACE to boost
                if Game:
                    check_boosting = True
                    space_bar_pressed = True
                    if boost_bank > boost_loss:
                        times_boosted += 1

            elif event.key == pygame.K_s:  # display previous game stats
                if Paused or Dead:
                    # Decide to display or hide previous game-stats
                    if viewing_previous_games:
                        viewing_previous_games = False
                    else:
                        # When opening previous game-stats menu
                        viewing_previous_games = True
                        print("updating game stats...")
                        update_viewing_game_stats()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:  # Release SPACE to stop boosting
                player_acceleration = 0.1
                boosting = False
                check_boosting = False
                space_bar_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if stat_animation == False:
                    if Game:
                        # Check if enough time has passed since the last shot
                        if current_time - last_shoot_time > shoot_interval / 10:
                            create_bullet()
                            last_shoot_time = current_time  # Update the last shooting time

                    # when the game is paused
                    elif Paused or Dead and stat_animation == False and viewing_previous_games == False:

                        # If the cursor hovers over "particles" option in settings
                        if cursor_x > 100 and cursor_x < 600 and cursor_y > screen_height-100 and cursor_y < screen_height-17:
                            if particles_on:
                                particles_on = False
                            else:
                                particles_on = True

                            if sound_sfx_on:
                                channel = pygame.mixer.find_channel(True)
                                if channel:
                                    sound_effects['click'].play()

                        # If the cursor hovers over "sound_sfx" option in settings
                        elif cursor_x > 100 and cursor_x < 600 and cursor_y > screen_height-200 and cursor_y < screen_height-117:
                            if sound_sfx_on:
                                sound_sfx_on = False
                                manage_menu_sound()
                            else:
                                sound_sfx_on = True
                                manage_menu_sound()

                            if sound_sfx_on:
                                channel = pygame.mixer.find_channel(True)
                                if channel:
                                    sound_effects['click'].play()

                        # If the cursor hovers over "music" option in settings
                        elif cursor_x > 100 and cursor_x < 600 and cursor_y > screen_height-300 and cursor_y < screen_height-217:
                            if music_on:
                                music_on = False
                                toggle_music_off()
                            else:
                                music_on = True
                                toggle_music_on()

                            if sound_sfx_on:
                                channel = pygame.mixer.find_channel(True)
                                if channel:
                                    sound_effects['click'].play()

                        # If cursor is over volume control section
                        elif cursor_x > 150 and cursor_x < 600 and cursor_y > volume_controll_yposition-30 and cursor_y < volume_controll_yposition+30:
                            volume_scroller_knob_move = True

                    if Dead and viewing_previous_games == False:
                        # If cursor is over "ascend" button (starts a new game)
                        if cursor_x > screen_width/2-250 and cursor_x < screen_width/2+250 and cursor_y > screen_height/2 and cursor_y < screen_height/2+167:
                            start_new_game()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                volume_scroller_knob_move = False # Ensure the volume slider doesn't change when not clicked

        # Move the volume slider when clicking and dragging on the knob
        if volume_scroller_knob_move:
            # Calculate the desired x-position based on the cursor's position
            desired_xposition = cursor_x - 15

            # Clamp the x-position to make sure it's within the bounds of the volume bar
            volume_knob_xposition = max(170, min(desired_xposition, 570))

            volume = (volume_knob_xposition - 170) / 400
            set_volume(volume)  # Assuming set_volume updates the music volume
            adjust_sound_effects_volume(volume)  # Update sound effects volume


# ---------- While the game is active (player is moving etc) -------------
    if Game:
        # Apply boost if available and refill boost accordingly
        handle_boosting()

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw()
            if particle.is_dead():
                particles.remove(particle)

        # Calculate the angle between player and cursor
        dx = cursor_x - player_x
        dy = cursor_y - player_y
        angle = math.atan2(dy, dx)

        # Increase time survived for stats
        time_survived += 1/144

        # Handle player angle, speed and movement logic
        update_player()


#-------------------------  drawing to screen and handling position data --------------------------

        draw_bullets()
        draw_pointer()

    # Handle enemy speed, hp, movement logic and drawing
    update_enemy()

    if Dead == False: # (active or paused)

        # Calculate gun position and angle based on player position and draw the gun
        update_player_gun()

        # Draw each heart under "progress_bar" or "player_boost_bank" display
        draw_heart()

        # Display the "progress_bar" or "player_boost_bank" display on the top of the display
        display_progress_bar()

    # Fade effect
    if fading:
        alpha -= fade_rate
        if alpha <= 0:
            alpha = 0
            fading = False  # Stop fading once fully transparent
        overlay.fill((0, 0, 0, alpha))
        if alpha > 0:
            mainGameScreen.blit(overlay, (0, 0))  # Draw the overlay

    # Calculate jitter effect
    if jitter_active:
        jitter_timer -= clock.get_time() / 1000.0  # Decrease timer based on frame time

        if jitter_timer <= 0:
            jitter_active = False  # Stop jittering when time runs out
        else:
            # Calculate jitter
            jitter_x = random.randint(-jitter_intensity, jitter_intensity)
            jitter_y = random.randint(-jitter_intensity, jitter_intensity)

            # Temporarily adjust player's position for this frame
            player_x += jitter_x
            player_y += jitter_y



        #-------------- If game is paused or players has died --------------
    if Paused or Dead:
        # Calculate the new y position to make the menu title hover
        hover_offset = math.sin(time_passed * hover_frequency) * hover_amplitude

        # Darken screen when paused or dead
        alpha = 128
        overlay.fill((0, 0, 0, alpha))
        mainGameScreen.blit(overlay, (0, 0))  # Draw the overlay

        if Paused:
            mainGameScreen.blit(global_images["paused_text"], (screen_width / 2 - 500, hover_offset), (0, 0, 1000, 330))

        # Display game title when player isn't alive
        elif Dead:
            if stat_animation == False:
                if viewing_previous_games == False:
                    # display "ascend" option in light color when hovering over it
                    if cursor_x > screen_width / 2 - 150 and cursor_x < screen_width / 2 + 150 and cursor_y > screen_height / 2 and cursor_y < screen_height / 2 + 100:
                        mainGameScreen.blit(global_images["ascend_hover_image"], (screen_width / 2 - 150, screen_height / 2), (0, 0, 500, 167))
                    else:
                        mainGameScreen.blit(global_images["ascend_image"], (screen_width / 2 - 150, screen_height / 2), (0, 0, 500, 167))

            mainGameScreen.blit(global_images["game_image"], (screen_width / 2 - 400, hover_offset), (0, 0, 1000, 330))

        # only draw menu if statistics animation is not running
        if stat_animation == False:
            if viewing_previous_games == False:
                draw_menu()

        # Move previous game statistics when allowed
        if time_passed - stat_popup_time > stat_wait_time*10 and Dead:
            if stat_current_xpos < screen_width-200:
                stat_current_xpos += stat_speed

        # Stops movement of previous game statistics
        if time_passed - stat_popup_time > stat_reveal_time*10 and Dead and stat_reavealed == False:
            stat_animation = False
            if sound_sfx_on:
                channel = pygame.mixer.find_channel(True)
                if channel:
                    sound_effects['woosh1'].play()
                manage_menu_sound()

            stat_reavealed = True

        # Display stats if any games have been played
        if rounds_played > 0 and Dead:
            display_stats() # Display previosu game statistics at bottom right corner in menu


    # ---------------- Constant displays ----------------
    display_close_icon()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(144)  # Set the frame rate to 144 frames per second

print(f"{enemies_killed} enemies killed")
print(f"{enemies_alive} enemies alive")
print(f"{rounds_played} rounds_played")
print(f"{times_boosted} times boosted")

pygame.quit()
sys.exit()