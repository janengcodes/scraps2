"""scraps development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (
    b'z\x8a\\b\xb2\xca\xcc\xf0l\x91q\xb2\x99<t\xd0)\xe9\xfbGv\x0f\x93\xb4'
)
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SCRAPS_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SCRAPS_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/scraps485.sqlite3
DATABASE_FILENAME = SCRAPS_ROOT/'var'/'scraps.sqlite3'
