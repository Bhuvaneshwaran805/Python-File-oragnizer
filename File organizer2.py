from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".doc"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"]
}


def organize_files():

    folder_path = filedialog.askdirectory(
        title="Select a folder to organize"
    )

    if not folder_path:
        return

    folder = Path(folder_path)

    confirm = messagebox.askyesno(
        "Confirm",
        f"Organize files in:\n{folder}?"
    )

    if not confirm:
        return

    moved = 0
    skipped = 0
    errors = 0
    report = []

    for file in list(folder.iterdir()):

        if not file.is_file():
            continue

        destination = "Others"

        for category, extensions in categories.items():
            if file.suffix.lower() in extensions:
                destination = category
                break

        target = folder / destination
        new_file = target / file.name

        if new_file.exists():
            skipped += 1
            report.append(f"Skipped: {file.name}")
            continue

        try:
            target.mkdir(exist_ok=True)
            shutil.move(str(file), str(new_file))

            moved += 1
            report.append(
                f"Moved: {file.name} -> {destination}"
            )

        except OSError as error:
            errors += 1
            report.append(f"Error: {file.name} - {error}")

    report_path = folder / (
        "organizer_report_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".txt"
    )

    report.append(f"\nTotal moved: {moved}")
    report.append(f"Total skipped: {skipped}")
    report.append(f"Total errors: {errors}")

    try:
        report_path.write_text(
            "\n".join(report),
            encoding="utf-8"
        )
    except OSError as error:
        messagebox.showerror(
            "Report Error",
            str(error)
        )

    messagebox.showinfo(
        "Completed",
        f"Moved: {moved}\n"
        f"Skipped: {skipped}\n"
        f"Errors: {errors}\n\n"
        f"Report: {report_path}"
    )


# Create application window
root = tk.Tk()
root.title("Python File Organizer")
root.geometry("400x250")

title = tk.Label(
    root,
    text="Automatic File Organizer",
    font=("Arial", 16, "bold")
)
title.pack(pady=25)

button = tk.Button(
    root,
    text="Browse and Organize",
    command=organize_files,
    font=("Arial", 12),
    padx=15,
    pady=10
)
button.pack(pady=20)

footer = tk.Label(
    root,
    text="Powered by Python",
    font=("Arial", 9)
)
footer.pack()

root.mainloop()