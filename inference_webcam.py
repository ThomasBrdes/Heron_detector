import cv2
import argparse
import torch

from ultralytics import YOLO
import supervision as sv
import numpy as np

# based on this https://github.com/SkalskiP/yolov8-live

ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    parser.add_argument(
        "--skip-frames", 
        default=1, 
        type=int, 
        help="Process every N-th frame"
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Load the model with GPU support if available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = YOLO("best.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    # zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    # zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    # zone_annotator = sv.PolygonZoneAnnotator(
    #     zone=zone, 
    #     color=sv.Color.red(),
    #     thickness=2,
    #     text_thickness=4,
    #     text_scale=2
    # )

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Skip frames to increase processing speed
        if frame_count % args.skip_frames == 0:
            result = model(frame, agnostic_nms=True)[0]
            detections = sv.Detections.from_ultralytics(result)

            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for (xyxy, confidence, class_id, *_) in zip(detections.xyxy, detections.confidence, detections.class_id)
            ]
            print(labels)
            frame = box_annotator.annotate(
                scene=frame, 
                detections=detections, 
                labels=labels
            )

            # zone.trigger(detections=detections)
            # frame = zone_annotator.annotate(scene=frame)      

        cv2.imshow("yolov8", frame)
        frame_count += 1

        if (cv2.waitKey(1) == 27):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
