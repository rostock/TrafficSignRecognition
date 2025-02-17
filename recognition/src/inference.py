from ultralytics import YOLO
import cv2
import numpy as np

def inference(dataset_path_absolute: str) -> None:
    # Load a pretrained YOLOv8 model
    model = YOLO("models/retrained.pt")

    img_path = dataset_path_absolute+"/test.jpg"

    # Perform object detection on a test image
    results = model(img_path)

    # Load the original image
    original_image = cv2.imread(img_path)

    # Visualize the results on the image
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB)  # convert BGR to RGB

        # Overlay segmentation masks
        if r.masks is not None:
            for mask in r.masks:
                mask_array = mask.data.cpu().numpy()
                mask_array = cv2.resize(mask_array, (original_image.shape[1], original_image.shape[0]))
                mask_color = np.random.randint(0, 255, size=(3,))
                mask_overlay = np.where(mask_array[..., None], mask_color, [0, 0, 0])
                im = cv2.addWeighted(im, 1, mask_overlay.astype(np.uint8), 0.5, 0)

    # Save the output image
    cv2.imwrite("output/segmentation.jpg", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))

    print("Segmentation visualization saved as output/segmentation.jpg")
    print(results)