"""Insta485 development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
# SECRET_KEY = '''b'B\xb8\xda\xcc\xb6,
#     \x02\x1c\x9d&\xf4\xb6\x02/\xf7\x1b`\xd5\xb1\xb4,\xdc\x08e'''
# SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SCRAPS_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SCRAPS_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = SCRAPS_ROOT/'var'/'scraps.sqlite3'
