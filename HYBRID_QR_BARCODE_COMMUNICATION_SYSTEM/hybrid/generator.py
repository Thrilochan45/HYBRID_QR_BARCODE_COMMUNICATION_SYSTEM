from typing import Optional
from PIL import Image
import qrcode
import barcode
from barcode.writer import ImageWriter
from hybrid.utils import output_path
import os

def generate_qr(data: str, filename: Optional[str] = None, box_size=10) -> str:
    if not filename:
        filename = "qr.png"
    out = output_path(filename)
    qr = qrcode.QRCode(version=1, box_size=box_size, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out)
    return out

def generate_barcode(data: str, filename: Optional[str] = None, code_class: str = "code128") -> str:
    if not filename:
        filename = "barcode.png"
    out = output_path(filename)
    BAR = barcode.get_barcode_class(code_class)
    bar = BAR(data, writer=ImageWriter())
    bar.save(out.replace(".png", ""))
    return out
