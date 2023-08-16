# Fingerprint-Ridge-Counting
Name: Mohammad Sarhan
Project Name: Finding the number of ridges from a fingerprint.
Project Type: A graduation project in an image processing course.
Code for fingerprint ridge counting using image processing: identifies optimal regions, enhances images, counts ridges via diagonal analysis for accurate results.

Introduction to the project:

This code is used to count the number of ridges in an image using the identification and isolation of the most suitable rectangular region in terms of brightness and density in the image. To achieve this, I apply different image processing techniques as a deferment to clean the image and emphasize the desired parts (gray, blur, Gaussian blur, threshold, mask, Kernel, clahe, skeleton, and dilate).
Then I repeat the rectangular areas within the picture to find the one that is more appropriate. After identifying the brightest rectangle, I cut the original image into this area and apply additional image processing techniques to isolate and improve the parts and ridges, and epic of the image within this area.
Then when everything is ready, I begin to tell the number of ridges in the picture that the diagonal is cut with them, and every time it is cut I count one and I do it in both diagonals from left to right and to right of Lest and then at the end I choose the highest substrate that comes out of the two diagonals and he will be the number of ridges in the picture.


Description of the project in stages:

This code receives images in the PNG format from an input_images directory and performs several image processing operations on them (gray, blur, Gaussian blur, threshold, mask, Kernel, clahe, skeleton, and dilate) to find the most suitable rectangular area to perform a ridges count and finally save the images with a direction on the rectangle location and also the number of ridges in the library called output_images.

The steps for processing the image in code:
1- Loading the image using OpenCV.
2- Converts the image to grayscale.
3– Apply Gaussian blur to the image.
4 - Apply Otsu's thresholding to the blurry image to create a binary mask.
5- Turn the mask over so that the front is white and the background is black.
6– Perform some morphological actions to clear the mask.
7- Create a mask image by applying the mask to the original image.
8—Apply a histogram comparison (CLAHE) to the masked image.
9 – Create an embedded version of the image using the skeletonize function from the skimage package.
10 – Looking for the most suitable rectangular area in the picture.
11 - Draw a rectangle around the most appropriate area.
12 - Crop the most suitable rectangular area and perform additional image processing on it.
13 - Count the number of black pixels in the left and right diagonal of the cutting area.
14- Select the maximum number of assets counted and take it.
15- Draw a rectangle with a diagonal on the original image that shows the best place with the number of ridges.


Description of the project in general:
The code uses cv2, os, numpy, and skimming libraries.

The code reads pictures from the input_images library, processes a picture to find the most appropriate rectangular area in the picture, draws a rectangle around it, and extracts it as a new image.
It loads the image from the given directory using the OpenCV Imread function. It checks to see if the image is loaded successfully, converts the image to grayscale, and applies Gaussian Blur.

He then applies thresholding to the image to obtain a binary mask of the object and cleans the mask using morphological actions. Then, he applies the mask to the original image to get a picture with a mask. Then apply histogram equalization to a picture in grayscale and then apply Gaussian Blur to slide the picture.


Then, perform skeletonization on the image to get a skeletonized image. Then, it sets the rectangular area size to look for the most appropriate area in the picture. It then repeats any possible rectangular area and follows the most appropriate area.

It draws a rectangle around the best area and displays the original image with the area described by the rectangle. It also extracts the area as a separate image and applies image processing operations such as histogram equalization, Gaussian Blu, and thresholding to this image to identify the black pixels that are cut with the diagonals on the left and right of the image. It counts the number of black pixels in the left and right diagonal and prints the count.

And finally, he saves the pictures in a library called Output_images, highlighting each moderate rectangle with the number of ridges.
