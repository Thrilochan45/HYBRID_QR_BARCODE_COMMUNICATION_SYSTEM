import tkinter as tk
from tkinter import filedialog, messagebox
from hybrid.generator import generate_qr, generate_barcode
from hybrid.scanner import scan_image
from PIL import ImageTk, Image

def main():
    root = tk.Tk()
    root.title("HYBRID QR & BARCODE COMMUNICATION SYSTEM")
    root.geometry("600x400")

    tk.Label(root, text="Enter Data").pack()
    entry = tk.Entry(root, width=50)
    entry.pack()

    def generate_qr_code():
        data = entry.get()
        if not data:
            messagebox.showerror("Error", "Enter data!")
            return
        path = generate_qr(data, "gui_qr.png")
        messagebox.showinfo("QR Generated", f"Saved to {path}")

    def generate_bar_code():
        data = entry.get()
        if not data:
            messagebox.showerror("Error", "Enter data!")
            return
        path = generate_barcode(data, "gui_barcode.png")
        messagebox.showinfo("Barcode Generated", f"Saved to {path}")

    tk.Button(root, text="Generate QR", command=generate_qr_code).pack(pady=5)
    tk.Button(root, text="Generate Barcode", command=generate_bar_code).pack(pady=5)

    def scan_image_file():
        file = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not file:
            return
        results = scan_image(file)
        if results:
            data_text = "\n".join([r["data"] for r in results])
            messagebox.showinfo("Scan Results", data_text)
        else:
            messagebox.showinfo("Scan Results", "No codes found.")

    tk.Button(root, text="Scan Image", command=scan_image_file).pack(pady=5)
    root.mainloop()
