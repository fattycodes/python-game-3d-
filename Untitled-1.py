from panda3d.core import Point3, Vec3, LVector3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight, WindowProperties
import math

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the default camera control
        self.disableMouse()

        # Set up the window properties to capture the mouse
        props = WindowProperties()
        props.setCursorHidden(True)  # Hide the mouse cursor
        self.win.requestProperties(props)

        # Load the environment model and set its scale
        self.environment = self.loader.loadModel("models/environment")
        self.environment.reparentTo(self.render)
        self.environment.setScale(2, 2, 2)
        self.environment.setPos(-8, 42, 0)

        # Create a player (a simple cube)
        self.player = self.loader.loadModel("models/box")
        self.player.setScale(2, 2, 4)
        self.player.setPos(0, 10, 0)
        self.player.reparentTo(self.render)

        # Add lighting
        self.add_lighting()

        # Movement variables
        self.movement_speed = 30  # Movement speed of the player
        self.jump_force = 30  # Initial upward force for jumping
        self.gravity = -50  # Gravity effect
        self.vertical_velocity = 0  # Current vertical velocity
        self.is_jumping = False  # Jump state
        self.player_velocity = Vec3(0, 0, 0)  # Velocity of the player
        self.is_moving = {"w": False, "s": False, "a": False, "d": False}  # Movement status
        dlight2 = DirectionalLight('dlight2')
        dlight2.setColor((0.5, 0.5, 0.5, 1))
        dlight2.setDirection(Vec3(0, 8, -2))
        dlight_node2 = self.render.attachNewNode(dlight2)
        self.render.setLight(dlight_node2)        
        # Camera control variables
        self.camera_sensitivity = 10.0  # Adjust this value as needed
        self.pitch = 0  # Vertical camera angle (up/down)
        self.yaw = 0    # Horizontal camera angle (left/right)
        

        # Set camera position to be at the player's height
        self.camera.reparentTo(self.player)  # Make the camera a child of the player
        self.camera.setPos(0, 0, 2)  # Position the camera at the player's eye level

        # Keyboard controls to move the player
        self.accept("w", self.start_moving, ["s"])
        self.accept("s", self.start_moving, ["w"])
        self.accept("a", self.start_moving, ["d"])
        self.accept("d", self.start_moving, ["a"])
        self.accept("space", self.jump)  # Jump when space is pressed

        # Stop movement when keys are released
        self.accept("w-up", self.stop_moving, ["s"])
        self.accept("s-up", self.stop_moving, ["w"])
        self.accept("a-up", self.stop_moving, ["d"])
        self.accept("d-up", self.stop_moving, ["a"])

        # Set up the task to update movement and camera
        self.taskMgr.add(self.update_movement, "UpdateMovementTask")
        self.taskMgr.add(self.mouse_look, "MouseLookTask")

    def add_lighting(self):
        # Add a directional light
        dlight = DirectionalLight('dlight')
        dlight.setDirection(Vec3(0, 8, -2))
        dlight_node = self.render.attachNewNode(dlight)
        self.render.setLight(dlight_node)

    def start_moving(self, key):
        self.is_moving[key] = True

    def stop_moving(self, key):
        self.is_moving[key] = False

    def jump(self):
        if not self.is_jumping:  # Only allow jumping if not already in the air
            self.vertical_velocity = self.jump_force
            self.is_jumping = True

    def update_movement(self, task):
        # Delta time for smooth movement
        dt = globalClock.getDt()

        # Reset player velocity
        self.player_velocity.set(0, 0, 0)

        # Calculate the direction based on yaw
        direction = LVector3()
        direction.setX(math.sin(math.radians(self.yaw)))
        direction.setY(-math.cos(math.radians(self.yaw)))

        # Normalize the direction vector
        direction.normalize()

        # Apply movement based on the keys pressed
        if self.is_moving["w"]:
            self.player_velocity += direction * self.movement_speed * dt  # Move forward
        if self.is_moving["s"]:
            self.player_velocity -= direction * self.movement_speed * dt  # Move backward
        if self.is_moving["a"]:
            # Rotate 90 degrees to move left
            left_direction = LVector3(-direction.getY(), direction.getX(), 0)
            self.player_velocity += left_direction * self.movement_speed * dt  # Move left
        if self.is_moving["d"]:
            # Rotate -90 degrees to move right
            right_direction = LVector3(direction.getY(), -direction.getX(), 0)
            self.player_velocity += right_direction * self.movement_speed * dt  # Move right

        # Apply gravity and update vertical velocity
        if self.is_jumping:
            self.vertical_velocity += self.gravity * dt  # Apply gravity
            self.player_velocity.setZ(self.vertical_velocity * dt)  # Move vertically

        # Check if the player is on the ground (you might need to adjust this logic for your specific setup)
        if self.player.getZ() <= 0:
            self.player.setZ(0)  # Reset to ground level
            self.vertical_velocity = 0  # Reset vertical velocity
            self.is_jumping = False  # Allow jumping again

        # Update the player's position based on the velocity
        self.player.setPos(self.player.getPos() + self.player_velocity)

        return Task.cont

    def mouse_look(self, task):
        # Get the current mouse position (returns None if the mouse is outside the window)
        if self.mouseWatcherNode.hasMouse():
            # Get mouse movement
            mouse_x = self.mouseWatcherNode.getMouseX()
            mouse_y = self.mouseWatcherNode.getMouseY()

            # Rotate the camera horizontally (yaw) based on mouse X-axis movement
            self.yaw -= mouse_x * self.camera_sensitivity

            # Update the vertical camera angle (pitch), and clamp it to avoid excessive vertical rotation
            self.pitch += mouse_y * self.camera_sensitivity
            self.pitch = max(-89, min(89, self.pitch))  # Constrain pitch between -89 and 89 degrees

            # Set the camera's orientation
            self.camera.setH(self.yaw)     # Set the yaw for horizontal look
            self.camera.setP(self.pitch)   # Set the pitch for vertical look

            # Reset mouse to the center of the screen after each frame to capture relative movement
            self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)

        return Task.cont

# Create the game instance and run the game
game = MyGame()
game.run()
