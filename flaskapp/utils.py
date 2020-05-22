import os
import secrets
from PIL import Image
from flaskapp import app

OUT_SIZE = {'pfp': (125, 125)}


def save_picture(picture, pic_type):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    pic_fname = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics/', pic_fname)
    
    # resize and save
    i = Image.open(picture)
    i.thumbnail(OUT_SIZE[pic_type])
    i.save(pic_path)

    # return filename
    return pic_fname