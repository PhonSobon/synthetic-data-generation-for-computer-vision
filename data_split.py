import os
import random
import shutil

def split_data(train_ratio=0.8):
    """
    Splits image and label data (both .txt and .xml) into training 
    and validation sets.

    This function assumes that for every image file, there is a 
    corresponding .txt and .xml label file with the same base name.

    Args:
        train_ratio (float): The proportion of data for training. 
                             Defaults to 0.8 (80%).
    """
    # === CONFIGURATION ===
    # Define paths to your source folders
    image_source = 'synthetic_images'
    label_source = 'synthetic_labels'       # For .txt files
    xml_label_source = 'synthetic_xml_labels' # <-- ADDED for .xml files
    
    # Define the base output directory
    output_base = 'data'
    
    # Define label extensions
    label_ext = '.txt'
    xml_ext = '.xml' # <-- ADDED
    # =====================

    print("--- Starting Data Split (including XML) ---")

    # 1. Setup paths for destination folders
    train_img_path = os.path.join(output_base, 'img', 'train')
    val_img_path = os.path.join(output_base, 'img', 'val')
    train_label_path = os.path.join(output_base, 'label', 'train')
    val_label_path = os.path.join(output_base, 'label', 'val')
    train_xml_path = os.path.join(output_base, 'xml_label', 'train') # <-- ADDED
    val_xml_path = os.path.join(output_base, 'xml_label', 'val')     # <-- ADDED

    # 2. Create the required directory structure
    print(f"Creating directory structure at: '{output_base}'")
    for path in [train_img_path, val_img_path, train_label_path, val_label_path, train_xml_path, val_xml_path]:
        os.makedirs(path, exist_ok=True)

    # 3. Get a list of all image files and shuffle them
    try:
        all_images = [f for f in os.listdir(image_source) if os.path.isfile(os.path.join(image_source, f))]
        random.shuffle(all_images)
        print(f"Found {len(all_images)} images to split.")
    except FileNotFoundError:
        print(f"ERROR: Source image directory not found at '{image_source}'. Please check the path.")
        return

    # 4. Calculate the split point
    split_index = int(len(all_images) * train_ratio)
    train_files = all_images[:split_index]
    val_files = all_images[split_index:]

    # 5. Define a helper function to move files
    def move_files(filenames, img_dest, label_dest, xml_dest): # <-- MODIFIED: added xml_dest
        moved_count = 0
        for img_name in filenames:
            base_name, _ = os.path.splitext(img_name)
            label_name = base_name + label_ext
            xml_name = base_name + xml_ext # <-- ADDED

            # Construct full source paths
            src_img = os.path.join(image_source, img_name)
            src_label = os.path.join(label_source, label_name)
            src_xml = os.path.join(xml_label_source, xml_name) # <-- ADDED

            # Check if all three corresponding files exist
            if os.path.exists(src_img) and os.path.exists(src_label) and os.path.exists(src_xml):
                shutil.move(src_img, os.path.join(img_dest, img_name))
                shutil.move(src_label, os.path.join(label_dest, label_name))
                shutil.move(src_xml, os.path.join(xml_dest, xml_name)) # <-- ADDED
                moved_count += 1
            else:
                print(f"Warning: Skipping '{img_name}' as a corresponding label (.txt or .xml) was not found.")
        return moved_count

    # 6. Move the files to their new homes
    print(f"\nMoving {len(train_files)} file sets to the training set...")
    moved_train = move_files(train_files, train_img_path, train_label_path, train_xml_path) # <-- MODIFIED
    
    print(f"\nMoving {len(val_files)} file sets to the validation set...")
    moved_val = move_files(val_files, val_img_path, val_label_path, val_xml_path) # <-- MODIFIED
    
    print("\n--- Data Split Complete ---")
    print(f"Training set: {moved_train} image/label/xml sets.")
    print(f"Validation set: {moved_val} image/label/xml sets.")
    print("---------------------------\n")

# This part allows you to run the script directly from the command line
if __name__ == '__main__':
    split_data(train_ratio=0.8)