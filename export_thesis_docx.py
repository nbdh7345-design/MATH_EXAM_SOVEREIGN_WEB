# -*- coding: utf-8 -*-
"""
export_thesis_docx.py - Chuyển đổi Báo cáo Đồ án Tốt nghiệp Markdown sang Word DOCX chuẩn học thuật
Khổ giấy A4, Lề 1 inch (2.54cm), Font Times New Roman 13pt, Giãn dòng 1.3, Tiêu đề phân cấp.
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(BASE_DIR, "BAO_CAO_DO_AN_TOT_NGHIEP.md")
DOCX_PATH = os.path.join(BASE_DIR, "BAO_CAO_DO_AN_TOT_NGHIEP.docx")


def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_thesis_docx():
    doc = docx.Document()

    # Cấu hình lề trang A4 chuẩn 1 inch (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.2)  # lề gáy đóng cuốn
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Cấu hình Normal style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(15, 23, 42)
    style.paragraph_format.line_spacing = 1.3
    style.paragraph_format.space_after = Pt(6)

    with open(MD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    in_code_block = False
    code_lines = []
    in_table = False
    table_lines = []

    for line in lines:
        stripped = line.strip()

        # Xử lý khối mã nguồn ```
        if stripped.startswith('```'):
            if in_code_block:
                # Kết thúc code block
                in_code_block = False
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.3)
                p.paragraph_format.space_after = Pt(8)
                run = p.add_run('\n'.join(code_lines))
                run.font.name = 'Consolas'
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(30, 41, 59)
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Xử lý bảng Markdown | ... |
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            # Render bảng đã tích lũy
            in_table = False
            render_markdown_table(doc, table_lines)
            table_lines = []

        if not stripped:
            continue

        # Tiêu đề cấp 1 (# )
        if stripped.startswith('# '):
            text = stripped[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(17)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
            if 'BÁO CÁO' in text or 'ĐỀ TÀI' in text:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            continue

        # Tiêu đề cấp 2 (## )
        if stripped.startswith('## '):
            text = stripped[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(14.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 58, 138)
            if 'NGHIÊN CỨU' in text or 'ĐỀ TÀI' in text:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            continue

        # Tiêu đề cấp 3 (### )
        if stripped.startswith('### '):
            text = stripped[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
            continue

        # Danh sách gạch đầu dòng (* hoặc -)
        if stripped.startswith('* ') or stripped.startswith('- '):
            text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.line_spacing = 1.25
            p.paragraph_format.space_after = Pt(4)
            add_formatted_runs(p, text)
            continue

        # Danh sách đánh số (1. 2. ...)
        match_num = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if match_num:
            num = match_num.group(1)
            text = match_num.group(2)
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.line_spacing = 1.25
            p.paragraph_format.space_after = Pt(4)
            add_formatted_runs(p, text)
            continue

        # Khối trích dẫn / Ghi chú (> )
        if stripped.startswith('> '):
            text = stripped[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(text)
            run.font.italic = True
            run.font.color.rgb = RGBColor(71, 85, 105)
            continue

        # Đường kẻ ngang (---)
        if stripped == '---':
            continue

        # Đoạn văn thông thường
        p = doc.add_paragraph()
        if '<div align="center">' in stripped or '<div align="right">' in stripped:
            continue
        if stripped.endswith('</div>'):
            continue
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(6)
        add_formatted_runs(p, stripped)

    doc.save(DOCX_PATH)
    print(f"Generated successfully: {DOCX_PATH}")


def add_formatted_runs(paragraph, text):
    """Xử lý in đậm **text**, in nghiêng *text*, code `text`"""
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`|\$.*?\$)', text)
    for t in tokens:
        if not t:
            continue
        if t.startswith('**') and t.endswith('**') and len(t) >= 4:
            run = paragraph.add_run(t[2:-2])
            run.bold = True
        elif t.startswith('*') and t.endswith('*') and len(t) >= 2:
            run = paragraph.add_run(t[1:-1])
            run.italic = True
        elif t.startswith('`') and t.endswith('`') and len(t) >= 2:
            run = paragraph.add_run(t[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(194, 65, 12)
        elif t.startswith('$') and t.endswith('$') and len(t) >= 2:
            run = paragraph.add_run(t[1:-1])
            run.font.italic = True
            run.font.color.rgb = RGBColor(30, 58, 138)
        else:
            paragraph.add_run(t)


def render_markdown_table(doc, table_lines):
    rows_data = []
    for l in table_lines:
        cells = [c.strip() for c in l.strip('|').split('|')]
        # Bỏ dòng phân cách |--|--|
        if any(set(c).issubset({'-', ':', ' '}) for c in cells):
            continue
        rows_data.append(cells)

    if not rows_data:
        return

    num_cols = max(len(r) for r in rows_data)
    table = doc.add_table(rows=len(rows_data), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    for r_idx, row in enumerate(rows_data):
        is_header = (r_idx == 0)
        for c_idx in range(num_cols):
            cell_text = row[c_idx] if c_idx < len(row) else ''
            cell = table.cell(r_idx, c_idx)
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(cell_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)

            if is_header:
                run.bold = True
                run.font.color.rgb = RGBColor(15, 23, 42)
                set_cell_background(cell, 'E2E8F0')  # Xám nhạt
            else:
                set_cell_background(cell, 'F8FAFC' if r_idx % 2 == 1 else 'FFFFFF')

            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)


if __name__ == '__main__':
    create_thesis_docx()
