"""Warning! Here be dragons.

This was thrown together lazily based on a vague memory of how to do
this sort of rendering. It's very slow. It's not very pretty. It's
not very well documented. It's not very well tested. It's not very
well thought out. It's not very well anything. It's just a quick
hack to get something working.
"""

import pygame
import numpy as np
from math import sin, cos, pi
from typing import Tuple, Union, Optional, List

pygame.init()
window = pygame.display.set_mode((1100, 800))
clock = pygame.time.Clock()

Number = Union[int, float]
Color = Tuple[int, int, int]

eyes = [
    ["200", "231", "010", "143", "222", "023", "300", "104", "044", "221", "132", "240", "231", "222", "112", "024", "311", "013", "030", "303", "002", "104", "023", "144", "001", "310", "312", "130", "223", "311", "041", "034", "000", "130", "201", "230", "101", "024", "041", "240", "142", "134", "143", "132", "034", "143", "023", "142", "034", "144", "242", "111", "010", "044", "003", "133", "214", "232", "113", "144", "131", "220", "041", "101", "110", "010", "100", "040", "241", "021", "244", "211", "004", "244", "034", "241", "004", "201", "131", "133", "310", "242", "204", "223", "304", "311", "030", "031", "134", "111", "110", "022", "113", "212", "103", "023", "224", "133", "143" ],
    ["310", "231", "010", "143", "222", "023", "300", "104", "044", "221", "132", "240", "231", "222", "112", "024", "311", "013", "030", "303", "002", "104", "023", "144", "001", "104", "021", "110", "202", "311", "041", "034", "000", "100", "101", "204", "040", "024", "041", "240", "142", "134", "143", "132", "034", "143", "023", "142", "034", "144", "134", "101", "214", "302", "224", "133", "304", "103", "242", "224", "001", "110", "243", "043", "232", "011", "113", "100", "224", "311", "233", "141", "032", "121", "023", "032", "041", "233", "023", "014", "141", "232", "212", "114", "222", "312", "030", "020", "243", "222", "002", "021", "230", "242", "122", "134", "020", "133", "233", "222", "014", "114", "033" ],
    ["121", "231", "010", "143", "222", "023", "300", "104", "044", "221", "132", "240", "231", "222", "112", "024", "311", "013", "030", "303", "002", "104", "023", "144", "001", "234", "301", "202", "014", "143", "231", "310", "042", "224", "212", "130", "144", "303", "003", "031", "211", "034", "142", "130", "310", "011", "023", "224", "104", "144", "224", "223", "011", "144", "111", "023", "031", "020", "140", "044", "101", "302", "020", "220", "311", "221", "114", "204", "240", "041", "030", "004", "231", "302", "132", "122", "110", "042", "000", "021", "131", "242", "212", "040", "043", "212", "230", "131", "043", "033", "242", "132", "010", "003", "101", "303", "013", "010", "204", "140", "302", "100", "224", "221", "031", "134", "204", "201", "040", "223", "100", "021", "101", "140", "203", "220", "123", "114" ],
    ["301", "231", "010", "144", "300", "204", "234", "141", "112", "001", "132", "220", "101", "143", "200", "310", "112", "044", "210", "221", "142", "022", "041", "022", "144", "204", "114", "100", "121", "030", "211", "210", "040", "014", "013", "222", "023", "312", "014", "134", "104", "220", "203", "312", "132", "310", "010", "133", "241", "003", "310", "302", "142", "303", "114", "100", "222", "033", "020", "144", "222", "224", "202", "311", "021", "231", "222", "023", "142", "032", "202", "240", "101", "043", "112", "111", "224", "043", "120", "112", "200", "011", "001", "100", "013", "122", "142", "133", "101", "301", "230", "233", "310", "032", "012", "140", "223", "024", "203", "223", "220", "031" ],
    ["223", "231", "010", "144", "300", "204", "002", "220", "104", "130", "303", "142", "220", "300", "232", "241", "220", "002", "230", "012", "142", "024", "140", "244", "214", "131", "310", "023", "220", "023", "311", "042", "120", "200", "130", "124", "002", "214", "143", "111", "301", "002", "310", "300", "001", "211", "232", "021", "041", "013", "130", "230", "140", "300", "210", "124", "220", "132", "023", "003", "042", "212", "002", "011", "213", "014", "240", "001", "213", "211", "223", "233", "100", "304", "012", "040", "034", "224", "002", "231", "243", "110", "241", "031", "022", "110", "230", "122", "040", "023", "042", "223", "033", "141", "224", "214", "131", "311", "312", "042", "303", "121", "142", "032", "004", "011", "032", "010", "121", "304", "223", "001", "224", "234", "030", "133", "004", "213", "211", "111", "024", "224", "213", "033", "134", "303", "234", "001", "000", "141", "040", "241", "243", "100", "120", "013", "044" ],
    ["114", "231", "010", "144", "300", "204", "043", "244", "021", "023", "103", "101", "034", "143", "232", "212", "122", "220", "114", "103", "244", "020", "032", "112", "021", "033", "034", "133", "034", "311", "132", "004", "222", "014", "141", "144", "112", "201", "301", "213", "004", "133", "142", "032", "232", "304", "041", "112", "134", "031", "110", "122", "101", "103", "131", "233", "212", "114", "201", "020", "234", "240", "013", "011", "141", "133", "033", "124", "142", "133", "030", "023", "113", "110", "120", "222", "122", "000", "122", "010", "123", "210", "122", "023", "130", "100", "014", "041", "021", "224", "010", "304", "132", "233", "021", "241", "021", "143", "003", "232", "221", "130", "042", "024", "120", "200", "221", "124", "021", "002", "231", "144", "201", "203", "032", "243", "121", "300", "244", "204", "044", "110", "204", "240" ],
    ["102", "231", "010", "144", "300", "204", "002", "220", "104", "130", "002", "210", "014", "030", "214", "033", "233", "003", "121", "010", "142", "302", "134", "123", "001", "033", "103", "301", "004", "114", "220", "223", "213", "310", "032", "204", "304", "300", "143", "204", "210", "034", "222", "224", "024", "142", "201", "240", "300", "010", "021", "142", "140", "213", "233", "234", "304", "100", "123", "140", "243", "142", "233", "200", "114", "140", "303", "101", "304", "212", "004", "211", "042", "220", "033", "300", "133", "220", "214", "232", "223", "132", "144", "113", "130", "230", "304", "302", "012", "003", "101", "222", "111", "303", "101", "212", "234", "130", "004", "043", "101", "023", "232", "132", "123", "242", "021", "124", "230", "220", "100", "011", "310", "231", "233", "302", "214", "303", "034" ],
    ["302", "231", "010", "144", "300", "204", "002", "220", "104", "130", "002", "210", "014", "030", "214", "033", "233", "003", "121", "010", "142", "220", "041", "310", "001", "242", "210", "031", "312", "120", "212", "034", "001", "231", "033", "102", "124", "032", "244", "311", "124", "024", "303", "000", "100", "230", "133", "231", "224", "123", "311", "043", "044", "200", "212", "110", "241", "300", "101", "233", "204", "212", "211", "200", "241", "243", "024", "041", "013", "112", "101", "223", "010", "122", "034", "133", "231", "142", "203", "114", "231", "043", "243", "111", "204", "123", "302", "232", "021", "223", "304", "011", "042", "041", "201", "234", "244", "041", "010", "032", "232", "122", "104", "041", "220", "024", "312", "134", "110", "004", "040", "132", "120", "001", "111", "204", "141", "040", "130", "110" ],
    ["113", "231", "010", "144", "300", "204", "002", "220", "104", "130", "002", "210", "014", "030", "214", "033", "233", "003", "121", "010", "142", "113", "041", "214", "134", "033", "103", "301", "214", "114", "220", "223", "304", "102", "022", "204", "010", "144", "143", "204", "210", "202", "222", "242", "234", "020", "212", "042", "213", "143", "232", "203", "012", "114", "112", "110", "111", "034", "101", "013", "114", "141", "012", "110", "241", "210", "114", "300", "204", "014", "011", "220", "010", "043", "100", "140", "132", "310", "100", "022", "042", "301", "040", "201", "222", "041", "130", "014", "131", "020", "134", "243", "013", "113", "240", "243", "011", "111", "041", "242", "010", "130", "221", "201", "132", "231", "224", "244", "221", "100", "223", "132", "044", "131" ]
]

