import os
import config

def generate_html(page_name, title, section_file=None, section_content=None):
    with open(config.LAYOUT_FILE, "r", encoding="utf-8") as f:
        layout = f.read()

    if section_file:
        with open(section_file, "r", encoding="utf-8") as f:
            section = f.read()
    else:
        section = section_content or ""

    html = layout.replace("{{title}}", title).replace("{{section}}", section)

    output_path = os.path.join(config.HTML_OUTPUT_DIR, page_name)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Đã sinh {output_path}")


def generate_index_html():
    """Sinh riêng trang chủ index.html"""
    section_content = """
    <!-- Hero -->
    <section class="hero">
      <h1>Chào mừng đến với Thư viện học tập</h1>
      <p class="subtitle">Nơi tổng hợp đề thi, học liệu và bài viết hữu ích cho học sinh, giáo viên và người yêu thích Tin học.</p>
    </section>
    <!-- Features -->
    <section class="features">
      <h1>Chức năng chính</h1>
      <p class="subtitle">Khám phá các mục nổi bật của thư viện</p>
      <div class="card-container">...</div>
    </section>
    <!-- Intro -->
    <section class="intro">
      <h1>Lời ngỏ</h1>
      <p class="subtitle">Thư viện học tập được xây dựng với mong muốn...</p>
    </section>
    """
    generate_html("index.html", "Thư viện học tập - Trang chủ", section_content=section_content)