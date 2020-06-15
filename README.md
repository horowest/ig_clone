# Ig_clone

![Image 1](https://raw.githubusercontent.com/himanshup/instagram-clone/master/screenshots/image1.png)  
An instagram like clone built with python and flask.

## Features

- Sign up for an account and edit avatar/username later on
- Upload images with captions and option to delete posts.
- Comment on posts and option to delete them
- Like/unlike posts
- Follow/unfollow users
- Feed consists of posts from users you follow 
-'Explore' page has posts from every user
- Notifications on activities on your posts.

## Features to add
- Tag feature
- Search option for users and tags
- Display followers/following (on profile)

## Running Locally

Follow these instructions to get this project up and running on your machine.  

### Prerequisites
1. Postgresql database
2. AWS S3 bucket

### Installing
```
git clone https://github.com/horowest/ig_clone
cd ig_clone
pip install -r requirements.txt
```

Set environments for the following following:

```
DATABASEURL=postgres://localhost/<dbname>
S3_BUCKET=<bucket_name>
S3_ACCESS_KEY=<access_key>
S3_SECRET_KEY=<secret_key>
```

Set ```debug=1``` on main.py