pattern_names = ["east-1", "west-1", "east-2", "west-2", "east-3", "west-3", "east-4", "west-4", "east-5"]


class Point:
    def __init__(self, x: Number, y: Number, z: Number, color: Optional[Color]=None):
        """Represents a point in 3D space.

        Args:
            x (Number): X coordinate
            y (Number): Y coordinate
            z (Number): Z coordinate
            color (Optional[Color]): Color of the point. Defaults to None.
        """
        self.location = np.array([x, y, z])
        self.color = color
    
    def rotate(self, rotation: np.ndarray) -> "Point":
        """Rotates the point around each axis by the given angle. Returns a new point.
        
        Args:
            rotation (np.ndarray): Rotation matrix
        
        Returns:
            Point: Rotated point
        """
        rotated = rotation @ self.location
        return Point(rotated[0], rotated[1], rotated[2], self.color)
    
    def project(self, scale: Number, origin: List[int]) -> np.ndarray:
        """Projects the point onto the 2D plane. Returns X and Y coordinates.
        
        Args:
            scale (Number): Scale of the projection
            origin (List[int]): Origin of the projection
        
        Returns:
            np.ndarray: The projected point"""
        return np.array([self.location[0] * scale + origin[0], self.location[1] * scale + origin[1]])
    
    def __repr__(self):
        return f"Point({self.location[0]}, {self.location[1]}, {self.location[2]}, {self.color})"
    

