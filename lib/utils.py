from cloudinary.uploader import upload

async def upload_image(file):
    # Upload the image to Cloudinary
    result = upload(file.file)

    image_url = result['secure_url']

    return image_url