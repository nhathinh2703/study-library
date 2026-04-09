import os

# thư mục gốc của repo study-library
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(ROOT_DIR, "..")  # nhảy ra khỏi thư mục tool
ROOT_DIR = os.path.abspath(ROOT_DIR)

# Đường dẫn gốc data
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Layout và output HTML
LAYOUT_FILE = os.path.join(ROOT_DIR, "docs", "assets", "layout", "layout.txt")
HTML_OUTPUT_DIR = os.path.join(ROOT_DIR, "docs")

# Section files
SECTION_EXAM_FILE = os.path.join(DATA_DIR, "exams", "output", "section_exams.txt")
SECTION_BOOK_FILE = os.path.join(DATA_DIR, "books", "output", "section_books.txt")

# Exams
EXAMS_INPUT_DIR = os.path.join(DATA_DIR, "exams", "input")
EXAMS_OUTPUT_DIR = os.path.join(DATA_DIR, "exams", "output")

# Books
BOOKS_INPUT_DIR = os.path.join(DATA_DIR, "books", "input")
BOOKS_OUTPUT_DIR = os.path.join(DATA_DIR, "books", "output")

# Articles
ARTICLES_DIR = os.path.join(DATA_DIR, "articles")

# Cấu hình xử lý ảnh/PDF
DPI = 300
IMAGE_WIDTH = 1200
WATERMARK_TEXT = "studylibrary.com"

# Google Drive folder IDs
DRIVE_EXAMS_INPUT_ID = "1JDnVLOPWflA2E9tr2HOAiTF__wegYqER"
DRIVE_EXAMS_OUTPUT_ID = "1jqDM23yaoZcSQ05LY-dNkMpUErQV_oXq"
DRIVE_BOOKS_INPUT_ID = "1GDFWgPwRzMbHFQe1H2WCrMRII4PNYUA6"
DRIVE_BOOKS_OUTPUT_ID = "1e4sW_JM4TR6fDFrkcEkdJiHfiQwzobPu"
DRIVE_ARTICLES_ID = "..."

# Cờ điều khiển
FORCE_UPDATE = False

GITHUB_PAGE_URL = "https://nhathinh2703.github.io/study-library/"
