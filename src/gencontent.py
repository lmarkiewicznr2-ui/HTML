import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    title = extract_title(markdown)
    body_node = markdown_to_html_node(markdown)

    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    # Insert Title & Content
    final_html = template_html.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", body_node.to_html())

    # Rewrite URLs to respect basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                rel_dir = os.path.relpath(root, dir_path_content)
                if rel_dir == ".":
                    dest_subdir = dest_dir_path
                else:
                    dest_subdir = os.path.join(dest_dir_path, rel_dir)

                os.makedirs(dest_subdir, exist_ok=True)

                content_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_subdir, file.replace(".md", ".html"))

                generate_page(content_path, template_path, dest_file_path, basepath)
