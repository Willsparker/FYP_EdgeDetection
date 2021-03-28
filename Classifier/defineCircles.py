import cv2, numpy as np, os, math

CurPath = os.path.dirname(__file__)
# Path to output txt file:
output_path = CurPath + '/PrintedImages/IrisPositions.txt'
image_dir = CurPath + '/PrintedImages/'


# Mouse callback function
global click_list
global img_list
positions, click_list, img_list = [], [], []

def callback(event, x, y, flags, param):
    if event == 1: 
        print(img_name)
        img_list.append(img_name)
        click_list.append((x,y))

# Get all printed images, if they're .jpg
def getPrintedImageNames():
    return [os.path.splitext(f)[0] for f in os.listdir(image_dir) if os.path.splitext(f)[1] == ".jpg"]

def calculateDistanceBetweenPoints(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Create OpenCV Window, and make fullscreen
cv2.namedWindow('img', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback('img', callback)

# For all images
for img_name in getPrintedImageNames():
    img = cv2.imread(image_dir+img_name+".jpg")

    #   Mainloop - show the image and collect the data
    while True:
        cv2.imshow('img', img)    
        
        # Wait, and allow the user to quit with the 'esc' key
        k = cv2.waitKey(1)
        # If user presses 'esc' break 
        if k == 27: break        
cv2.destroyAllWindows()

for index in range(0,len(click_list),2):
    x1, y1 = click_list[index][0], click_list[index][1]
    x2, y2 = click_list[index+1][0], click_list[index+1][1]
    distance = calculateDistanceBetweenPoints(x1,y1,x2,y2)
    img_name = img_list[index]
    text = img_name + " " + str(x1) + "," + str(y1) + " " + str(distance) + "\n"
    WriteTxtFile = open(output_path, "a")
    WriteTxtFile.write(text)
    WriteTxtFile.close()
