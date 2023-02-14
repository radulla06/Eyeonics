import cv2


def identify_objects(img_url, show_img=False):
    img = cv2.imread(img_url)

    class_file = 'coco.names'
    with open(class_file, 'rt') as f:
        class_names = f.read().rstrip('\n').split('\n')

    config_path = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weights_path = 'frozen_inference_graph_2.pb'

    net = cv2.dnn_DetectionModel(weights_path, config_path)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    
    max_conf = 0
    closest_object = "None detected"

    if show_img:
        class_ids, confs, bounding_box = net.detect(img, confThreshold=0.2)

        if len(class_ids) > 0:
            for classId, confidence, box in zip(class_ids.flatten(), confs.flatten(), bounding_box):
                if confidende > max_conf:
                    max_conf = confidence
                    closest_object = classId
                cv2.rectangle(img, box, color=(255, 0, 0), thickness=4)
                cv2.putText(img, class_names[classId].upper(), (box[0] + 10, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 170, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow('Output', img)
            cv2.waitKey(0)

    return closest_object
