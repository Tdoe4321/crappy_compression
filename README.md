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
./src/main.py -d 5 -y # specify degree of 5 and perform in the y direction
./src/main.py -i ../data/my_favorite_image.jpg # specify image path
./src/main.py -2d 2 # Specify that you want to perform a 2d polyfit of degree 2
./src/main.py -a 45 # Specify that you want to perform the fitting at an angle of 45 degrees
```

## Output examples
Input:  

<img src="data/dog.bmp">  

Degree 16 Polynomial (max numpy can handle):  

<img src="output/dog_16.png">

Degree 4 Polynomial:  

<img src="output/dog_4.png">

Degree 1 Polynomial:  

<img src="output/dog_1.png">

Input:  

<img src="data/sun.jpg">

Degree 16 Polynomial (max numpy can handle):  

<img src="output/sun_16.png">

Degree 4 Polynomial:  

<img src="output/sun_4.png">

Degree 1 Polynomial:  

<img src="output/sun_1.png">

2d Polynomial - degree 2:  

<img src="output/sun_2_2d.png">

Arbirtary angle 45deg - degree 16:  

<img src="output/dog_16_45deg.png">