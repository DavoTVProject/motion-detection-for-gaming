import cv2
import logging
import time
import keyboard
import os


def read_config(file_path):
    if not os.path.exists(file_path):
        logging.error(f"Configuration file '{file_path}' not found.")
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            config[name.strip()] = value.strip()
    return config


def main():
    # Read configuration from file
    config_file = 'config.txt'
    try:
        config = read_config(config_file)
    except FileNotFoundError as e:
        logging.error(e)
        return

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Notify user to set up the application in English and wait before starting
    start_delay = int(config.get('start_delay', 5))
    logging.info(f"Set your application in English. Starting in {start_delay} seconds...")
    time.sleep(start_delay)

    # Capture video from the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Error opening the camera")
        return

    # Set video resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Initialize the first frame
    ret, frame1 = cap.read()
    if not ret:
        logging.error("Failed to read the first frame")
        return

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    min_area = int(config.get('min_area', 500))
    line_height = int(config.get('line_height', 200))
    key_walk = config.get('key_walk', 'w')
    key_jump = config.get('key_jump', 'space')
    use_keyboard = config.get('use_keyboard', 'True').lower() == 'true'

    while True:
        # Read the next frame
        ret, frame2 = cap.read()
        if not ret:
            break

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        # Compute the absolute difference between the first and second frame
        frame_delta = cv2.absdiff(gray1, gray2)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the horizontal line
        cv2.line(
            frame2,
            (0, line_height),
            (frame2.shape[1], line_height),
            (0, 255, 0), 2
        )

        movement = "No movement"
        for contour in contours:
            if cv2.contourArea(contour) < min_area:
                continue

            # Find the topmost point of the contour
            topmost = tuple(contour[contour[:, :, 1].argmin()][0])
            top_x, top_y = topmost

            for point in contour:
                cv2.circle(frame2, tuple(point[0]), 1, (0, 0, 255), -1)

            if top_y > line_height:
                movement = "Walking"
                if use_keyboard:
                    keyboard.press_and_release(key_walk)
            else:
                movement = "Jumping"
                if use_keyboard:
                    keyboard.press_and_release(key_jump)

        # Display the movement text in the bottom left corner
        cv2.putText(frame2, movement, (10, frame2.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the additional text in the top left corner
        cv2.putText(frame2, "Subscribe to pycrafting_tv", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Display the processed frame
        cv2.imshow("Security Feed", frame2)

        # Update the first frame
        gray1 = gray2.copy()

        # Exit the loop if 'q' key is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
