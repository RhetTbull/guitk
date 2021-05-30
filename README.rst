guitk: GUI Toolkit for TKinter
==============================

What is guitk?
------------------

guitk is yet another toolkit for building graphical user interfaces (GUIs) with TKinter. 

Examples
--------

.. code-block::
    
    import guitk

    # subclass guitk.Window as the starting point for your app's main window
    class HelloWindow(guitk.Window):
        # define a layout for the window
        # you must have a class variable named `layout` or you'll get an empty window
        layout = [
            [guitk.Label("What's your name?")],
            [guitk.Entry(key="name")],
            [guitk.Button("Ok")],
        ]

        # define your event loop
        # every guitk.Window will call self.handle_event to handle GUI events
        # event is a guitk.Event object
        def handle_event(self, event):
            print(f"Hello {self['name'].value}")


    # run your event loop
    HelloWindow("Window Title").run()

License
-------
Published under the MIT License.

