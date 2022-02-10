#!/usr/bin/env python3

import argparse

from PIL import Image
import numpy as np
from scipy import ndimage

def polyfit2d(x, y, z, kx=3, ky=3, order=None):
    '''
    Two dimensional polynomial fitting by least squares.
    Fits the functional form f(x,y) = z.

    Notes
    -----
    Resultant fit can be plotted with:
    np.polynomial.polynomial.polygrid2d(x, y, soln.reshape((kx+1, ky+1)))

    Parameters
    ----------
    x, y: array-like, 1d
        x and y coordinates.
    z: np.ndarray, 2d
        Surface to fit.
    kx, ky: int, default is 3
        Polynomial order in x and y, respectively.
    order: int or None, default is None
        If None, all coefficients up to maxiumum kx, ky, ie. up to and including x^kx*y^ky, are considered.
        If int, coefficients up to a maximum of kx+ky <= order are considered.

    Returns
    -------
    Return paramters from np.linalg.lstsq.

    soln: np.ndarray
        Array of polynomial coefficients.
    residuals: np.ndarray
    rank: int
    s: np.ndarray

    '''

    # grid coords
    x, y = np.meshgrid(x, y)
    # coefficient array, up to x^kx, y^ky
    coeffs = np.ones((kx+1, ky+1))

    # solve array
    a = np.zeros((coeffs.size, x.size))

    # for each coefficient produce array x^i, y^j
    for index, (j, i) in enumerate(np.ndindex(coeffs.shape)):
        # do not include powers greater than order
        if order is not None and i + j > order:
            arr = np.zeros_like(x)
        else:
            arr = coeffs[i, j] * x**i * y**j
        a[index] = arr.ravel()

    # do leastsq fitting and return leastsq result
    return np.linalg.lstsq(a.T, np.ravel(z), rcond=None)

if __name__ == "__main__":
    # Parse user input
    parser = argparse.ArgumentParser(description="run the submarine")
    parser.add_argument('-i', '--image', default='../data/dog.bmp', help="Relative path to input image.")
    parser.add_argument('-d', '--degree', help='Degree of polynomial to fit image to', type=int, default=16)
    parser.add_argument('-y', '--yaxis', action="store_true", help='Perform polyfit over the y axis instead of x')
    parser.add_argument('-2d', '--degree2d', default=None, help="Turns on 2d polyfitting, must also provide an integer for the degree of the polynomial. This is typically very low (1-4)", type=int)
    parser.add_argument('-a', '--angle', default=None, help="Provide an angle (in degrees) to fit the polynomial along. 0-180 up from the x-axis.", type=int)
    args = parser.parse_args()

    image = Image.open(args.image)
    data = np.asarray(image)
    output = np.zeros(data.shape)

    print("Image shape:")
    print(data.shape)

    # Degree for polynomial
    deg = args.degree
    polymat = None

    # Perform the 2d fitting
    if args.degree2d is not None:
        deg = args.degree2d
        for c in range(data.shape[2]):
            x = np.arange(data.shape[1])
            y = np.arange(data.shape[0])
            
            kx = args.degree2d
            ky = args.degree2d

            soln, residuals, rank, s = polyfit2d(x, y, data[:,:,c], kx, ky)
            fitted_surf = np.polynomial.polynomial.polygrid2d(y, x, soln.reshape((kx+1,ky+1)))
            output[:,:,c] = fitted_surf

    elif args.angle is not None:
        # Expand and rotate the data we'll be working on
        pad_vals= 60 # This probably should be an argument
        tmp_data = np.pad(data, ((pad_vals, pad_vals), (pad_vals, pad_vals), (0, 0)), mode='reflect')
        tmp_data = ndimage.rotate(tmp_data, angle=args.angle, reshape=False, mode='mirror')
        output = np.zeros(tmp_data.shape)
        print(tmp_data.shape)

        # Apply compression
        poly_mat = np.zeros((tmp_data.shape[0], deg + 1, tmp_data.shape[2]))
        x = np.arange(tmp_data.shape[1])
        for c in range(tmp_data.shape[2]): # for all the color channels
            for row in range(tmp_data.shape[0]): # for all the rows
                y = tmp_data[row,:,c]
                poly_mat[row,:,c] = np.polyfit(x, y, deg)
                output[row,:,c] = np.polyval(poly_mat[row,:,c], x)

        # Unrotate and zoom image
        output = ndimage.rotate(output, angle=-args.angle, reshape=False, mode='mirror')
        output = output[pad_vals:-pad_vals, pad_vals:-pad_vals, :]

    # Perform the regular fitting of the image in x or y direction
    else:
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
    # polymat or fitted_surf
        
    # clip output to correct values and cast to uint
    output = np.clip(output, 0, 255).astype('uint8')

    # Save image
    out_str = '../output/' + args.image.split("/")[-1].split(".")[0] + "_" + str(deg)
    if args.yaxis:
        out_str = out_str + "_" + "y"
    if args.degree2d:
        out_str = out_str + "_" + "2d"
    if args.angle:
        out_str = out_str + "_" + str(args.angle) + "deg"
    Image.fromarray(output).save(out_str + '.png')

