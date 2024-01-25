import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Load an image
def load_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.flip(image, 0)  # Flip the image
    return image

# Create texture from image
def create_texture(image):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.shape[1], image.shape[0], 0, GL_BGR, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    return texture_id

# Draw hemisphere
def draw_hemisphere(radius, texture_id):
    slices = 50  # Number of slices (longitude)
    stacks = 25  # Number of stacks (latitude)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + float(i) / stacks)
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * np.pi * float(j - 1) / slices
            x = np.cos(lng)
            y = np.sin(lng)
            glTexCoord2f(float(j) / slices, float(i) / stacks)
            glVertex3f(radius * x * zr0, radius * y * zr0, radius * z0)
            glTexCoord2f(float(j) / slices, float(i + 1) / stacks)
            glVertex3f(radius * x * zr1, radius * y * zr1, radius * z1)
        glEnd()

# Initialize OpenGL
def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
    glEnable(GL_DEPTH_TEST)            # Enable depth testing for z-culling
    glEnable(GL_TEXTURE_2D)            # Enable 2D textures

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                   # Reset projection matrix
    gluPerspective(45, (800/600), 0.1, 100.0)  # Set up a perspective projection matrix

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()                   # Reset modelview matrix

# Display callback for GLUT
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0)  # Position the camera

    draw_hemisphere(2, texture_id)  # Draw hemisphere with radius 2

    glutSwapBuffers()

# Main function
if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'  # Replace with your image path
    image = load_image(image_path)
    texture_id = create_texture(image)

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)  # Window size
    glutCreateWindow('Hemisphere Image Mapping')  # Window title

    initialize()  # Initialize OpenGL environment

    glutDisplayFunc(display)  # Register display callback
    glutMainLoop()  # Start the main loop
