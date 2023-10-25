import cv2, time, os

def roll(file_path):
    vidcap = cv2.VideoCapture(file_path)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    spf = 1/fps

    thumbprint = []

    ascii = [" ",".",":","-","=","+","*","#","%","@"]

    max_brightness = 0

    while vidcap.isOpened():

        last_time = time.time()

        for frame in range(total_frames):
            success, image = vidcap.read()
            if not success:
                break

            # greyscale
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # resize to fit the current terminal session
            term_size = os.get_terminal_size()
            max_columns, max_rows = term_size.columns, term_size.lines
            img_columns, img_rows = len(image[0]), len(image)
            fx, fy = max_columns / img_columns, max_rows / img_rows
            image = cv2.resize(image, (0,0), fx = fx, fy = fy)

            string = ""
            for row in range(len(image)):
                for column in range(len(image[0])):
                    brightness = (image[row][column] / 255)
                    index = round(brightness * len(ascii))
                    if index >= len(ascii):
                        # then we'd have an out of bounds error
                        index = len(ascii)-1
                    char = ascii[index]
                    string += char
                string+="\n"

            # block until appropriate for the frame to display
            blocking = True
            while blocking:
                now = time.time()
                if now >= last_time + spf:
                    last_time = now
                    blocking = False

                # print('\033[H\033[J', end='')  # Move cursor to top-left and clear screen
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
                print(string)
    #   break
