# Welcome to GUITk's documentation!

GUITk is a declarative framework for building nice-looking, cross-platform GUIs with [tkinter](https://docs.python.org/3/library/tkinter.html) inspired by [SwiftUI](https://developer.apple.com/documentation/swiftui).

GUITk allows you to build complete GUI applications with a few lines of code. GUITk makes it easy to layout your GUI elements and respond to events using a declarative syntax. Because GUITk is built on top of tkinter, you can access the underlying tkinter API if you need to but for many use cases, you can build your GUI without needing to know much about tkinter.

GUITk apps are built by subclasses the `guitk.Window` class. Your GUI elements are layed out using a `guitk.HLayout` (horizontal layout) or `guitk.VLayout` (vertical layout) object which takes care of placing all widgets in the window using a declarative syntax. This is much simpler than using the underlying tkinter [grid manager](https://tkdocs.com/shipman/grid.html) or [pack](https://dafarry.github.io/tkinterbook/pack.htm) geometry managers.

GUITk is in alpha stage but is in constant development so check back frequently if this interests you or open an issue to start a conversation about what pain points this project could help you solve!

For full documentation visit [GUITk](https://rhettbull.github.io/guitk/).

## Installation

`pip install guitk`

## Source Code

[GUITk on GitHub](https://github.com/RhetTbull/guitk)

## License

MIT License

Copyright (c) 2020 Rhet Turnbull, All rights reserved.
