import cv2

isGray = 0
isRGB = 1
    
class getFrame:
     #\brief Gets video feed and checks the video structure(width, height, fps & colour pattern(rgb/grayscale))
        #\param [in]: video - VideoCapture object for capturing frames.
        #\param [out]: width - Width of the video frames.
        #\param [out]: height - Height of the video frames.
        #\param [out]: fps - Frames per second(of the video).
        #\param [in/out]: checkedType - Flag indicating if color type has been checked.
        #\param [in/out]: colorPattern - Color pattern of the video frames.
        #\return : None 
        #\globals: None
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.checkedType = False
        self.colorPattern = -1
    
    def run(self):
        try:
            while True:
                success, frame = self.video.read()

                if not success:
                    break

                if not self.checkedType:
                    if len(frame.shape) < 3:
                        self.colorPattern = isGray
                    elif len(frame.shape) == 3:
                        self.colorPattern = isRGB

                    self.checkedType = True

                yield frame

        finally:
            self.video.release()

