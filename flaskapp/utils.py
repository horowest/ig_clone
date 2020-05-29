import os
import secrets
from PIL import Image
from flaskapp import app

OUT_SIZE = {'pfp': (125, 125), 'media': (200, 200)}


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


def save_media(picture, pic_type):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(picture.filename)
    pic_fname = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/media/', pic_fname)
    
    i = Image.open(picture)
    # resize and save
    bwidth = 600
    ratio = bwidth / float(i.size[0])
    height = int((float(i.size[1]) * ratio))
    i = i.resize((bwidth, height), Image.ANTIALIAS)
    i.save(pic_path)

    # save thumb now
    j = Image.open(picture)

    bwidth = 300
    ratio = bwidth / float(j.size[0])
    height = int((float(j.size[1]) * ratio))
    j = j.resize((bwidth, height), Image.ANTIALIAS)
    thumb_path = os.path.join(app.root_path, 'static/media/', 'thumb' + pic_fname)
    j.save(thumb_path)

    # return filename
    return pic_fname