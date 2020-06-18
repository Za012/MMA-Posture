The code architecture is simple, under controllers is the underlying ui logic and eventhandlers.
under managers folder is most of the file processors and Machine learning stuff.

To get this application working, openpose must be built inside the openpose folder.

Inside the ML folder there's a jupyter notebook used for testing and model optimization purposes.

Included is the MainModel, this is the best model we've trained. We've included a small part of the video that was used to train this model under the RAWDATA folder 

https://www.youtube.com/watch?v=9eOBnIq07bQ this is the full video. (we know its boxing but a good mma video consisting of one person couldn't be found :c)
The first 3000 frames was used to train. A snippet (the included video) of the last minutes of the video was taken out to validate how the frame by frame prediction would work inside the application.
