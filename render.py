"""Warning! Here be dragons.

This was thrown together lazily based on a vague memory of how to do
this sort of rendering. It's very slow. It's not very pretty. It's
not very well documented. It's not very well tested. It's not very
well thought out. It's not very well anything. It's just a quick
hack to get something working.
"""

import pygame
import numpy as np
from math import sin, cos

pygame.init()
window = pygame.display.set_mode((1100, 800))
clock = pygame.time.Clock()

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

points = []
lines = []
eye_points = []
eye_lines = []


def add_plane(x, y, z, size):
    """Adds a plane at the given coordinates.

    Args:
        x (int): x origin
        y (int): y origin
        z (int): z origin
        size (int): size of the plane
    """
    # add the corners
    points.append([[x + size//2], [y], [z], (255, 0, 0)])
    points.append([[x + size], [y + size//2], [z], (255, 0, 0)])
    points.append([[x + size//2], [y + size], [z], (255, 0, 0)])
    points.append([[x], [y + size//2], [z], (255, 0, 0)])
    # add 4 lines, connecting the points
    lines.append([len(points) - 4, len(points) - 3])
    lines.append([len(points) - 3, len(points) - 2])
    lines.append([len(points) - 2, len(points) - 1])
    lines.append([len(points) - 1, len(points) - 4])


eye_pattern = {
    0: [1, 1], # middle
    1: [1, 0], # top
    2: [2, 1], # right
    3: [1, 2], # bottom
    4: [0, 1], # left
}

# order to display each eye in a trigram
eye_order = [0, 1, 2]


def add_eye(x, y, z, eye, size, height):
    """Adds an eye at the given coordinates.

    Args:
        x (int): x origin
        y (int): y origin
        z (int): z origin
        eye (str): eye to add
        size (int): size of the plane
        height (int): height of the eye
    """
    eye = [list(map(int, i)) for i in eye]
    for i in range(len(eye)):
        j = eye_order[i]
        # lookup the pattern
        pattern = eye_pattern[eye[j][0]]
        # add the point
        eye_points.append([[x + pattern[0]], [y + pattern[1]], [z + (2-j)*height], (0, 0, 255)])
    # add 2 lines, connecting the points
    eye_lines.append([len(eye_points) - 3, len(eye_points) - 2])
    eye_lines.append([len(eye_points) - 2, len(eye_points) - 1])



# projects a 3d point to 2d for display
proj_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])

origin = [400, 400]


def draw_points_and_lines(a_x, a_y, a_z):
    """Draws all points and lines.

    Args:
        a_x (int): x rotation
        a_y (int): y rotation
        a_z (int): z rotation
    """
    r_x = np.array([[1, 0, 0], [0, cos(a_x), -sin(a_x)], [0, sin(a_x), cos(a_x)]])
    r_y = np.array([[cos(a_y), 0, sin(a_y)], [0, 1, 0], [-sin(a_y), 0, cos(a_y)]])
    r_z = np.array([[cos(a_z), -sin(a_z), 0], [sin(a_z), cos(a_z), 0], [0, 0, 1]])

    for point in points:
        *point, color = point
        if color is not None and SHOW_POINTS:
            rotated_x = np.matmul(r_x, point)
            rotated_y = np.matmul(r_y, rotated_x)
            rotated_z = np.matmul(r_z, rotated_y)
            point_2d = np.matmul(proj_matrix, rotated_z)
            x = point_2d[0][0] * scale + origin[0]
            y = point_2d[1][0] * scale + origin[1]
            pygame.draw.circle(window, color, (x, y), 2)

    for line in lines:
        # same rotation as above
        *p1, color = points[line[0]]
        *p2, color = points[line[1]]
        if SHOW_PLANES:
            rotated_x = np.matmul(r_x, p1)
            rotated_y = np.matmul(r_y, rotated_x)
            rotated_z = np.matmul(r_z, rotated_y)
            point_2d = np.matmul(proj_matrix, rotated_z)
            x1 = point_2d[0][0] * scale + origin[0]
            y1 = point_2d[1][0] * scale + origin[1]

            rotated_x = np.matmul(r_x, p2)
            rotated_y = np.matmul(r_y, rotated_x)
            rotated_z = np.matmul(r_z, rotated_y)
            point_2d = np.matmul(proj_matrix, rotated_z)
            x2 = point_2d[0][0] * scale + origin[0]
            y2 = point_2d[1][0] * scale + origin[1]

            pygame.draw.line(window, (128, 128, 128), (x1, y1), (x2, y2), 2)

    for point in eye_points:
        *point, color = point
        if color is not None and SHOW_EYE_POINTS:
            rotated_x = np.matmul(r_x, point)
            rotated_y = np.matmul(r_y, rotated_x)
            rotated_z = np.matmul(r_z, rotated_y)
            point_2d = np.matmul(proj_matrix, rotated_z)
            x = point_2d[0][0] * scale + origin[0]
            y = point_2d[1][0] * scale + origin[1]
            pygame.draw.circle(window, color, (x, y), 2)

    for line in eye_lines:
        # same rotation as above
        *p1, color = eye_points[line[0]]
        *p2, color = eye_points[line[1]]
        if SHOW_EYE_LINES:
            rotated_x = np.matmul(r_x, p1)
            rotated_y = np.matmul(r_y, rotated_x)
            rotated_z = np.matmul(r_z, rotated_y)
            point_2d = np.matmul(proj_matrix, rotated_z)
            x1 = point_2d[0][0] * scale + origin[0]
            y1 = point_2d[1][0] * scale + origin[1]

            rotated_x = np.matmul(r_x, p2)
            rotated_y = np.matmul(r_y, rotated_x)
            rotated_z = np.matmul(r_z, rotated_y)
            point_2d = np.matmul(proj_matrix, rotated_z)
            x2 = point_2d[0][0] * scale + origin[0]
            y2 = point_2d[1][0] * scale + origin[1]

            pygame.draw.line(window, (255, 255, 255), (x1, y1), (x2, y2), 2)


def add_rotation_text(a_x, a_y, a_z):
    """Adds text to the screen describing the current state of the viewer.

    Args:
        a_x (int): x rotation
        a_y (int): y rotation
        a_z (int): z rotation
    """
    # round values
    a_x = round(a_x, 2)
    a_y = round(a_y, 2)
    a_z = round(a_z, 2)
    font = pygame.font.SysFont("Arial", 30)
    text = font.render("Rotation: " + str(a_x) + ", " + str(a_y) + ", " + str(a_z), 1, (255, 255, 255))
    window.blit(text, (10, 10))
    # add origin text line
    text = font.render("Origin: " + str(origin[0]) + ", " + str(origin[1]), 1, (255, 255, 255))
    window.blit(text, (10, 40))


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
        "H: Toggle these instructions", 
        "0: Reset rotation",
    ]
    font = pygame.font.SysFont("Arial", 20)
    text = font.render("Controls:", 1, (255, 255, 255))
    window.blit(text, (10, window.get_height() - 10 - (len(t) * 28)))

    f2 = pygame.font.SysFont("Arial", 15)
    for i, line in enumerate(t):
        text = f2.render(line, 1, (255, 255, 255))
        window.blit(text, (10, window.get_height() - 10 - (len(t) * 25) + (i * 25)))


# some display options
SHOW_POINTS = False
SHOW_PLANES = True
SHOW_EYE_POINTS = False
SHOW_EYE_LINES = False
SHOW_GUIDE_TEXT = True
a_x = 0
a_y = 0
a_z = 0
scale = 20
a_x_moving = False
a_y_moving = False
a_z_moving = False
scale_moving = False
origin_x_moving = False
origin_y_moving = False

adjustment = 0.02

def handle_events():
    """Yeah, this one is a burning dumpster fire. Sorry.
    """
    global SHOW_POINTS, SHOW_PLANES, SHOW_EYE_POINTS, SHOW_EYE_LINES, SHOW_GUIDE_TEXT
    global a_x, a_y, a_z, scale, origin
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
            if event.key == pygame.K_RIGHT:
                a_y_moving = '-'
            if event.key == pygame.K_UP:
                a_x_moving = '+'
            if event.key == pygame.K_DOWN:
                a_x_moving = '-'
            if event.key == pygame.K_q:
                a_z_moving = '+'
            if event.key == pygame.K_e:
                a_z_moving = '-'

            # zoom
            if event.key == pygame.K_z:
                scale_moving = '-'
            if event.key == pygame.K_x:
                scale_moving = '+'

            # strafe
            if event.key == pygame.K_a:
                origin_x_moving = '-'
            if event.key == pygame.K_d:
                origin_x_moving = '+'
            if event.key == pygame.K_w:
                origin_y_moving = '-'
            if event.key == pygame.K_s:
                origin_y_moving = '+'

            # hide/show layers
            if event.key == pygame.K_p:
                SHOW_POINTS = not SHOW_POINTS
            if event.key == pygame.K_l:
                SHOW_PLANES = not SHOW_PLANES
            if event.key == pygame.K_t:
                SHOW_EYE_POINTS = not SHOW_EYE_POINTS
            if event.key == pygame.K_r:
                SHOW_EYE_LINES = not SHOW_EYE_LINES
            if event.key == pygame.K_h:
                SHOW_GUIDE_TEXT = not SHOW_GUIDE_TEXT

            # reset view
            if event.key == pygame.K_0:
                a_x = 0
                a_y = 0
                a_z = 0
                scale = 20
                origin[0], origin[1] = 400, 400

        if event.type == pygame.KEYUP:
            # stop rotating
            if event.key == pygame.K_LEFT:
                a_y_moving = False
            if event.key == pygame.K_RIGHT:
                a_y_moving = False
            if event.key == pygame.K_UP:
                a_x_moving = False
            if event.key == pygame.K_DOWN:
                a_x_moving = False
            if event.key == pygame.K_q:
                a_z_moving = False
            if event.key == pygame.K_e:
                a_z_moving = False
            
            # stop zooming
            if event.key == pygame.K_z:
                scale_moving = False
            if event.key == pygame.K_x:
                scale_moving = False

            # stop strafing
            if event.key == pygame.K_a:
                origin_x_moving = False
            if event.key == pygame.K_d:
                origin_x_moving = False
            if event.key == pygame.K_w:
                origin_y_moving = False
            if event.key == pygame.K_s:
                origin_y_moving = False

    # adjust rotation
    if a_x_moving == '+':
        a_x += adjustment
    if a_x_moving == '-':
        a_x -= adjustment
    if a_y_moving == '+':
        a_y += adjustment
    if a_y_moving == '-':
        a_y -= adjustment
    if a_z_moving == '+':
        a_z += adjustment
    if a_z_moving == '-':
        a_z -= adjustment

    # adjust scale
    scale_offset = 1
    if scale_moving == '+':
        scale += scale_offset
    if scale_moving == '-' and scale > 1:
        scale -= scale_offset

    # adjust origin
    origin_offset = 10
    if origin_x_moving == '+':
        origin[0] += origin_offset
    if origin_x_moving == '-':
        origin[0] -= origin_offset
    if origin_y_moving == '+':
        origin[1] += origin_offset
    if origin_y_moving == '-':
        origin[1] -= origin_offset


def main():
    height_between_planes = 3
    eye_spacing = 2.5
    # add 26x4 planes
    for row in range(4):
        for c in range(26):
            add_plane(c*eye_spacing, 0 + row*height_between_planes, 0, 2)
            add_plane(c*eye_spacing, 0 + row*height_between_planes, 1, 2)
            add_plane(c*eye_spacing, 0 + row*height_between_planes, 2, 2)

    hs_c = ["310", "231"]
    eye_pattern = eyes[0]
    current_char = 0
    row = 0
    for eye in eye_pattern:
        if current_char > 25:
            current_char = 0
            row += 1

        add_eye(current_char*eye_spacing, 0 + row*height_between_planes, 0, eye, 2, 1)
        current_char += 1

    while True:
        clock.tick(30)

        handle_events()

        window.fill((0, 0, 0))
        draw_points_and_lines(a_x, a_y, a_z)
        add_rotation_text(a_x, a_y, a_z)
        if SHOW_GUIDE_TEXT:
            add_guide_text()
        pygame.display.update()


if __name__ == "__main__":
    main()