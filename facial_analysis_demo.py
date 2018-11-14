import boto3
import cv2
import os
from pprint import pprint


FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")


def detect_faces(image_blob, attributes=['ALL']):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_faces(
        Image={
            'Bytes': image_blob
        },
        Attributes=attributes,
    )
    return response['FaceDetails']


def img_matrix_to_bytes(img, tmp_img_file):
    cv2.imwrite(tmp_img_file, img)
    with open(tmp_img_file, 'rb') as f:
        img_bytes = f.read()
    os.remove(tmp_img_file)
    return img_bytes


def wait_for_space_pressed():
    while (cv2.waitKey(1) & 0xFF) != ord(' '): pass


def draw_results(img, results):
    img = img.copy()
    img_h, img_w, _ = img.shape
    for face in results:
        # drawing face bounding box
        bbox = face['BoundingBox']
        bbx1 = int((bbox['Left'] if bbox['Left'] >= 0 else 0) * img_w)
        bbx2 = int(bbx1 + (bbox['Width'] if bbox['Width'] >= 0 else 0) * img_w)
        bby1 = int((bbox['Top'] if bbox['Top'] >= 0 else 0) * img_h)
        bby2 = int(bby1 + (bbox['Height'] if bbox['Height'] >= 0 else 0) * img_h)
        cv2.rectangle(img, (bbx1, bby1), (bbx2, bby2), (0, 255, 0), 2)

        # drawing annotations
        age_low = face['AgeRange']['Low']
        age_high = face['AgeRange']['High']
        gender = face['Gender']['Value']
        emotions = face['Emotions']  # Are by default sorted by confidence
        top_emotion = emotions[0]['Type']
        top_emotion_conf = emotions[0]['Confidence']
        annotation_line_1 = f'{gender}, {age_low}-{age_high} yo'
        annotation_line_2 = f'Emotion: {top_emotion}, {top_emotion_conf:.2f}%'
        cv2.putText(img, annotation_line_1, (bbx1 - 30, bby2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
        cv2.putText(img, annotation_line_2, (bbx1 - 30, bby2 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))

    return img


def img_from_disc_detection():
    TEST_IMG_PATH = 'sandbox/test_1.jpg'
    with open(TEST_IMG_PATH, 'rb') as f:
        content = f.read()
    faces = detect_faces(content)
    for face in faces:
        print(face)
        print(face.keys())  # dict_keys(['BoundingBox', 'AgeRange', 'Smile', 'Eyeglasses', 'Sunglasses', 'Gender', 'Beard', 'Mustache', 'EyesOpen', 'MouthOpen', 'Emotions', 'Landmarks', 'Pose', 'Quality', 'Confidence'])


def main():
    tmp_img_file = 'tmp.jpg'

    cv2.namedWindow('whatever', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('whatever', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    while True:

        cv2.imshow('whatever', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            img_bytes = img_matrix_to_bytes(frame, tmp_img_file)
            faces = detect_faces(img_bytes)
            frame_annotated = draw_results(frame, faces)
            cv2.imshow('whatever', frame_annotated)
            for face in faces:
                pprint(face)
            wait_for_space_pressed()

        _, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
