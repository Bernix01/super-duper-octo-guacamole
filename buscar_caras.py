import face_recognition
import cv2
# import pyttsx3
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

# engine = pyttsx3.init("nsss")
# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
# pedro_image = face_recognition.load_image_file("pedro.jpg")
paulette_image = face_recognition.load_image_file("paulette.jpg")
fernando_image = face_recognition.load_image_file("fernando.jpg")
kevin_image = face_recognition.load_image_file("kevin.jpg")
guillermo_image = face_recognition.load_image_file("guillermo.jpg")
elgabriel_image = face_recognition.load_image_file("elgabriel.PNG")
la13 = face_recognition.load_image_file("13.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
paulette_face_encoding = face_recognition.face_encodings(paulette_image)[0]
# pedro_face_encoding = face_recognition.face_encodings(pedro_image)[0]
# fernando_face_encoding = face_recognition.face_encodings(fernando_image)[0]
kevin_face_encoding = face_recognition.face_encodings(kevin_image)[0]
guillermo_face_encoding = face_recognition.face_encodings(guillermo_image)[0]
la13_encoding = face_recognition.face_encodings(la13)[0]
elgabriel_encoding = face_recognition.face_encodings(elgabriel_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    frame = increase_brightness(frame,20)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
            name = "no reconocido"

            if match[0]:
                name = "Barack"
            if face_recognition.compare_faces([guillermo_face_encoding], face_encoding)[0]:
                name = "Guillermo"
            if face_recognition.compare_faces([la13_encoding],face_encoding)[0]:
                name = "La Trece"
            if face_recognition.compare_faces([elgabriel_encoding],face_encoding)[0]:
                name = "Gabriel"
            # if face_recognition.compare_faces([fernando_face_encoding],face_encoding)[0]:
            #     name = "Fernando"
            if face_recognition.compare_faces([kevin_face_encoding],face_encoding)[0]:
                name = "Kevin San"
            # if face_recognition.compare_faces([pedro_face_encoding],face_encoding)[0]:
            #     name = "Pedro"
            if face_recognition.compare_faces([paulette_face_encoding],face_encoding)[0]:
                name = "Paulette"

            face_names.append(name)
            # engine.say(name)
            # engine.runAndWait()

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()