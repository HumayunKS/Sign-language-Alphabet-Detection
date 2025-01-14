from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
import shutil  # For copying the original image

# Define augmentation parameters
datagen = ImageDataGenerator(
    width_shift_range=0.2,     # Randomly shift images horizontally (20% of width)
    height_shift_range=0.2,    # Randomly shift images vertically (20% of height)
    shear_range=0.2,           # Randomly apply shearing transformations
    zoom_range=0.2,            # Randomly zoom in or out
    horizontal_flip=True,      # Randomly flip images horizontally
    fill_mode='nearest',       # Fill missing pixels after transformations
    brightness_range=[0.8, 1.2]  # Randomly adjust brightness
)

# Define input and output paths
input_folder = r"C:\Users\humtw\OneDrive\Desktop\University Files\Semester 7\Machine Learning\Project\new test\A"
output_folder = os.path.join(
    r"C:\Users\humtw\OneDrive\Desktop\University Files\Semester 7\Machine Learning\Project\new test\DataT",
    "AugmentedHH"
)

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Augment each image
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        
        # Copy the original image to the output folder
        shutil.copy(img_path, os.path.join(output_folder, f"original_{filename}"))
        
        # Perform augmentations
        img = load_img(img_path)  # Load the image as PIL format
        x = img_to_array(img)     # Convert to NumPy array
        x = x.reshape((1,) + x.shape)  # Reshape to (1, height, width, channels)

        # Generate and save augmented images
        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=output_folder, save_prefix='aug', save_format='jpeg'):
            i += 1
            if i >= 10:  # Generate 10 augmented images per input image
                break
