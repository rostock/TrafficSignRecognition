import os
import glob
from datetime import datetime
from pathlib import Path
from selectors import SelectSelector

from ultralytics import YOLO
from ultralytics.models.yolo.detect import DetectionTrainer


def find_latest_checkpoint(base_dir="runs/train"):
    experiment_dirs = [d for d in os.listdir(base_dir) if d.startswith('experiment_')]
    experiment_dirs.sort()

    if experiment_dirs:
        newest_experiment = experiment_dirs[-1]
        last_pt_path = os.path.join(base_dir, newest_experiment, 'weights', 'last.pt')
        if os.path.isfile(last_pt_path):
            return last_pt_path
        else:
            print('No last checkpoint found at {}'.format(last_pt_path))
            return False
    else:
        print("No experiment folders found.")


def log_training_info(trainer: DetectionTrainer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    epoch = trainer.epoch

    print(f"\n🔄 Epoch {epoch} finished on {timestamp}")

    if hasattr(trainer, 'metrics') and trainer.metrics:
        print(f"📈 Current Metrics:")
        for key, value in trainer.metrics.items():
            if isinstance(value, (int, float)):
                print(f"   - {key}: {value:.4f}")

    if hasattr(trainer, 'loss') and trainer.loss is not None:
        print(f"📉 Current Loss: {trainer.loss:.4f}")


def save_checkpoint_with_timestamp(trainer: DetectionTrainer):
    epoch = trainer.epoch

    try:
        trainer.save_model()
        print(f"💾 Checkpoint saved to {trainer.last}")


        metadata_folder = os.path.join(trainer.save_dir, "metadata")
        os.makedirs(metadata_folder, exist_ok=True)
        metadata_path = os.path.join(metadata_folder, f"checkpoint_epoch_{epoch:03d}_metadata.txt")
        with open(metadata_path, 'w') as f:
            f.write(f"Checkpoint Information\n")
            f.write(f"====================\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Epoch: {epoch}\n")
            f.write(f"Model: {trainer.args.model}\n")
            f.write(f"Dataset: {trainer.args.data}\n")

            if hasattr(trainer, 'best_fitness') and trainer.best_fitness is not None:
                f.write(f"Best Fitness: {trainer.best_fitness}\n")
            if hasattr(trainer, 'metrics') and trainer.metrics:
                f.write(f"Metrics: {trainer.metrics}\n")

        print(f"📝 Saved Metadaten to: {metadata_path}")

    except Exception as e:
        print(f"❌ Error saving the checkpoint: {e}")


def train(dataset_path_absolute: str, try_resume: bool) -> None:
    os.system("yolo settings tensorboard=True")

    latest_checkpoint =  find_latest_checkpoint() if try_resume else False

    resume_training = try_resume and latest_checkpoint

    if try_resume and not latest_checkpoint:
        print("🆕 No Checkpoint found, starting new")
    elif resume_training:
        print(f"🔄 Found Checkpoint to resume training: {latest_checkpoint}")
    else:
        print("🆕 Starting new training")

    model_path = latest_checkpoint if resume_training else "models/yolov8n.pt"
    model = YOLO(model_path)

    model.add_callback("on_train_epoch_end", log_training_info)
    model.add_callback("on_model_save", save_checkpoint_with_timestamp)

    custom_dataset_yaml = dataset_path_absolute + "/data.yaml"

    # Training-Parameter
    training_params = {
        "data": custom_dataset_yaml,
        "epochs": 5,
        "imgsz": 640,
        "save": True,
        "save_period": 1,  # save every n-th epoch
        "project": "runs/train",
        "name": f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "exist_ok": True,
        "plots": True,
        "device": None,  # detect automatically
    }

    if resume_training:
        training_params["resume"] = True

    print("⚙️  Training Parameters:")
    for key, value in training_params.items():
        print(f"   - {key}: {value}")

    try:
        print("\n🎯 Start Training:")

        train_results = model.train(**training_params)

        print("✅ Training completed! Starting evaluation...")
        val_results = model.val()

        # test example image
        test_image_path = dataset_path_absolute + "/test.jpg"
        if os.path.exists(test_image_path):
            print(f"🔍 Test-Prediction for: {test_image_path}")
            results = model(test_image_path)
        else:
            print("⚠️ Did not found test prediction image, skipping...")
            results = None

        try:
            success = model.export(format="onnx")
            print("📦 ONNX exported successfully!")
        except Exception as e:
            print(f"❌ ONNX-Export failed: {e}")
            success = False

        # save final model
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_model_path = f"models/retrained_{timestamp_str}.pt"
        os.makedirs("models", exist_ok=True)
        model.save(final_model_path)
        print(f"💾 Saved final model to {final_model_path}")

        print(
            "\n🎨 For visualization, start tensorboard with tensorboard --logdir runs/train/experiment_... and then open: http://localhost:6006/")

        # return train_results, val_results, results, success

    except Exception as e:
        print(f"❌ Error during Training: {e}")
        raise
