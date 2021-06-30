# crappy_compression
The terrible image compression system that barely works.

## Dependencies
 * PIL
 * Numpy

## How it works
This compression works by taking the pixel data for the image in each row and fitting it into a polynomial.
If we think of an image as a 3D matrix with [rows, columns, color_channels] this will reduce the image into [rows, degrees, color_channels]. You could go even crazier with a function to describe a surface and fit the x,y coordinates for each color channel onto it, but I don't dare to challenge nature like that.

## How to run
The user is able to feed in the desired degree using the `-d` flag and the image path with `-i`.

```bash
./src/main.py
./src/main.py -d 8 # specify degree
./src/main.py -i ../data/my_favorite_image.jpg # specify image path
```

## Output examples
Input:  

<img src="data/dog.bmp">  

Degree 16 Polynomial (max numpy can handle):  

<img src="output/dog_16.png">

Degree 8 Polynomial:  

<img src="output/dog_8.png">

Degree 4 Polynomial:  

<img src="output/dog_4.png">

Degree 1 Polynomial:  

<img src="output/dog_1.png">

Input:  

<img src="data/sun.jpg">

Degree 16 Polynomial (max numpy can handle):  

<img src="output/sun_16.png">

Degree 8 Polynomial:  

<img src="output/sun_8.png">

Degree 4 Polynomial:  

<img src="output/sun_4.png">

Degree 1 Polynomial:  

<img src="output/sun_1.png">
