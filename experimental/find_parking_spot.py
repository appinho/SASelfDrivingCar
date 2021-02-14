# import libraries
import cv2
import numpy as np
import math

# parameters
h_min = 0 #cv2.getTrackbarPos('Hue min','Parameter')
s_min = 120 #cv2.getTrackbarPos('Sat min','Parameter')
v_min = 20 #cv2.getTrackbarPos('Val min','Parameter')
h_max = 5 #cv2.getTrackbarPos('Hue max','Parameter')
s_max = 255 #cv2.getTrackbarPos('Sat max','Parameter')
v_max = 255 #cv2.getTrackbarPos('Val max','Parameter')
# filter color
lower_color = np.array([h_min,s_min,v_min])
#lower_color = np.array([30,65,160])
upper_color = np.array([h_max,s_max,v_max])
#upper_color = np.array([100,125,220])
dilate_kernel_size =  2 #cv2.getTrackbarPos('Dilate kernel size','Parameter')
erode_kernel_size =  2 # cv2.getTrackbarPos('Erode kernel size','Parameter')
dilate_shape = cv2.MORPH_RECT
dilate_kernel = cv2.getStructuringElement(dilate_shape, (2 * dilate_kernel_size + 1, 2 * dilate_kernel_size + 1),
                                   (dilate_kernel_size, dilate_kernel_size))
                                   
erosion_shape = cv2.MORPH_RECT
erode_kernel = cv2.getStructuringElement(erosion_shape, (2 * erode_kernel_size + 1, 2 * erode_kernel_size + 1),
                                   (erode_kernel_size, erode_kernel_size))
                                   
test_image = cv2.imread("../data/image/2.png")
video_filename = "../data/video/2.mp4"

def detect(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    bin_color_img = cv2.inRange(hsv, lower_color, upper_color)
    #filtered = cv2.bitwise_and(frame,frame, mask= bin_color_img)

    # dilate image
    bin_dilate_img = cv2.dilate(bin_color_img,dilate_kernel)
    
    # erode image
    bin_erode_img = cv2.erode(bin_dilate_img,erode_kernel)
    
    """
    lines = cv2.HoughLines(bin_erode_img, 1, np.pi / 180, 200, None, 0, 0)
    lines_image = frame.copy()
    print(lines)
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(lines_image, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
        
    return lines_image
    """

    # find contours
    # contours, hierarchy = cv2.findContours(bin_dilate_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    num_labels, labels, clusters, _ = cv2.connectedComponentsWithStats(bin_erode_img)
    if num_labels == 1:
        return frame
    areas = clusters[1:,4]
    max_index = np.argmax(areas) + 1
    bc = clusters[max_index]
    mask = np.array(frame, dtype=np.uint8)
    mask[labels==max_index] = [255, 255, 0]
    
    # Map component labels to hue val
    # label_hue = np.uint8(179*labels/np.max(labels))
    # blank_ch = 255*np.ones_like(label_hue)
    #labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    # labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    # labeled_img[label_hue==0] = 0
    
    output_img = frame.copy()
    added_image = cv2.addWeighted(output_img,1.0,mask,1.0, 0)
    cv2.rectangle(added_image, (bc[0], bc[1]), (bc[0]+bc[2], bc[1]+bc[3]), (255, 0, 0), 2)

    return added_image

def main():
    #frame = test_image[240:,:,:]
    #result = detect(frame)
    #cv2.imshow("Image", result)
    #cv2.waitKey(0)
    
    cap = cv2.VideoCapture(video_filename)
    while(cap.isOpened()):

        ret, frame = cap.read()
        if frame is None:
            continue
        # Cut frame to process only lower half
        frame = frame[240:,:,:]
        
        result = detect(frame)
        cv2.imshow("Image", result)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
    
main()
