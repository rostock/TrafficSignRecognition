from ultralytics import YOLO

def train(dataset : str) -> None:
    # Load a pretrained YOLOv8 model
    model = YOLO("models/yolov8n.pt")

    # Define the path to your custom dataset YAML file
    custom_dataset_yaml = "../datasets/"+dataset+"/data.yaml"

    # Train the model on your custom dataset
    train_results = model.train(data=custom_dataset_yaml, epochs=100, imgsz=640)

    # Evaluate the model's performance on the validation set
    val_results = model.val()

    # Perform object detection on a test image
    results = model("../datasets/"+dataset+"/test.jpg")

    # Export the model to ONNX format
    success = model.export(format="onnx")
    model.save("models/retrained.pt")
    print(results, success)