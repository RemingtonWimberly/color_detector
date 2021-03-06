import cv2
import numpy as np
import pandas as pd
import argparse


# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser(description='''Color Detector 1.3''',
    epilog="""Input a path to an image to continue.""")
ap.add_argument('-i', '--image', required=True, help="Enter the Image Path to run")
args = vars(ap.parse_args())
img_path = args['image']

print('Press ESC or close the window to exit the program')

# Reading the image with opencv
image = cv2.imread(img_path)

clicked = False
red = green = blue = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
colors_url = 'https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv'
csv = pd.read_csv(colors_url, names=index, header=None)

def get_color_name(R, G, B):
    """
    calculates the minimum distance from all colors to get the best matching color

    :param R: red value of selection
    :param G: green value of selection
    :param B: blue value of selection
    :return: string with color name and hex value
    """
    minimum_distance = 10000
    # set color name to not found in case it is not found
    color_name_str = 'Color Not Found'
    hex = 'Error'
    for i in range(len(csv)):
        distance = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if distance <= minimum_distance:
            minimum_distance = distance
            color_name_str = csv.loc[i, "color_name"]
            # trims down the color name
            if len(color_name_str) > 11 and ' ' in color_name_str:
                first, *middle, last = color_name_str.split()
                if last is not None:
                    color_name_str = first + ' ' + last
            hex = csv.loc[i, 'hex']
    return color_name_str + ' ' + hex


# function to get x,y coordinates of mouse double click
def get_rgb_from_coordinates(event, x, y, flags, paramaters):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global red, green , blue, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        blue, green, red = image[y, x]
        red = int(red)
        green = int(green)
        blue = int(blue)


cv2.namedWindow(img_path)
cv2.setMouseCallback(img_path, get_rgb_from_coordinates)

while True:

    cv2.imshow(img_path, image)
    if clicked:

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(image, (20, 20), (750, 60), (blue, green, red), -1)

        # Creating text string to display( Color name and RGB values )
        color_name = get_color_name(red, green, blue) + ' R=' + str(red) + ' G=' + str(green) + ' B=' + str(blue)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(image, color_name, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # display light colors with black text
        # fixed to run with lumens
        if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
            cv2.putText(image, color_name, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # break the loop when user hits 'esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break
    # break the loop when the user closes the window
    if cv2.getWindowProperty(img_path, cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
