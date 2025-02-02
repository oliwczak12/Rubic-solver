from PIL import Image, ImageEnhance
import globals
import numpy as np
import cv2
import time
import json

def get_dominant_color(pil_img, palette_size=8):
    img = pil_img.copy()
    img.thumbnail((100, 100))

    paletted = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)

    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]

    return (dominant_color[2], dominant_color[1], dominant_color[0])




def closest(color):
    colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 140, 0], [255, 255, 255]])
    color = np.array(color)
    distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return tuple(smallest_distance.tolist()[0])


def apply_filters(pil_image, brightness=0, contrast=0,sat=1.0):
    pil_image = saturation(pil_image,sat)
    buf = np.array(pil_image)

    #TODO sprawdzić
    if buf.ndim == 2:  
        pass
    elif buf.ndim == 3 and buf.shape[2] == 3:  
        pass
    else:
        raise ValueError("Nieobsługiwany format obrazu")


    alpha_c = contrast / 127.0 + 1.0  
    gamma_c = brightness  

    buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return Image.fromarray(buf)


def cropGrid(pil_img, grid):
    w, h = 3, 3
    cells_crops = [[0 for x in range(w)] for y in range(h)]
    for i in range(3):
        for j in range(3):
            cells_crops[j][i] = closest(
                list(
                    get_dominant_color(
                        pil_img.crop(
                            (
                                grid.grid_x + (grid.cell_size * i),
                                grid.grid_y + (grid.cell_size * j),
                                grid.grid_x + (grid.cell_size * i) + grid.cell_size,
                                grid.grid_y + (grid.cell_size * j) + grid.cell_size,
                            )
                        )
                    )
                )
            )

    return cells_crops

def saturation(pil_img, saturation):
    img = ImageEnhance.Color(pil_img)
    return img.enhance(saturation)


def colorArrayToImg(array):
    block_size = globals.cube.cube_mesh_cell_size
    img = Image.new("RGB", (3 * block_size, 3 * block_size))
    pixels = img.load()
    for i in range(3):
        for j in range(3):
            for x in range(block_size):
                for y in range(block_size):
                    pixels[i * block_size + x, j * block_size + y] = array[j][i]
    return img


def rgbDistance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2

def findClosestSettings(color, grid):
    mid_cell_img = Image.fromarray(globals.screen.lastFrame).crop(
        (grid.grid_x + (grid.cell_size * 1), grid.grid_y + (grid.cell_size * 1), grid.grid_x + (grid.cell_size * 1) + grid.cell_size, grid.grid_y + (grid.cell_size * 1) + grid.cell_size)
    )
    brightness = 0
    contrast = 0
    sat = 0
    
    points = []
    
    best = (brightness, contrast,sat)
    best_distance = 1000000
    start = time.time()
    check_sum = 0
    
    for i in range(-20, 100):
        for j in range(-20, 150):
            for k in range(10,30):
                k/=10
                buffer = apply_filters(mid_cell_img, i, j, k)
                k*=10
                    
                dom_color =  get_dominant_color(buffer)
                
                distance = rgbDistance(color, dom_color)
                print(distance)
                if  distance < best_distance:
                    print("pyk")
                    best = (i, j, k/10)
                    best_distance = distance
                    points.append((i,j,k/10,dom_color))
                    if best_distance<4500:
                        break
                if best_distance<4500 or distance>10000:
                        break
        if best_distance<4500:
            break
    print(best_distance)
    end = time.time()
    print(end - start)              
    print(best)
    print(dom_color)
    print(f"checksum= {check_sum}")
    globals.s1.set(best[0])
    globals.s2.set(best[1])
    globals.s3.set(best[2])
    
    with open('points.json', 'w') as file:
        json.dump(points, file)
