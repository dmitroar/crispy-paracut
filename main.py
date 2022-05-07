import sys, getopt, os
import cv2
import numpy as np

def main(argv):
   inputfile = ''
   outputfolder = ''
   try:
      opts, _ = getopt.getopt(argv,'hi:o:',['help=', 'inputfile=','outputfolder='])
   except getopt.GetoptError:
      print('crispy.py -i <inputfile> -o <outputfolder>')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ('-h', '--help'):
         print('crispy.py -i <inputfile> -o <outputfolder>')
         sys.exit()
      elif opt in ('-i', '--inputfile'):
         inputfile = os.path.expanduser('~/' + arg)
         file_exist = os.path.exists(inputfile)
         if not file_exist:
            print(f'file {inputfile} is not exist') 
      elif opt in ('-o', '--outputfolder'):
         outputfolder = os.path.expanduser('~/' + arg)
         if not os.path.exists(outputfolder):
            os.makedirs(outputfolder)

   print(f'Input file is {inputfile}')
   print(f'Output folder is {outputfolder}')
   process(inputfile, outputfolder)

def process(inputfile, outputfolder):
    cap = cv2.VideoCapture(inputfile)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    while True:
         success = False
         frameId = cap.get(1)
         id = cap.get(cv2.CAP_PROP_POS_FRAMES)
         success, img = cap.read()

         if id % fps == 0:
            img = compress(img)
            image_name = os.path.join(outputfolder, f'img_{id / fps}.jpg')
            cv2.imwrite(image_name, img)
         if not success:
            print('process finish')
            return
         

def compress(img):
   return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

if __name__ == "__main__":
   main(sys.argv[1:])