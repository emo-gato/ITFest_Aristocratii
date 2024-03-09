import cv2

class VideoPlayer:

    #\brief: Initializes the video player
    #\param[in]: videoSource - the path to the video file
    def __init__(self, video_source):
        self.video = video_source  # Store the video source in the 'video' attribute

        self.isPlaying = False
        self.isPaused = False
        self.current_frame = None
    
    #\brief: Handles the 'Play' button click
    def playButton(self):
        if not self.isPlaying:
            self.isPlaying = True
            self.isPaused = False

    #\brief: Handles the 'Pause' button click
    def pauseButton(self):
        self.isPaused = True
        self.isPlaying = False

    #\brief: Handles the 'Rewind' button click
    def rewindButton(self):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.isPlaying = True
        self.isPaused = False

    #\brief: Retrieves a frame from the video source
    #\return: Returns the retrieved frame in RGB
    def getFrame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None