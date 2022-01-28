#!/usr/bin/env python3

import argparse

from PIL import Image
import numpy as np


if __name__ == "__main__":
    # Parse user input
    parser = argparse.ArgumentParser(description="run the submarine")
    parser.add_argument('-i', '--image', default='../data/dog.bmp', help="Relative path to input image.")
    parser.add_argument('-d', '--degree', help='Degree of polynomial to fit image to', type=int, default=16)
    parser.add_argument('-y', '--yaxis', action="store_true", help='Perform polyfit over the y axis instead of x')
    args = parser.parse_args()

    image = Image.open(args.image)
    data = np.asarray(image)
    output = np.zeros(data.shape)

    print("Image shape:")
    print(data.shape)

    # Degree for polynomial
    deg = args.degree
    polymat = None

    if args.yaxis: # Y axis
        poly_mat = np.zeros((deg + 1, data.shape[1], data.shape[2]))

        y = np.arange(data.shape[0])
        for c in range(data.shape[2]): # for all the color channels
            for col in range(data.shape[1]): # for all the cols
                x = data[:,col,c]
                poly_mat[:,col,c] = np.polyfit(y, x, deg)
                output[:,col,c] = np.polyval(poly_mat[:,col,c], y)
    else: # X axis
        poly_mat = np.zeros((data.shape[0], deg + 1, data.shape[2]))
        
        x = np.arange(data.shape[1])
        for c in range(data.shape[2]): # for all the color channels
            for row in range(data.shape[0]): # for all the rows
                y = data[row,:,c]
                poly_mat[row,:,c] = np.polyfit(x, y, deg)
                output[row,:,c] = np.polyval(poly_mat[row,:,c], x)

    # This is what you would output if you wanted to store just the compressed version
    # polymat
        
    # clip output to correct values and cast to uint
    output = np.clip(output, 0, 255).astype('uint8')

    # Save image
    Image.fromarray(output).save('../output/' + args.image.split("/")[-1].split(".")[0] + "_" + str(deg) + '.png')

