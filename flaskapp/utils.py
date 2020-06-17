import os
import secrets
from PIL import Image
from flaskapp import app
import boto3
from flaskapp.config import S3_BUCKET, S3_BUCKET_LOC, S3_ACCESS_KEY, S3_SECRET_KEY

OUT_SIZE = {'pfp': (125, 125), 'media': (200, 200)}


def save_picture(picture, pic_type):# open s3 instance
    s3 = boto3.resource('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    pic_fname = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics/', pic_fname)
    
    # resize and save
    i = Image.open(picture)
    i.thumbnail(OUT_SIZE[pic_type])
    i.save(pic_path)

    s3.meta.client.upload_file(pic_path, S3_BUCKET, 'profile_pics/' + pic_fname, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/' + f_ext[1:]})

    # return filename
    return pic_fname


def save_media(picture, pic_type):
    # open s3 instance
    s3 = boto3.resource('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

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

    s3.meta.client.upload_file(pic_path, S3_BUCKET, 'media/' + pic_fname, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/' + f_ext[1:]})

    # save thumb now
    j = Image.open(picture)

    bwidth = 125
    ratio = bwidth / float(j.size[0])
    height = int((float(j.size[1]) * ratio))
    j = j.resize((bwidth, height), Image.ANTIALIAS)
    thumb_path = os.path.join(app.root_path, 'static/media/', 'thumb' + pic_fname)
    j.save(thumb_path)

    s3.meta.client.upload_file(thumb_path, S3_BUCKET, 'media/thumb' + pic_fname, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/' + f_ext[1:]})
    # save display image for explore and user page
    k = Image.open(picture)

    bwidth = 500
    ratio = bwidth / float(j.size[0])
    height = int((float(j.size[1]) * ratio))
    k = k.resize((bwidth, height), Image.ANTIALIAS)
    mid_path = os.path.join(app.root_path, 'static/media/', 'mid' + pic_fname)
    k.save(mid_path)

    s3.meta.client.upload_file(mid_path, S3_BUCKET, 'media/mid' + pic_fname, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/' + f_ext[1:]})

    # return filename
    return pic_fname


def get_file_url(f_path):
    url = f'https://{S3_BUCKET}.s3.{S3_BUCKET_LOC}.amazonaws.com/{f_path}'
    return url


def delete_file(f_path):
    s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
    for item in ['media/', 'media/mid', 'media/thumb']:
        s3.delete_object(Bucket=S3_BUCKET, Key=item + f_path)