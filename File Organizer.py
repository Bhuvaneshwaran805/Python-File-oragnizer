from pathlib import Path
import shutil

folder = Path(input("Enter folder path:").strip().strip('"'))

if not folder.is_dir():
    print("Invalid folder path!")
    raise SystemExit
categories ={
    "Image":[".jpg",".jpeg",".png"],
    "Docments":[".pdf",".docx",".txt"],
    "Videos":[".mp4",".mkv",],
    "Audio":[".mp3",".wav"],
}
#destination
for file in folder.iterdir():

    if not file.is_file():
        continue
    destination ="others"
    for category, extensions in categories.items():
        if file.suffix.lower() in extensions:
            destination = category
            break

    print(file.name,"----->",destination)
confirm =input("\nMove these files? (Yes/No):")
if confirm.lower() =="yes":
        for file in list(folder.iterdir()):
            if not file.is_file():
                continue

            destination = "Others"

            for category,extensions in categories.items():
                if file.suffix.lower() in extensions:
                    destination = category
                    break

            target = folder /destination
            target.mkdir(exist_ok=True)

            new_file = target / file.name
            #not overwriting
            if new_file.exists():
                print("Skipped:", file.name)
                continue

            shutil.move(str(file), str(new_file))

        print("Organization Completed")

else:
        print("No file were moved.")