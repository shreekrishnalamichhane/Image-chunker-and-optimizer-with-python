import os
from PIL import Image, ImageOps

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def compress_img(src,dst,image_name, new_size_ratio=0.9, quality=90, width=None, height=None, to_jpg=True):
    # print(src,dst,image_name, new_size_ratio, quality, width, height, to_jpg)
    # load the image to memory
    img = Image.open(src + image_name)
    img = ImageOps.exif_transpose(img)
    # print the original image shape
    # print("[*] Image shape:", img.size)
    # get the original image size in bytes
    image_size = os.path.getsize(src + image_name)
    # print the size before compression/resizing
    # print("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        # print new image shape
        # print("[+] New Image shape:", img.size)
    elif width and height:
        # if width and height are set, resize with them instead
        img = img.resize((width, height), Image.ANTIALIAS)
        # print new image shape
        # print("[+] New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name
    if to_jpg:
        # change the extension to JPEG
        new_file_path = f"{dst}/{filename}.jpg"
    else:
        # retain the same extension of the original image
        new_file_path = f"{filename}{ext}"
    try:
        pass
        # save the image with the corresponding quality and optimize set to True
        img.save(new_file_path, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")

        # save the image with the corresponding quality and optimize set to True
        img.save(new_file_path, quality=quality, optimize=True)

    # print("[+] New file saved:", new_file_path)
    # get the new image size in bytes
    new_image_size = os.path.getsize(new_file_path)
    # print the new size in a good format
    # print("[+] Size after compression:", get_size_format(new_image_size))
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    return -(saving_diff)
    # print the saving percentage
    # print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size. Space Saved {get_size_format(-(saving_diff))}")


