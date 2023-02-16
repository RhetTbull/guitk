# """_Layout mixin"""

# from guitk.tooltips import Hovertip

# from .widgets import *


# class _Layout:
#     """Mixin class to provide layout"""

#     layout = []

#     def __init__(self, *args, **kwargs):
#         pass

#     def _layout(self, parent, window: "_WindowBaseClass", autoframe):
#         # as this is a mixin, make sure class being mixed into has necessary attributes

#         row_offset = 0
#         for row_count, row in enumerate(self.layout):
#             col_offset = 0
#             if autoframe and len(row) > 1:
#                 row_ = [Frame(layout=[row], autoframe=False)]
#             else:
#                 row_ = row
#             for col_count, widget in enumerate(row_):
#                 if widget is None:
#                     # add blank label to maintain column spacing
#                     widget = Label("", disabled=True, events=False)

#                 widget.key = (
#                     widget.key or f"{widget.widget_type},{row_count},{col_count}"
#                 )
#                 widget._create_widget(
#                     parent, window, row_count + row_offset, col_count + col_offset
#                 )
#                 tooltip = widget.tooltip or window.tooltip
#                 if tooltip:
#                     _tooltip = tooltip(widget.key) if callable(tooltip) else tooltip
#                     widget._tooltip = (
#                         Hovertip(widget.widget, _tooltip) if _tooltip else None
#                     )
#                 else:
#                     widget._tooltip = None

#                 window._widgets.append(widget)
#                 widget.parent = self
#                 window._widget_by_key[widget.key] = widget
#                 if widget.rowspan and widget.rowspan > 1:
#                     row_offset += widget.rowspan - 1
#                 if widget.columnspan and widget.columnspan > 1:
#                     col_offset += widget.columnspan - 1