class Line:
    def __init__(self, p1: Point, p2: Point):
        """Represents a line between two points.

        Args:
            p1 (Point): The first point
            p2 (Point): The second point
        """
        self.p1 = p1
        self.p2 = p2
    
    def rotate(self, rotation: np.ndarray) -> "Line":
        """Rotates the line around each axis by the given angle. Returns a new line.
        
        Args:
            rotation (np.ndarray): Rotation matrix
        
        Returns:
            Line: Rotated line
        """
        return Line(self.p1.rotate(rotation), self.p2.rotate(rotation))
    
    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"


points = []
lines = []
eye_points = []
eye_lines = []


def add_plane(x: Number, y: Number, z: Number, size: int):
    """Adds a plane at the given coordinates. Uses the Point class.

    Args:
        x (Number): x origin
        y (Number): y origin
        z (Number): z origin
        size (int): size of the plane
    """
    # add the corners
    points.append(Point(x + size//2, y, z, (255, 0, 0)))
    points.append(Point(x + size, y + size//2, z, (255, 0, 0)))
    points.append(Point(x + size//2, y + size, z, (255, 0, 0)))
    points.append(Point(x, y + size//2, z, (255, 0, 0)))

    # add 4 lines, connecting the points
    lines.append(Line(points[-4], points[-3]))
    lines.append(Line(points[-3], points[-2]))
    lines.append(Line(points[-2], points[-1]))
    lines.append(Line(points[-1], points[-4]))


eye_pattern = {
    0: [1, 1], # middle
    1: [1, 0], # top
    2: [2, 1], # right
    3: [1, 2], # bottom
    4: [0, 1], # left
}

# order to display each eye in a trigram
eye_orders = [
  [0, 1, 2],
  [0, 2, 1],
  [1, 0, 2],
  [1, 2, 0],
  [2, 0, 1],
  [2, 1, 0]
]
eye_order_idx = 0


def add_eye(x: Number, y: Number, z: Number, eye_str: str, size: int, height: int):
    """Adds an eye at the given coordinates. Uses the Point class.

    Args:
        x (Number): x origin
        y (Number): y origin
        z (Number): z origin
        eye_str (str): eye to add
        size (int): size of the plane
        height (int): height of the eye
    """
    eye = [list(map(int, i)) for i in eye_str]
    for i in range(len(eye)):
        j = eye_orders[eye_order_idx][i]
        # lookup the pattern
        pattern = eye_pattern[eye[j][0]]
        # add the point
        eye_points.append(Point(x + pattern[0], y + pattern[1], z + (2-i)*height, (0, 0, 255)))
    # add 2 lines, connecting the points
    eye_lines.append(Line(eye_points[-3], eye_points[-2]))
    eye_lines.append(Line(eye_points[-2], eye_points[-1]))


def draw_points_and_lines(a_x: Number, a_y: Number, a_z: Number):
    """Draws all points and lines. Uses the Point and Line classes.

    Args:
        a_x (Number): X rotation (radians)
        a_y (Number): Y rotation (radians)
        a_z (Number): Z rotation (radians)
    """
    # rotation matrix
    rotation = np.array([
        [1, 0, 0],
        [0, cos(a_x), -sin(a_x)],
        [0, sin(a_x), cos(a_x)]
    ]) @ np.array([
        [cos(a_y), 0, sin(a_y)],
        [0, 1, 0],
        [-sin(a_y), 0, cos(a_y)]
    ]) @ np.array([
        [cos(a_z), -sin(a_z), 0],
        [sin(a_z), cos(a_z), 0],
        [0, 0, 1]
    ])

    if SHOW_POINTS:
        for point in points:
            if point.color is not None:
                p2 = point.rotate(rotation)
                x, y = p2.project(scale, origin)
                pygame.draw.circle(window, point.color, (x, y), 2)
    
    if SHOW_PLANES:
        for line in lines:
            p1 = line.p1.rotate(rotation)
            p2 = line.p2.rotate(rotation)
            x1, y1 = p1.project(scale, origin)
            x2, y2 = p2.project(scale, origin)
            pygame.draw.line(window, (128, 128, 128), (x1, y1), (x2, y2), 2)
    
    if SHOW_EYE_POINTS:
        for point in eye_points:
            if point.color is not None:
                p2 = point.rotate(rotation)
                x, y = p2.project(scale, origin)
                pygame.draw.circle(window, point.color, (x, y), 2)
    
    if SHOW_EYE_LINES:
        for line in eye_lines:
            p1 = line.p1.rotate(rotation)
            p2 = line.p2.rotate(rotation)
            x1, y1 = p1.project(scale, origin)
            x2, y2 = p2.project(scale, origin)
            pygame.draw.line(window, (255, 255, 255), (x1, y1), (x2, y2), 2)


def add_rotation_text(a_x: Number, a_y: Number, a_z: Number):
    """Adds text to the screen describing the current state of the viewer.

    Args:
        a_x (Number): x rotation
        a_y (Number): y rotation
        a_z (Number): z rotation
    """
    # round values
    a_x = round(a_x, 2)
    a_y = round(a_y, 2)
    a_z = round(a_z, 2)
    text = arial30.render("Rotation: " + str(a_x) + ", " + str(a_y) + ", " + str(a_z), True, (255, 255, 255))
    window.blit(text, (10, 10))
    # add origin text line
    line = (
        "Origin: " + str(origin[0]) + ", " + str(origin[1]) + " | "
        + "Scale: " + str(scale) + " | "
        + "Spacing: " + str(round(eye_spacing, 2)) + " | "
        + "Order: " + str(eye_orders[eye_order_idx]) + " | "
    )
    text = arial30.render(line, True, (255, 255, 255))
    window.blit(text, (10, 40))
    # add pattern text line
    pattern_name = pattern_names[current_pattern]
    text = arial30.render("Pattern: " + pattern_name, True, (255, 255, 255))
    window.blit(text, (10, 70))


def add_guide_text():
    """Adds text to the screen describing the controls.
    """

    t = [
        "Up/Down: Rotate around x axis",
        "Left/Right: Rotate around y axis",
        "Q/E: Rotate around z axis",
        "X/Z: Scale up/down",
        "WASD: Move origin",
        "L: Toggle planes",
        "T: Toggle eye points",
        "R: Toggle eye lines",
    ]
    t2 = [
        "Shift+Rotation: Move by 45 degrees",
        "H: Toggle these instructions", 
        "0: Reset rotation",
        "1/2: Change eye pattern",
        "3/4: Change eye spacing",
        "5/6: Change eye display order",
        "Esc: Quit"
    ]
    text = arial20.render("Controls:", True, (255, 255, 255))
    window.blit(text, (10, window.get_height() - 10 - (len(t) * 28)))

    for i, line in enumerate(t):
        text = arial15.render(line, True, (255, 255, 255))
        window.blit(text, (10, window.get_height() - 10 - (len(t) * 25) + (i * 25)))

    # move a column along
    for i, line in enumerate(t2):
        text = arial15.render(line, True, (255, 255, 255))
        window.blit(text, (10 + 200, window.get_height() - 10 - (len(t2) * 25) + (i * 25)))


def handle_events():
    """Yeah, this one is a burning dumpster fire. Sorry.
    """
    global SHOW_POINTS, SHOW_PLANES, SHOW_EYE_POINTS, SHOW_EYE_LINES, SHOW_GUIDE_TEXT, RUNNING
    global a_x, a_y, a_z, scale, origin, current_pattern, holding_shift, eye_spacing, eye_order_idx
    global a_x_moving, a_y_moving, a_z_moving, scale_moving, origin_x_moving, origin_y_moving
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        # rotate while key is held down
        if event.type == pygame.KEYDOWN:
            # rotations
            if event.key == pygame.K_LEFT:
                a_y_moving = '+'
            elif event.key == pygame.K_RIGHT:
                a_y_moving = '-'
            elif event.key == pygame.K_UP:
                a_x_moving = '+'
            elif event.key == pygame.K_DOWN:
                a_x_moving = '-'
            elif event.key == pygame.K_q:
                a_z_moving = '+'
            elif event.key == pygame.K_e:
                a_z_moving = '-'

            # rotation modifier
            elif event.key == pygame.K_LSHIFT:
                holding_shift = True

            # zoom
            elif event.key == pygame.K_z:
                scale_moving = '-'
            elif event.key == pygame.K_x:
                scale_moving = '+'

            # strafe
            elif event.key == pygame.K_a:
                origin_x_moving = '-'
            elif event.key == pygame.K_d:
                origin_x_moving = '+'
            elif event.key == pygame.K_w:
                origin_y_moving = '-'
            elif event.key == pygame.K_s:
                origin_y_moving = '+'

            # hide/show layers
            elif event.key == pygame.K_p:
                SHOW_POINTS = not SHOW_POINTS
            elif event.key == pygame.K_l:
                SHOW_PLANES = not SHOW_PLANES
            elif event.key == pygame.K_t:
                SHOW_EYE_POINTS = not SHOW_EYE_POINTS
            elif event.key == pygame.K_r:
                SHOW_EYE_LINES = not SHOW_EYE_LINES
            elif event.key == pygame.K_h:
                SHOW_GUIDE_TEXT = not SHOW_GUIDE_TEXT

            # reset view
            elif event.key == pygame.K_0:
                a_x = 0
                a_y = 0
                a_z = 0
                scale = 20
                origin[0], origin[1] = 400, 400
            
            # change pattern
            elif event.key == pygame.K_1:
                if current_pattern > 0:
                    current_pattern -= 1
                    display_eye_pattern(eyes[current_pattern])
            elif event.key == pygame.K_2:
                if current_pattern < len(eyes) - 1:
                    current_pattern += 1
                    display_eye_pattern(eyes[current_pattern])
            
            # modify eye spacing
            elif event.key == pygame.K_3:
                eye_spacing -= 0.1
                display_eye_pattern(eyes[current_pattern])
            elif event.key == pygame.K_4:
                eye_spacing += 0.1
                display_eye_pattern(eyes[current_pattern])
            
            # modify eye order
            elif event.key == pygame.K_5:
                if eye_order_idx > 0:
                    eye_order_idx -= 1
                    display_eye_pattern(eyes[current_pattern])
            elif event.key == pygame.K_6:
                if eye_order_idx < len(eye_orders) - 1:
                    eye_order_idx += 1
                    display_eye_pattern(eyes[current_pattern])
                
            # quit
            elif event.key == pygame.K_ESCAPE:
                RUNNING = False

        if event.type == pygame.KEYUP:
            # stop rotating
            if event.key == pygame.K_LEFT:
                a_y_moving = False
            elif event.key == pygame.K_RIGHT:
                a_y_moving = False
            elif event.key == pygame.K_UP:
                a_x_moving = False
            elif event.key == pygame.K_DOWN:
                a_x_moving = False
            elif event.key == pygame.K_q:
                a_z_moving = False
            elif event.key == pygame.K_e:
                a_z_moving = False
            
            # stop rotation modifier
            elif event.key == pygame.K_LSHIFT:
                holding_shift = False
            
            # stop zooming
            elif event.key == pygame.K_z:
                scale_moving = False
            elif event.key == pygame.K_x:
                scale_moving = False

            # stop strafing
            elif event.key == pygame.K_a:
                origin_x_moving = False
            elif event.key == pygame.K_d:
                origin_x_moving = False
            elif event.key == pygame.K_w:
                origin_y_moving = False
            elif event.key == pygame.K_s:
                origin_y_moving = False

    # adjust rotation
    if holding_shift:
        adjustment = pi/4
    else:
        adjustment = 0.02
    if a_x_moving == '+':
        a_x += adjustment
    elif a_x_moving == '-':
        a_x -= adjustment
    if a_y_moving == '+':
        a_y += adjustment
    elif a_y_moving == '-':
        a_y -= adjustment
    if a_z_moving == '+':
        a_z += adjustment
    elif a_z_moving == '-':
        a_z -= adjustment
    if holding_shift:
        # we don't want continuous movement if we're moving large amounts...
        a_x_moving = a_y_moving = a_z_moving = False

    # adjust scale
    scale_offset = 1
    if scale_moving == '+':
        scale += scale_offset
    elif scale_moving == '-' and scale > 1:
        scale -= scale_offset

    # adjust origin
    origin_offset = 10
    if origin_x_moving == '+':
        origin[0] += origin_offset
    elif origin_x_moving == '-':
        origin[0] -= origin_offset
    if origin_y_moving == '+':
        origin[1] += origin_offset
    elif origin_y_moving == '-':
        origin[1] -= origin_offset


def display_eye_pattern(eye_pattern):
    # first, reset
    global points, lines, eye_points, eye_lines
    points = []
    lines = []
    eye_points = []
    eye_lines = []

    height_between_planes = 3
    # add 26x4 planes
    for row in range(4):
        for c in range(26):
            add_plane(c*eye_spacing, 0 + row*height_between_planes, 0, 2)
            add_plane(c*eye_spacing, 0 + row*height_between_planes, 1, 2)
            add_plane(c*eye_spacing, 0 + row*height_between_planes, 2, 2)

    current_char = 0
    row = 0
    for eye in eye_pattern:
        if current_char > 25:
            current_char = 0
            row += 1

        add_eye(current_char*eye_spacing, 0 + row*height_between_planes, 0, eye, 2, 1)
        current_char += 1


# some display options
SHOW_POINTS = False
SHOW_PLANES = True
SHOW_EYE_POINTS = False
SHOW_EYE_LINES = True
SHOW_GUIDE_TEXT = True
a_x = 0
a_y = 0
a_z = 0
scale = 20
holding_shift = False
a_x_moving = False
a_y_moving = False
a_z_moving = False
scale_moving = False
origin_x_moving = False
origin_y_moving = False
current_pattern = 0
eye_spacing = 2.5
RUNNING = True
adjustment = 0.02
origin = [400, 400]

arial15 = pygame.font.SysFont("Arial", 15)
arial20 = pygame.font.SysFont("Arial", 20)
arial30 = pygame.font.SysFont("Arial", 30)


def main():
    hs_c = ["310", "231"]
    eye_pattern = eyes[0]

    display_eye_pattern(eye_pattern)

    while RUNNING:
        clock.tick(60)

        handle_events()

        window.fill((0, 0, 0))
        draw_points_and_lines(a_x, a_y, a_z)
        add_rotation_text(a_x, a_y, a_z)
        if SHOW_GUIDE_TEXT:
            add_guide_text()
        pygame.display.update()


if __name__ == "__main__":
    main()