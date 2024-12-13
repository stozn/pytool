# 安装所需的库
# pip install PyPDF2 pdf2image

from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os
from pdf2image import convert_from_path

def merge_pdfs(pdf_list, output_pdf):
    """将多个PDF文件合并成一个PDF文件。"""
    pdf_writer = PdfWriter()
    
    # 遍历每个PDF文件，将其中的页面加入到合并的PDF中
    for pdf in pdf_list:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    
    # 将合并后的内容写入到输出PDF文件
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

def pdf_to_images(pdf_path):
    """将PDF的每一页提取为图像。"""
    return convert_from_path(pdf_path)

def create_4x4_page(images, output_size=(3508, 2480)):
    """将16张图片合并为一个4x4的页面。"""
    rows, cols = 4, 4  # 4行4列
    width, height = output_size  # 输出页面的宽和高
    cell_width, cell_height = width // cols, height // rows  # 每个单元格的宽度和高度

    # 创建一个白色的空白画布
    canvas = Image.new('RGB', (width, height), 'white')

    # 将每张图片按照4x4的布局放入画布中
    for idx, img in enumerate(images):
        row, col = divmod(idx, cols)  # 根据索引计算行列位置
        # 将图片调整为适合单元格大小
        img = img.resize((cell_width, cell_height), Image.Resampling.LANCZOS)  # 使用LANCZOS高质量重采样
        # 将图片粘贴到画布的指定位置
        canvas.paste(img, (col * cell_width, row * cell_height))

    return canvas

def process_pdf(input_pdf, output_pdf):
    """处理PDF文件，将每16页合并为一个4x4的页面。"""
    images = pdf_to_images(input_pdf)  # 将PDF转换为图片
    total_pages = len(images)  # 获取总页数
    output_images = []

    # 每16页合成一个4x4页面
    for i in range(0, total_pages, 16):
        # 获取接下来的16页图片
        group = images[i:i+16]
        # 如果剩余页数少于16页，补充空白页
        while len(group) < 16:
            group.append(Image.new('RGB', (group[0].width, group[0].height), 'white'))
        # 创建4x4页面
        page = create_4x4_page(group)
        output_images.append(page)

    # 将所有4x4页面保存到新的PDF文件中
    output_images[0].save(output_pdf, save_all=True, append_images=output_images[1:])

if __name__ == "__main__":
    # Step 1: 合并1.pdf到5.pdf这5个PDF文件为一个PDF
    pdf_list = [f"{i}.pdf" for i in range(1, 6)]  # PDF文件列表
    merged_pdf = "merged.pdf"  # 合并后的PDF文件名
    if not os.path.exists("output"):
        os.makedirs("output")  # 如果输出文件夹不存在，则创建

    # 合并PDF文件
    merge_pdfs(pdf_list, merged_pdf)
    print(f"合并后的PDF已保存到 {merged_pdf}")

    # Step 2: 将合并后的PDF转换为图像，并创建4x4的布局
    output_pdf = "output/merged_4x4.pdf"  # 输出的4x4布局PDF文件
    process_pdf(merged_pdf, output_pdf)
    print(f"合并后的4x4布局PDF已保存到 {output_pdf}")
