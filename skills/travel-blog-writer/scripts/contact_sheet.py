"""받은 사진을 한 장의 미리보기로 모은다 (내용 검수용). 필요: pip install pillow
사용법: python -I contact_sheet.py <사진폴더> <출력.jpg>"""
import sys, os
from PIL import Image, ImageDraw
d = sys.argv[1]
fs = sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".jpeg", ".png")))
W, H, cols = 360, 240, 5
rows = (len(fs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W, rows * (H + 20)), "white"); dr = ImageDraw.Draw(sheet)
for i, f in enumerate(fs):
    try:
        im = Image.open(os.path.join(d, f)).convert("RGB"); im.thumbnail((W, H))
    except Exception:
        print("깨진 파일 (지우고 다시 받으세요):", f); continue
    x, y = (i % cols) * W, (i // cols) * (H + 20)
    sheet.paste(im, (x, y + 20)); dr.text((x + 4, y + 4), f, fill="black")
sheet.save(sys.argv[2])
