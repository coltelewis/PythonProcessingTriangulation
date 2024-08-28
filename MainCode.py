"""
Triangulating an Image to Processing Code, Colten Lewis

Work Process:
Initially, I tried to manually place each triangle, using a coordinate-picking tool to ensure accuracy in representing the image. 
However, this approach was too time-consuming. After some research, I discovered a more efficient method using Python. Work below: 
1. Load the image and generate a set of random points across it
2. Perform Delaunay triangulation on these points (https://www.degeneratestate.org/posts/2017/May/24/images-to-triangles/)
3. For each triangle, determine the median color of the pixels within it.
4. Generate Processing code that draws the triangulated image with the sampled colors.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from skimage import color
import cv2

#generate uniform random points across the image
def generate_uniform_random_points(image, n_points):
    height, width = image.shape[:2]
    points = np.vstack([np.random.randint(0, width, n_points), np.random.randint(0, height, n_points)]).T
    return points

#get  median color of each triangle
def get_triangle_colour(tri, image):
    triangle_colours = []
    for triangle in tri.simplices:
        pts = tri.points[triangle]

        # create a mask for the triangle
        mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        cv2.fillPoly(mask, [pts.astype(np.int32)], 1)

        # get the median color inside the triangle
        colors = image[mask == 1]
        median_color = np.median(colors, axis=0)
        triangle_colours.append(median_color)
    return np.array(triangle_colours)

#generate processing code
def generate_processing_code(tri, colors, width, height):
    code = f"void setup() {{\n  size({width}, {height});\n  background(#e5d5ba);\n}}\n\nvoid draw() {{\n  noStroke();\n\n" #background color and nostroke() was best suited for my original image, change to whatever
    for i, triangle in enumerate(tri.simplices):
        pts = tri.points[triangle]
        color = colors[i]
        code += f"  fill({int(color[0])}, {int(color[1])}, {int(color[2])}); triangle({int(pts[0][0])}, {int(pts[0][1])}, {int(pts[1][0])}, {int(pts[1][1])}, {int(pts[2][0])}, {int(pts[2][1])});\n"
    code += "  saveFrame(\"AdamsCreationColtenLewis.jpg\");\n"
    code += "  noLoop();\n"
    code += "}\n"
    return code

#process the image and generate processing code
def main(image_path):
    im = plt.imread(image_path)
    height, width = im.shape[:2]
    n_points = 900 #amount of points
    points = generate_uniform_random_points(im, n_points)
    tri = Delaunay(points)
    triangle_colours = get_triangle_colour(tri, im)
    processing_code = generate_processing_code(tri, triangle_colours, width, height)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "AdamsCreationColtenLewis.pde")#obv change to whatever you want
    
    with open(output_path, 'w') as f:
        f.write(processing_code)
    print(f"Processing code saved to '{output_path}'")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "originaladam.jpg")#change to the image name in the same folder that you want to reference
    main(image_path)