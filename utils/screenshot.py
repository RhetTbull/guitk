"""Take screenshots of a GUItk window for use in documentation"""

import argparse
import importlib
import os
import pathlib
import subprocess
import sys
from collections import namedtuple

import guitk as ui

# Note: this uses macOS specific utilities and will not work on other platforms
# I develop on macOS so this works for me. I tried to use pyautogui but it
# did not run on macOS Ventura, see: https://github.com/asweigart/pyautogui/issues/783

# Some of the code in this module is based on the code in [tkcap](https://github.com/ghanteyyy/tkcap)
# which is licensed under the MIT license, Copyright (c) 2020 ghanteyyy

Region = namedtuple("Region", "x y width height")


def screencapture(region: Region, filename: pathlib.Path):
    """Capture a screenshot of a region and save it to filename as PNG using screencapture utility on macOS"""
    command = f"screencapture -R{region.x},{region.y},{region.width},{region.height} -t png {filename}"
    os.system(command)


def get_display_resolution():
    """Hack to get display resolution on macOS"""

    command = 'system_profiler SPDisplaysDataType | grep "UI Looks like"'
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    resolution = output.split(":")[1].strip()
    resolution = resolution.split("@")[0]
    width, height = resolution.split(" x ")
    return int(width), int(height)


def load_class(pyfile: str, class_name: str):
    """Load function_name from python file pyfile"""
    module_file = pathlib.Path(pyfile)
    if not module_file.is_file():
        raise FileNotFoundError(f"module {pyfile} does not appear to exist")

    module_dir = module_file.parent or pathlib.Path(os.getcwd())
    module_name = module_file.stem

    # store old sys.path and ensure module_dir at beginning of path
    syspath = sys.path
    sys.path = [str(module_dir)] + syspath
    module = importlib.import_module(module_name)

    try:
        class_ = getattr(module, class_name)
    except AttributeError as e:
        raise ValueError(f"'{class_name}' not found in module '{module_name}'") from e
    finally:
        # restore sys.path
        sys.path = syspath

    return class_


class ScreenshotRunner(ui.Window):
    """Take screenshot of a GUItk window"""

    def __init__(
        self,
        window_class: type[ui.Window],
        output: str,
        overwrite: bool,
        delay: int,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.window_class = window_class
        self.output = output
        self.overwrite = overwrite
        self.delay = delay

    def config(self):
        """Configure the window"""
        self.title = "Screenshot Runner"
        self.size = get_display_resolution()
        with ui.VLayout():
            ui.Frame(weightx=1, weighty=1).style(bg="black")

    def setup(self):
        """Setup the window"""
        # create a timer to open the target window
        self.snapshot_timer = self.bind_timer_event(1000, "<<target_window>>")

    @ui.on("<<target_window>>")
    def on_target(self):
        """Show the target window and start timer for the screenshot"""
        self.target_window = self.window_class()
        # self.window.withdraw()
        self.bind_timer_event(self.delay, "<<capture>>")

    @ui.on("<<capture>>")
    def on_capture(self):
        """Capture the screenshot and quit"""
        region, path = self.capture()
        print(f"Screenshot of region {region} saved to {path}")

        self.target_window.quit()
        self.quit()

    def get_region(self):
        """Get x-coordinate, y-coordinate, width and height of the tkinter target window"""
        # this is a hack to get the window size and may not work on all platforms

        target = self.target_window
        target.window.update()
        x_pos, y_pos = target.window.winfo_x(), target.window.winfo_y()
        if x_pos >= 1:
            x_pos -= 1
        width, height = target.window.winfo_width() + 1, target.window.winfo_height() + 29
        return Region(x_pos, y_pos, width, height)

    def capture(self):
        """Capture and save screenshot of the tkinter window and save to self.image_filename"""

        path = pathlib.Path(self.output).expanduser().absolute()
        if path.exists() and not self.overwrite:
            raise FileExistsError(f"Output file aleady exists: {path}")

        if self.overwrite and path.exists():
            path.unlink()

        region = self.get_region()
        screencapture(region, path)
        return region, path


def main():
    """Take screenshot of a GUItk window and save to file"""
    parser = argparse.ArgumentParser(
        description="Take screenshot of a GUItk window and save to file"
    )
    parser.add_argument("file", help="Python file to run")
    parser.add_argument("classname", help="Window class to instantiate")
    parser.add_argument("output", help="Output file name")
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite output file", default=False
    )
    parser.add_argument(
        "--delay",
        type=int,
        help="Delay before screenshot in milliseconds",
        default=1000,
    )
    args = parser.parse_args()
    print(args)
    classname = load_class(args.file, args.classname)
    ScreenshotRunner(
        window_class=classname,
        output=args.output,
        overwrite=args.overwrite,
        delay=args.delay,
    ).run()


if __name__ == "__main__":
    main()
