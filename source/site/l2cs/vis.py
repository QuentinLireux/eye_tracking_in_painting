import cv2
import numpy as np
from .results import GazeResultContainer

def draw_gaze(width, a,b,c,d,image_in, pitchyaw, thickness=2, color=(255, 255, 0),sclae=2.0, is_calibration=False):
    """Draw gaze angle on given image with a given eye positions."""
    image_out = image_in
    (h, w) = image_in.shape[:2]
    length = c
    # length = width / 2
    pos = (int(a+c / 2.0), int(b+d / 2.0))
    if len(image_out.shape) == 2 or image_out.shape[2] == 1:
        image_out = cv2.cvtColor(image_out, cv2.COLOR_GRAY2BGR)
    dx = -length * np.sin(pitchyaw[0]) * np.cos(pitchyaw[1])
    dy = -length * np.sin(pitchyaw[1])
    if not is_calibration:
        cv2.arrowedLine(image_out, tuple(np.round(pos).astype(np.int32)),
                    tuple(np.round([pos[0] + dx, pos[1] + dy]).astype(int)), color,
                    thickness, cv2.LINE_AA, tipLength=0.18)
    return image_out, dx, dy

def draw_bbox(frame: np.ndarray, bbox: np.ndarray):
    
    x_min=int(bbox[0])
    if x_min < 0:
        x_min = 0
    y_min=int(bbox[1])
    if y_min < 0:
        y_min = 0
    x_max=int(bbox[2])
    y_max=int(bbox[3])

    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0,255,0), 1)

    return frame

def render(frame: np.ndarray, results: GazeResultContainer, width, height, border_points, is_calibration, tracker):
    dx, dy = None, None
    gaze_point = 0
    # Draw bounding boxes
    if not is_calibration:
        for bbox in results.bboxes:
            frame = draw_bbox(frame, bbox)

    # Draw Gaze
    for i in range(results.pitch.shape[0]):
        bbox = results.bboxes[i]
        pitch = results.pitch[i]
        yaw = results.yaw[i]

        # Extract safe min and max of x,y
        x_min=int(bbox[0])
        if x_min < 0:
            x_min = 0
        y_min=int(bbox[1])
        if y_min < 0:
            y_min = 0
        x_max=int(bbox[2])
        y_max=int(bbox[3])

        # Compute sizes
        bbox_width = x_max - x_min
        bbox_height = y_max - y_min
        
        image_out, dx, dy = draw_gaze(width, x_min,y_min,bbox_width, bbox_height,frame,(pitch,yaw),color=(0,0,255), is_calibration=is_calibration)
        if not is_calibration:
            x1 , y1 = border_points[0][0], border_points[0][1]
            x2 , y2 = border_points[1][0], border_points[1][1]
            x3 , y3 = border_points[2][0], border_points[2][1]
            x4 , y4 = border_points[3][0], border_points[3][1]
            gaze_point = [0 , 0]
            if dx <= 0 and dy <= ((y4-y1)/2):
                gaze_point[0] = (width/2) - (width/2)*(dx/(x1))
                gaze_point[1] = 0 + (height/2)*((dy-y1)/((y4-y1)/2)) 
            elif dx > 0 and dy <= ((y3-y2)/2):
                gaze_point[0] = (width/2) + (width/2)*(dx/(x2))
                gaze_point[1] = 0 + (height/2)*((dy-y2)/((y3-y2)/2))
            elif dx > 0 and dy > ((y3-y2)/2):
                gaze_point[0] = (width/2) + (width/2)*(dx/(x3))
                gaze_point[1] = (height/2) + (height/2)*((dy-(y2+((y3-y2)/2)))/((y3-y2)/2))
            elif dx <= 0 and dy > ((y4-y1)/2):
                gaze_point[0] = (width/2) - (width/2)*(dx/(x4))
                gaze_point[1] = (height/2) + (height/2)*((dy-(y1+((y4-y1)/2)))/((y4-y1)/2))
            gaze_point = int(gaze_point[0]) , int(gaze_point[1])
            if gaze_point[0] >= 0 and gaze_point[0] <= width and gaze_point[1] >= 0 and gaze_point[1] <= height:
                #cv2.circle(frame, gaze_point, 15, (0, 0, 255), -1)
                tracker.set_transform_eye_calib(gaze_point)
    return frame, dx, dy

    