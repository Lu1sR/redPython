import qrcode
import uuid
import boto3
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from io import BytesIO
s3 = boto3.resource('s3')
REDIRECT_URL = 'https://7i0rlcm1v2.execute-api.us-east-1.amazonaws.com/validate-ticket'
def createQR(number, email):
    bucket = s3.Bucket("thehottestpartytickets")
    client = boto3.client('s3')
    obj = []
    for i in range(0,number):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        id = uuid.uuid4()
        qr.add_data(f'{REDIRECT_URL}?token={id}')
        img_2 = qr.make_image(image_factory=StyledPilImage)
        size = 500, 500
        fg = img_2.convert('RGBA')
        fg = fg.resize(size)
        base = Image.open("base.png").convert("RGBA")

        # img = Image.new('RGB', (50, 25))
        # d = ImageDraw.Draw(img)
        # d.text((20, 20), 'Hello', fill=(255, 0, 0))

        # img.save("text.png", format="png")
        # Calculate width to be at the center
        width = (base.width - fg.width) // 2

        # Calculate height to be at the center
        height = ((base.height - fg.height) // 2) + 125

        # Paste the fg at (width, height)
        base.paste(fg, (width, height), fg)

        # Save this image
        #base.save("new.png", format="png")
        
        in_mem_file = BytesIO()
        base.save(in_mem_file, format="png")
        in_mem_file.seek(0)

        response = bucket.put_object(Key = f'{str(id)}.png', Body=in_mem_file)
        file_name = f'{str(id)}.png'
        obj.append({'id': str(id), 'email': email, 's3File': file_name , 'identifier': str(id).split('-')[1]})
    return obj