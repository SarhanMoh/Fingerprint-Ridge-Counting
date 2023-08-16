# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
import cv2
import os
import numpy as np
import skimage
from skimage.morphology import skeletonize

# Set the directory path where the images are stored
directory = './input_images'
# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file has an image file extension
    if filename.lower().endswith('.png'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        # Load the image using OpenCV
        img = cv2.imread(file_path)
        # Check if the image was successfully loaded
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            gray_blur = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)
            gray_blur = cv2.cvtColor(gray_blur, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # invert the mask (background is white, foreground is black)
            mask = cv2.bitwise_not(mask)
            # apply some morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            # save the mask
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            masked_gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
            masked_gray = clahe.apply(masked_gray)
            # apply GaussianBlur on the image
            blur = cv2.GaussianBlur(masked_gray, (5, 5), 0)
            # convert the  image to grayscale
            masked_gray = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)
            masked_gray = cv2.cvtColor(masked_gray, cv2.COLOR_BGR2GRAY)
            thresh_val = 90
            thresh_img = np.where(masked_gray <= thresh_val, 0, 255).astype('uint8')
            thresh = 0.5
            # Apply thresholding
            binary = (thresh_img > thresh).astype(int)
            # apply skeleton to the image
            masked_gray = skeletonize(binary)

            # Define the size of the rectangular region to search for the best area
            rectangle_size = 120
            # Iterate over each possible rectangular region in the image and keep track of the best one
            best_rectangle = None
            best_pixel = 0
            for y in range(0, masked_gray.shape[0] - rectangle_size, rectangle_size):
                for x in range(0, masked_gray.shape[1] - rectangle_size, rectangle_size):
                    rectangle = masked_gray[y:y + rectangle_size, x:x + rectangle_size]
                    pixel = rectangle.sum()
                    if pixel > best_pixel:
                        best_pixel = pixel
                        best_rectangle = (x, y, rectangle_size, rectangle_size)
            #  cut the wanted rectangle
            cut_img = (img[best_rectangle[1]: best_rectangle[1] + best_rectangle[3],
                       best_rectangle[0]:best_rectangle[0] + best_rectangle[2]]).copy()
            # Draw a rectangle around the brightest area
            cv2.rectangle(img, (best_rectangle[0], best_rectangle[1]), (
                best_rectangle[0] + best_rectangle[2], best_rectangle[1] + best_rectangle[3]),
                          (0, 0, 255), 2)
            # convert the cut image to grayscale
            grayCut = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
            # apply clahe on the image (histogram equalization)
            clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(14, 14))
            grayCut = clahe.apply(grayCut)
            # apply GaussianBlur on the image
            blur = cv2.GaussianBlur(grayCut, (3, 3), 0)
            gray_blur = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)
            gray_blur = cv2.cvtColor(gray_blur, cv2.COLOR_BGR2GRAY)
            # apply to dilate on the image
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            dilated_image = cv2.dilate(gray_blur, kernel, iterations=1)
            # convert the image into binary image
            ret, binary_img = cv2.threshold(grayCut, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # count the number of the ridegs in each diagonal and take the max number
            whiteLine_Left = True
            count_left_diagonal = 0
            # Iterate over image from left to right
            for i in range(binary_img.shape[0]):
                if binary_img[i][i] == 0 and whiteLine_Left:
                    count_left_diagonal += 1
                    whiteLine_Left = False
                if binary_img[i][i] == 255:
                    whiteLine_Left = True
            # Flip the binary_img array horizontally
            flipped_img = np.flip(binary_img, axis=1)
            whiteLine_Right = True
            count_right_diagonal = 0
            # Iterate over the flipped image from right to left
            for i in range(flipped_img.shape[0]):
                if flipped_img[i][i] == 0 and whiteLine_Right:
                    count_right_diagonal += 1
                    whiteLine_Right = False
                if flipped_img[i][i] == 255:
                    whiteLine_Right = True
            my_str = 0
            # draw a diagonal line inside the rectangle the diagonal location depend on number of the ridges
            if count_right_diagonal > count_left_diagonal:
                my_str = str(count_right_diagonal)
                cv2.line(img, (best_rectangle[0] + best_rectangle[2], best_rectangle[1]), (
                    best_rectangle[0], best_rectangle[1] + best_rectangle[3]), (0, 0, 255), 2)
            if count_left_diagonal > count_right_diagonal:
                my_str = str(count_left_diagonal)
                cv2.line(img, (best_rectangle[0], best_rectangle[1]), (
                    best_rectangle[0] + best_rectangle[2], best_rectangle[1] + best_rectangle[3]),
                         (0, 0, 255), 2)
            if count_left_diagonal == count_right_diagonal:
                my_str = str(count_left_diagonal)
                cv2.line(img, (best_rectangle[0], best_rectangle[1]), (
                    best_rectangle[0] + best_rectangle[2], best_rectangle[1] + best_rectangle[3]),
                         (0, 0, 255), 2)

            # Define the text to display and its location
            text = my_str + ' Ridges'
            location = (best_rectangle[0] + 15, best_rectangle[1] + 15)  # (x, y) coordinates
            # Define the font and its properties
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.55
            color = (0, 0, 255)  # BGR format
            thickness = 2
            # Draw the text on the image
            cv2.putText(img, text, location, font, font_scale, color, thickness)
            # save the new image in the output_images folder
            output_dir = 'output_images'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            path = 'output_images/'
            imgName = str(filename)
            cv2.imwrite(os.path.join(path, imgName), img)
        else:
            print('Error: Unable to load image file: {}'.format(file_path))
