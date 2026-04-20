import cv2
import threading
import database
# this variable is shared between camera and FastAPI
current_count = 0
events = []
lock = threading.Lock()

def start_camera(video_path="test_video.mp4"):
    global current_count, events

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("ERROR: Could not open video file")
        return

    # this detects moving objects in the background
    subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500,
        varThreshold=50,
        detectShadows=False
    )

    print("Camera started...")

    while True:
        ret, frame = cap.read()

        # if video ends, restart it from beginning
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # resize frame to make processing faster
        frame = cv2.resize(frame, (640, 480))

        # apply background subtraction — gives us a mask
        mask = subtractor.apply(frame)

        # clean up the mask (remove small noise)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # find contours — each big contour is a person
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        count = 0
        for contour in contours:
            area = cv2.contourArea(contour)

            # ignore small blobs — only count large moving objects
            if area < 1500:
                continue

            count += 1

            # draw a green box around each detected person
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # only save to DB if count changed
        if count != current_count:
            database.insert_event(count)
            
        # safely update the shared variable
        with lock:
            current_count = count
            events.append({
                "people_count": count,
                "timestamp": str(__import__("datetime").datetime.now())
            })
            # keep only last 50 events in memory
            if len(events) > 50:
                events.pop(0)


        # show count on the video window
        cv2.putText(
            frame,
            f"People: {count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("People Counter", frame)

        # press Q to quit
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# run this file directly to test camera alone
if __name__ == "__main__":
    start_camera()