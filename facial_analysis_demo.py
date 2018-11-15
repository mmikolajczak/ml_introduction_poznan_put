"""
Facial recognition/analysis demo script (using aws online service), with simple opencv interface.
After running, you take a snap to analyse by pressing space, then after some time for request processing,
the result will be visible on screen. Press space again to return exit snap results and return to camera mode.
Press q to quit (not in results mode).
(This script assumes that the camera is enabled, and aws account/credentials are configured).
"""
import boto3
import cv2
import os
from pprint import pprint


def detect_faces(image_blob, attributes=['ALL']):
    """
    :param image_blob: image (encoded in jpg/png) bytes representation
    :param attributes: optional filter of analysis option
    :return:
    """
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_faces(
        Image={
            'Bytes': image_blob
        },
        Attributes=attributes,
    )
    return response['FaceDetails']


def img_matrix_to_bytes(img, tmp_img_file):
    """
    :param img: image opencv matrix (np.array)
    :param tmp_img_file: name/path of temporary "buffer file" used to conversion
    :return: bytes representation of image encoded in jpg/png (depends of extension of tmp_img_file)
    """
    cv2.imwrite(tmp_img_file, img)
    with open(tmp_img_file, 'rb') as f:
        img_bytes = f.read()
    os.remove(tmp_img_file)
    return img_bytes


def wait_for_space_pressed():
    while (cv2.waitKey(1) & 0xFF) != ord(' '): pass


def draw_annotations(img, results):
    """
    :param img: image opencv matrix (np.array)
    :param results: results of face analysis from AWS api response (dict)
    :return: image opencv matrix, with annotations drawn (np.array)
    """
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


def main():
    tmp_img_file = 'tmp.jpg'
    window_name = 'whatever'

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    while True:

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            img_bytes = img_matrix_to_bytes(frame, tmp_img_file)
            faces = detect_faces(img_bytes)
            frame_annotated = draw_annotations(frame, faces)
            cv2.imshow(window_name, frame_annotated)
            for face in faces:
                pprint(face)
            wait_for_space_pressed()

        _, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
