
import cv2
import centroid_tracker as trck




cap = cv2.VideoCapture("movie.mpg")

object_detector = cv2.bgsegm.createBackgroundSubtractorMOG()
ct = trck.CentroidTracker()


frame_id = 0
while True:
    ret, frame = cap.read()
    frame_id = frame_id + 1

    if frame is None:
        break

    else:
        height, width, _ = frame.shape

        # Extract Region of interest - just the area to look in, for speed
        roi = frame[33: 944,55: 784]
        #roi = frame
        # 1. Object Detection
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        rects = []
        #contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # contours is a list of detected objects
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 100:
                cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                x1, y1, x2, y2 = x, y, x + w, y + h
                rects.append([x1,y1, x2, y2])
                #print(rects)

        objects = ct.update(rects)
       # print(objects.items())
        for (objectID, centroid) in objects.items():
            # draw both the ID of the object and the centroid of the
                # object on the output frame
            text = "ID {}".format(objectID)
            ct.history[objectID][frame_id] = [x,y, w, h, centroid[0], centroid[1]]
            cv2.putText(frame, text, (centroid[0], centroid[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            # show the output frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break


ct.report()