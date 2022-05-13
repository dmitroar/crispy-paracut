import sys
import getopt
import os
import cv2


def main(argv):
    inputfile = ''
    outputfolder = ''
    try:
        opts, _ = getopt.getopt(
            argv, 'hi:o:', ['help=', 'inputfile=', 'outputfolder='])
    except getopt.GetoptError:
        print('crispy-paracut.py -i <inputfile> -o <outputfolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('crispy.py -i <inputfile> -o <outputfolder>')
            sys.exit()
        elif opt in ('-i', '--inputfile'):
            inputfile = arg
            file_exist = os.path.exists(inputfile)
            if not file_exist:
                print(f'file {inputfile} is not exist')
                sys.exit()
        elif opt in ('-o', '--outputfolder'):
            outputfolder = arg +'/'+ inputfile
            if not os.path.exists(outputfolder):
                os.makedirs(outputfolder)
    process(inputfile, outputfolder)


def process(inputfile, outputfolder):
    cap = cv2.VideoCapture(inputfile)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    current_frame = 0
    index = 0

    while current_frame <= frame_count:
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        success, img = cap.read()

        if not success:
            break

        img = compress(img)
        image_name = os.path.join(outputfolder, f'img_{index}.jpg')
        cv2.imwrite(image_name, img)
        current_frame += fps
        index += 1
    cap.release()


def compress(img):
    down_width = 640
    down_height = 480
    down_points = (down_width, down_height)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized_down = cv2.resize(
        gray, down_points, interpolation=cv2.INTER_LINEAR)
    return resized_down


if __name__ == "__main__":
    main(sys.argv[1:])
