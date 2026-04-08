import os

# thư mục gốc của repo study-library
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(ROOT_DIR, "..")  # nhảy ra khỏi thư mục tool
ROOT_DIR = os.path.abspath(ROOT_DIR)

# Đường dẫn gốc
DATA_DIR = "../study-library/data"

# Exams
EXAMS_INPUT_DIR = f"{DATA_DIR}/exams/input"
EXAMS_OUTPUT_DIR = f"{DATA_DIR}/exams/output"

# Books
BOOKS_INPUT_DIR = f"{DATA_DIR}/books/input"
BOOKS_OUTPUT_DIR = f"{DATA_DIR}/books/output"

# Articles
ARTICLES_DIR = f"{DATA_DIR}/articles"

# Cấu hình xử lý ảnh/PDF
DPI = 300
IMAGE_WIDTH = 1200
WATERMARK_TEXT = "studylibrary.com"

# Google Drive folder IDs
DRIVE_EXAMS_INPUT_ID = "1JDnVLOPWflA2E9tr2HOAiTF__wegYqER"    # ID folder input exams
DRIVE_EXAMS_OUTPUT_ID = "1jqDM23yaoZcSQ05LY-dNkMpUErQV_oXq"   # ID folder output exams
DRIVE_BOOKS_INPUT_ID = "1GDFWgPwRzMbHFQe1H2WCrMRII4PNYUA6"          # ID folder books
DRIVE_BOOKS_OUTPUT_ID = "1e4sW_JM4TR6fDFrkcEkdJiHfiQwzobPu"          # ID folder books
DRIVE_ARTICLES_ID = "..."       # ID folder articles

# Cờ điều khiển
FORCE_UPDATE = True

GITHUB_PAGE_URL = "https://nhathinh2703.github.io/study-library/"