import cv2
import serial


def get_available_cameras(max_cameras: int = 4) -> list:
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras


available_cameras = get_available_cameras()

if not available_cameras:
    print("No cameras found.")

print("Available cameras:", available_cameras)
camera_index = int(input("Enter the camera index you want to use: "))

if camera_index not in available_cameras:
    print("Invalid camera index.")

cap1 = cv2.VideoCapture(camera_index)

# Check if the cameras are opened successfully
if not cap1.isOpened():
    print("Error opening cameras")
else:
    while True:
        # Capture frames from the cameras
        ret1, frame1 = cap1.read()

        # Check if the frames are captured successfully
        if not ret1:
            print("Error capturing frames")
            break

        # Convert the frames to the HSV color space
        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds of the deep red color in HSV color space
        lower_red = (170, 100, 50)
        upper_red = (180, 255, 255)

        # Create a mask that isolates the deep red color in each frame
        mask1 = cv2.inRange(hsv1, lower_red, upper_red)

        # Find the contours of the deep red color in each frame
        contours1, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the center point of the contours and calculate the distance from the center of the screen
        for i, cnt in enumerate(contours1):
            area = cv2.contourArea(cnt)
            if area >= 500:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.drawContours(frame1, contours1, i, (0, 255, 0), 3)
                    cv2.circle(frame1, (cx, cy), 3, (0, 0, 255), -1)
                    height, width, _ = frame1.shape
                    dx = cx - width / 2
                    dy = cy - height / 2
                    if dx > 0:
                        print("Camera 1 - Deep Red: Move right by {} pixels".format(abs(dx)))
                    elif dx < 0:
                        print("Camera 1 - Deep Red: Move left by {} pixels".format(abs(dx)))
                    if dy > 0:
                        print("Camera 1 - Deep Red: Move down by {} pixels".format(abs(dy)))
                    elif dy < 0:
                        print("Camera 1 - Deep Red: Move up by {} pixels".format(abs(dy)))

        # Display the frames with the deep red color, contours, and center points
        cv2.imshow("Camera 1 - Deep Red", frame1)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the cameras and destroy the windows
    cap1.release()
    cv2.destroyAllWindows()
