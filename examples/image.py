"""Demo how to use images with guitk"""

import pathlib

import guitk as ui

# test whether pillow is installed
try:
    import PIL

    PIL = True
except ImportError:
    PIL = False

# set image path so code works if run in examples/ or root dir
if pathlib.Path("image.png").exists():
    IMAGE_FILE = "image.png"
elif pathlib.Path("./examples/image.png").exists():
    IMAGE_FILE = "./examples/image.png"
else:
    raise RuntimeError("image.png not found")

if pathlib.Path("button.png").exists():
    BUTTON_FILE = "button.png"
elif pathlib.Path("./examples/button.png").exists():
    BUTTON_FILE = "./examples/button.png"

if pathlib.Path("image.jpg").exists():
    JPG_FILE = "image.jpg"
elif pathlib.Path("./examples/image.jpg").exists():
    JPG_FILE = "./examples/image.jpg"

print(f"Using image file: {IMAGE_FILE}, PIL={PIL}")


class ImageDemo(ui.Window):
    def config(self):
        self.size = 600, 600
        with ui.VLayout(valign="center", halign="center"):
            with ui.HStack(halign="center"):
                ui.Label(
                    "Images can be displayed in a Label, a Button, or using an Image widget.\n"
                    "Only GIF and PNG images are supported by tkinter."
                )
            with ui.NoteBook():
                with ui.VTab("Label", valign="center", halign="center"):
                    ui.Label(
                        "Label with image",
                        key="image_label",
                        image=IMAGE_FILE,
                        compound="top",
                    )
                with ui.VTab("Button", valign="center", halign="center"):
                    ui.Button(
                        "Button with image", key="image_button", image=BUTTON_FILE
                    )
                with ui.VTab("Image", valign="center", halign="center"):
                    ui.Image(IMAGE_FILE, key="image")
                with ui.VTab("Image with text", valign="center", halign="center"):
                    # compound = top means the image is above the text
                    ui.Image(
                        IMAGE_FILE,
                        text="An image of a palm tree",
                        key="image",
                        compound="top",
                    )
                with ui.VTab("Clickable Image", valign="center", halign="center"):
                    ui.Image(IMAGE_FILE, key="image_events", events=True)
                if PIL:
                    with ui.VTab("JPEG Image", valign="center", halign="center"):
                        ui.Image(JPG_FILE, key="image_jpg")
                else:
                    with ui.VTab("JPEG Image", valign="center", halign="center"):
                        ui.Label("Pillow not installed, cannot load JPEG image")
            ui.Label("", key="status")

    def handle_event(self, event: ui.Event):
        self["status"].value = f"Event: {event.key}: {event.event_type}"


if __name__ == "__main__":
    ImageDemo().run()
