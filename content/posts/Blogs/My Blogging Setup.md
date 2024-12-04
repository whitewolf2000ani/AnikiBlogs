---
title: My blogging setup
date: 03/12/2025
---
## Why am I doing this?
- A Repository or a store for whatever cool concepts I study/Understand.
- It's really important to showcase and learn in Public.
## How am I doing this?
- Obsidian https://obsidian.md/
- ![Image Description](/images/Pasted_image_20241203121609.png)
- Hugo for building the static website blazingly fast. 
## Why are we using HUGO?
The simple answer is HUGO directly converts Markdown files to Website code directly(Isn't this convenient😁)
- Prerequisites for Hugo
	- Git -> Install According to Operating System.
		- Prompt: How do Install Git in "Operating System".
	- Go -> Install According to Operating System.
		- Prompt: How to Install Go in "Operating system".
-  Install HUGO following the official documentation https://gohugo.io/installation/linux/

## The next Steps
- Create a Folder for your blogs.
- Move into that folder and use command
``` Terminal
hugo new site <NameOfSite>
```
- The required files will be created.
- Initialize a Git repository
``` Terminal
git init
```
- Choose a exciting theme of choice. -> https://themes.gohugo.io/
	- After choosing a theme, -> https://themes.gohugo.io/themes/hugo-theme-terminal/
	- Find "Install theme as submodule" this is the easiest and best way to use the Theme.
``` Terminal
//similar to this command 
git submodule add -f https://github.com/panr/hugo-theme-terminal.git themes/terminal
```
- We need to configure the "config.toml" file in order to render the theme (e.g. Config file for terminal theme)
``` config.toml 

// Example config for terminal theme
baseurl = "/" 
languageCode = "en-us" 
# Add it only if you keep the theme in the `themes` directory. 
# Remove it if you use the theme as a remote Hugo Module. 
theme = "terminal" 
paginate = 5 

[params] 
# dir name of your main content (default is `content/posts`). 
# the list of set content will show up on your index page (baseurl). 
contentTypeName = "posts" 

# if you set this to 0, only submenu trigger will be visible 
showMenuItems = 2 
# show selector to switch language 
showLanguageSelector = false 
# set theme to full screen width 
fullWidthTheme = false 
# center theme with default width 
centerTheme = false 

# if your resource directory contains an image called `cover.(jpg|png|webp)`, 

# then the file will be used as a cover automatically. 

# With this option you don't have to put the `cover` param in a front-matter. 
autoCover = true 

# set post to show the last updated # If you use git, you can set `enableGitInfo` to `true` and then post will automatically get the last updated 
showLastUpdated = false 

# Provide a string as a prefix for the last update date. By default, it looks like this: 2020-xx-xx [Updated: 2020-xx-xx] :: Author 
# updatedDatePrefix = "Updated" # whether to show a page's estimated reading time # readingTime = false # default 
# whether to show a table of contents 
# can be overridden in a page's front-matter 
# Toc = false # default 
# set title for the table of contents 
# can be overridden in a page's front-matter 
# TocTitle = "Table of Contents" 
# default [params.twitter] 
# set Twitter handles for Twitter cards 
# see https://developer.twitter.com/en/docs/tweets/optimize-with-cards/guides/getting-started#card-and-content-attribution 
# do not include 
@ creator = "" 
site = "" 
[languages] 
	[languages.en] 
		languageName = "English" 
		title = "Terminal" 
	
	[languages.en.params] 
		subtitle = "A simple, retro theme for Hugo" 
		owner = "" 
		keywords = "" 
		copyright = "" 
		menuMore = "Show more" 
		readMore = "Read more" 
		readOtherPosts = "Read other posts" 
		newerPosts = "Newer posts" 
		olderPosts = "Older posts" 
		missingContentMessage = "Page not found..." 
		missingBackButtonLabel = "Back to home page" 
		minuteReadingTime = "min read" 
		words = "words" 
		[languages.en.params.logo] 
			logoText = "Terminal" 
			logoHomeLink = "/" 
		[languages.en.menu] 
			[[languages.en.menu.main]] 
				identifier = "about" 
				name = "About" 
				url = "/about" 
			[[languages.en.menu.main]] 
				identifier = "showcase" 
				name = "Showcase" 
				url = "/showcase"
```
- After this a simple command of 
``` Terminal
hugo server -t <themename>
```

## Now lets see some text rendering? 🖋️
- But there seems to be problem😐 that, the obsidian blog folder and our hugo blog folder are in different locations.
- The content in them should almost sync simultaneously.
- We solve this problem using a very specific command

linux
``` Terminal
rsync -av --delete "sourcepath" "destinationpath"
```

Windows
```
robocopy sourcepath destination path /mir
```


## Now lets render the images
- One more problem that we see is the rendering of images.
- The problem arises because obsidian keeps a different attachments folder for media.
- Now we need to copy the images used in our blog to the Hugo codebase.
- So we will use a python script to copy all the used images from the attachments folder to folder inside static/images/
- Create a python script known as images.py and copy the below script 
``` Python
# create a directory inside static known as images and then use the below code.
import os
import re
import shutil
  
# Paths
posts_dir = "/home/aniketkumar/blogs/AnikiBlog/content/posts/Blogs"
attachments_dir = r"/mnt/c/Users/kanik/OneDrive/Documents/MAIN/101 templates"
static_images_dir = "/home/aniketkumar/blogs/AnikiBlog/static/images"

# Ensure static images directory exists
if not os.path.exists(static_images_dir):
    os.makedirs(static_images_dir)
# Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r") as file:
            content = file.read()
        # Find all image links in the format `![Image Description](/images/filename.png)`
        images = re.findall(r"!\[\[([^]]+\.png)\]\]", content)
        for image in images:
            # Original filename with spaces
            image_with_spaces = image
            # Markdown-compatible filename with `%20`
            image_with_encoded_spaces = image.replace(" ", "%20")
            # Path to the original image
            image_source = os.path.join(attachments_dir, image_with_spaces)
            print(f"Checking for image: {image_source}")
            # Replace Markdown link with a Hugo-compatible link
            new_image_link = f"![Image Description](/images/{image_with_encoded_spaces})"
            content = content.replace(f"![[{image_with_spaces}]]", new_image_link)
            # Copy the image to the static directory if it exists
            if os.path.exists(image_source):
                # Copy the image to the static directory without changing its name
                shutil.copy(image_source, os.path.join(static_images_dir, image_with_spaces))
                print(f"Copied: {image_source} -> {static_images_dir}/{image_with_spaces}")
            else:
                print(f"Image not found: {image_source}")

        # Write updated content back to the file
        with open(filepath, "w") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")

```
- After using the below script run
```terminal
python3 images.py
```
- This will copy all the images used in the current blog to the images folder inside static
![Image Description](/images/Pasted_image_20241203173907.png)

- After the images are copied again run the file syncing command and start the Hugo server.
![Image Description](/images/Pasted_image_20241203181859.png)

## Do we always have to run the sync command then copy the images?
- The simple answer is yes, but we will automate the entire task using a long python script at the end of the blog.

## Now let's put this for people to see 😁
- Remember the "git init" command we used to initialize a git repository now we will use this.
- Step 1: Go to www.github.com
- Step 2: Create a new repository
- step 3: Connect the local repository to your remote repository
``` Terminal
git remote add origin </ssh /https link>
```
- step 4: Run Hugo to create all the necessary changes
``` Terminal
hugo
```
- Step 5: Now commit add and commit these changes to the locally 
``` Terminal
git add.  
git commit -m "My, first commit to the blog"
```
- Step 6: Push these changes to GitHub/ remote.
```
git push -u origin master
```
- Now we will be able to see the changes in our Github Repository.

## Now the moment of Truth, where should we host our website 🤔?
- Vercel/ GitHub pages/ Hostinger
- I personally will be using GitHub pages
	- It's good for static websites.
	- It's free 😍
- Choice made, lets get on to it.