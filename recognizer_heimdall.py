import face_recognition
import cv2
import imutils
#import pyttsx3
import json
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other
# demos that don't require it instead.


def recognize(image):
    #engine = pyttsx3.init("sapi5")
    # Load a sample picture and learn how to recognize it.
    obama_image = face_recognition.load_image_file("obama.jpg")
    guillermo_image = face_recognition.load_image_file("guillermo.jpg")
    elgabriel_image = face_recognition.load_image_file("elgabriel.PNG")
    la132 = face_recognition.load_image_file("13.2.jpg")
    la13 = face_recognition.load_image_file("13.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    guillermo_face_encoding = face_recognition.face_encodings(guillermo_image)[
        0]
    la13_encoding = face_recognition.face_encodings(la13)[0]
    la132_encoding = face_recognition.face_encodings(la132)[0]
    elgabriel_encoding = face_recognition.face_encodings(elgabriel_image)[0]
    print("loaded face encodings")
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    image = cv2.imread(image)
    small_frame = cv2.resize(image, (0, 0), fx=1/3, fy=1/3)
    print("scaled down pro")
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    face_names = []
    print(face_encodings)
    print(face_locations)
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(
            [obama_face_encoding], face_encoding)
        name = "Unknown"

        if match[0]:
            name = "Barack"
        if face_recognition.compare_faces([guillermo_face_encoding], face_encoding)[0]:
            name = "Guillermo"
        if face_recognition.compare_faces([la13_encoding,la132_encoding], face_encoding)[0]:
            name = "La Trece"
        if face_recognition.compare_faces([elgabriel_encoding], face_encoding)[0]:
            name = "Gabriel"
        face_names.append(name)
    print(face_locations)
    print(face_encodings)
    return json.dumps(face_names, sort_keys=True, indent=2)


def main(argv):
    reloader = '--reloader' in argv
    print('Starting with reloader={}'.format(reloader))
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=reloader)

if __name__ == '__main__':
    main(sys.argv)