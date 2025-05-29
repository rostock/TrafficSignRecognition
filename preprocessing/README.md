# Scripts for Image Preprocessing

To limit the large amount of data to the most important and to structure it clearly, a script was developed that fulfills the following functions:

1. **Filtering of consecutive images of the same street** (too similar images)
2. **Shuffling of images**
3. **Splitting the image set into the three splits "train," "val," and "test"**
4. **Copying the images into a new, flatter folder structure**

The script works with the folder structure of the sample data. These images are located in folders like:

```
Photos/0770079603/050_052_/SXA000053.jpg
```

These images are filtered and copied to a new folder path like:

```
Photos_filtered/train/0770079603_050_052_SXA000053.jpg
```

With this structure, it is easy to import the images into CVAT, while still retaining information about the original image paths.

The folder paths as well as the ratio of the different splits are configurable.  
As default values, 70% was set for training, 20% for test, and 10% for validation.

