import cv2

thresh = 0.45  # Threshold to detect objects
nms = 0.2

# Import coco dataset
class_file = '/tmp/pycharm_project_754/coco.names'
with open(class_file, 'r') as names_file:
    class_names = names_file.read().rstrip('\n').split('\n')
print(class_names)

# Import config and weights files
config_path = '/tmp/pycharm_project_754' \
              '/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weights_path = '/tmp/pycharm_project_754/frozen_inference_graph.pb'
# Settings
net = cv2.dnn_DetectionModel(weights_path, config_path)
net.setInputSize((320, 320))
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def get_objects(img, thresh, nms, draw=True, objects=[]):
    '''
    :param img: image from video
    :param draw: if True, draw on screen. If False, do not draw on screen
    :param objects: list of objects to draw for
    :return: img = image with CV info, object_info = box and ID that will be
    printed, even if not drawn
    '''
    # confidence - if below value, ignore. bbox = bounding box
    class_ids, confidence, bbox = net.detect(img, confThreshold=thresh,
                                             nmsThreshold=nms)
    #print(class_ids, bbox)

    # If no object is specified by user, display all objects
    if len(objects) == 0:
        objects = class_names

    # List of objects that will be returned
    object_info = []

    if len(class_ids) != 0:
        for class_id, conf_level, box in zip(class_ids.flatten(),
                                             confidence.flatten(), bbox):
            # Put info into list (useful if not drawing
            class_name = class_names[class_id - 1]
            # print('box', box, '\n')

            if class_name in objects:
                object_info.append([box, class_name, conf_level])

                if draw:
                    # Display box around object
                    cv2.rectangle(img, box, color=(180, 100, 200), thickness=4)

                    # Display ID text
                    # subtract 1 from class_id bc class_names list starts at 0
                    # dimensions are (width, height)
                    cv2.putText(img, class_names[class_id - 1], (box[0]+10, box[1]+30),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (180, 100, 200), 2)

                    # Display confidence text
                    cv2.putText(img, str(round(conf_level*100, 2)), (box[0] + 10,
                                                                  box[1] + 75),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (180, 100, 200), 2)
                #print('class name:', class_name, '\n', 'box:', box, '\n',
                      #'conf:', conf_level*100, '\n', '\n')

    return img, object_info


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    # Set width (3) and height (4)
    cap.set(3, 640)
    cap.set(4, 480)
    # cap.set(10, 70)  # Brightness
    while True:
        success, img = cap.read()
        # Can specify objects to detect using: objects=["person", "cup"]
        result, object_info = get_objects(img, thresh, nms, objects=['person'])
        print(object_info)
        # Turn on webcam
        cv2.imshow('Webcam', result)
        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break