import os
import re
import shutil

# Paths
posts_dir = "/home/aniketkumar/blogs/AnikiBlog/content/posts/Blogs"
attachments_dir = r"/mnt/c/Users/kanik/OneDrive/Documents/MAIN/101 templates"
static_images_dir = "/home/aniketkumar/blogs/AnikiBlog/static/images"

# Base URL for Hugo
baseURL = "https://whitewolf2000ani.github.io/AnikiBlogs"

# Ensure static images directory exists
if not os.path.exists(static_images_dir):
    os.makedirs(static_images_dir)

# Function to normalize image names (replace spaces with underscores)
def normalize_image_name(image_name):
    return image_name.replace(" ", "_")

# Process each Markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r") as file:
            content = file.read()

        # Find all image links in the format `![[filename.extension]]`
        images = re.findall(r"!\[\[([^]]+\.(?:png|jpg|jpeg|gif|webp))\]\]", content)

        for image in images:
            # Normalize the image filename
            normalized_image_name = normalize_image_name(image)
            
            # Original and normalized filenames
            image_with_spaces = image
            image_with_encoded_spaces = normalized_image_name

            # Path to the original image
            image_source = os.path.join(attachments_dir, image_with_spaces)
            print(f"Checking for image: {image_source}")

            # Replace Markdown link with a Hugo-compatible link
            new_image_link = f"![Image Description]({baseURL}/images/{image_with_encoded_spaces})"
            content = content.replace(f"![[{image_with_spaces}]]", new_image_link)

            # Copy the image to the static directory if it exists
            if os.path.exists(image_source):
                # Copy the image to the static directory with a normalized name
                shutil.copy(image_source, os.path.join(static_images_dir, normalized_image_name))
                print(f"Copied: {image_source} -> {static_images_dir}/{normalized_image_name}")
            else:
                print(f"Image not found: {image_source}")

        # Write updated content back to the file
        with open(filepath, "w") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
