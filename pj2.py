#!/usr/bin/env python3

"""PJ - Python VJ"""

#import gobject
#gobject.threads_init()
# import gst
import pygtk
pygtk.require("2.0")
import gtk
import math
# gtk.gdk.threads_init()
# import sys
#import os

# class PJException(Exception):
#     """Base exception class for errors which occur during demos"""

#     def __init__(self, reason):
#         self.reason = reason

__clips__ = 20

class PJ(object):
    """PJ main class"""

    __name__ = "PJ - PeeJay Video Mixer"
    __usage__ = "python pj.py -- starts the PJ"
    __def_win_size__ = (960, 540)

    __spacing__ = 5

    def destroy(self, widget, data=None):
        gtk.main_quit()
        return False

    def createWindow(self):
        """Creates a top-level window"""

        # create window, set basic attributes
        self.app = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.app.set_size_request(*self.__def_win_size__)
        #app.set_size_request(*self.__def_win_size__)
        #app.set_decorated(False)
        #self.app.fullscreen()
        #w.unfullscreen()
        self.app.set_title(self.__name__)

        self.app.connect("destroy", self.destroy)
        self.app.connect("delete_event", self.destroy)
        #app.connect("destroy", self.destroy)
        #self.app.set_border_width(100)

        box = gtk.HBox(False)
        self.app.add(box)

        grid_size = int(math.ceil(math.sqrt(__clips__)))
        #print(grid_size)

        table = gtk.Table(grid_size, grid_size, False)
        table.set_border_width(self.__spacing__ / 2)
        box.pack_start(table)

        # add clip grid
        for y in xrange(0, grid_size):
            for x in xrange(0, grid_size):
                if y * grid_size + x < __clips__:
                    clip = Clip(self)
                    table.attach(clip.get_widget(), x, x + 1, y, y + 1)

        mixboard = gtk.VBox(False, self.__spacing__)
        mixboard.set_border_width(self.__spacing__)
        box.pack_end(mixboard)

        channels = (
            gtk.DrawingArea(),
            gtk.DrawingArea(),
            gtk.DrawingArea(),
            gtk.DrawingArea(),
        )

        for channel in channels:
            channel.modify_bg(gtk.STATE_NORMAL, channel.style.black)
            channel.set_size_request(240, 135)
            mixboard.pack_start(channel)

        #preview = gtk.DrawingArea()
        #preview.modify_bg(gtk.STATE_NORMAL, preview.style.black)
        #mixboard.pack_end(preview)

        self.app.show_all()

    def createOutput(self):
        """Creates a output window"""

        # create window, set basic attributes
        self.output = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.app.set_size_request(*self.__def_win_size__)
        #app.set_size_request(*self.__def_win_size__)
        self.output.set_decorated(False)
        self.output.fullscreen()
        self.output.unfullscreen()
        self.output.fullscreen()
        #self.output.set_title(self.__name__)

        self.output.connect("destroy", self.destroy)
        self.output.connect("delete_event", self.destroy)
        #app.connect("destroy", self.destroy)
        #self.app.set_border_width(100)

        out = gtk.DrawingArea()
        out.modify_bg(gtk.STATE_NORMAL, out.style.black)

        self.output.add(out)

        self.output.show_all()

        # we want to return only the portion of the window which will
        # be used to display the video, not the whole top-level
        # window. a DrawingArea widget is, in fact, an X11 window.
        #return viewer

    def run(self):
        self.createWindow()
        self.createOutput()
        #.connect("destroy", self.destroy)
        #pipeline, sink = self.createPipeline(w)
        try:
        #    self.magic(pipeline, sink)
         #   self.pipeline.set_state(gst.STATE_PLAYING)
            gtk.main()
        except Exception, e:
            print e.reason
            print self.__usage__
            sys.exit(-1)

    def onOpen(self, unused_button):
        print("Opens")
        return False

    def onPlay(self, unused_button):
        print("Plays")
        #self.pipeline.set_state(gst.STATE_PLAYING)
        return False

    def onPause(self, unused_button):
        print("Pauses")
        #self.pipeline.set_state(gst.STATE_PLAYING)
        return False

    def onStop(self, unused_button):
        print("Stops")
        #self.pipeline.set_state(gst.STATE_READY)
        return False

class Clip(object):
    """Clip Preview"""

    def __init__(self, pj):
        self.frame = gtk.Frame(label=None)
        self.frame.set_border_width(pj.__spacing__ / 2)
        #self.frame.set_size_request(100, 100)
        layout = gtk.VBox(False, pj.__spacing__)
        layout.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        layout.set_border_width(pj.__spacing__)
        self.viewer = gtk.DrawingArea()
        self.viewer.modify_bg(gtk.STATE_NORMAL, self.viewer.style.black)
        self.viewer.set_size_request(240, 135)
        layout.pack_start(self.viewer)
        controls = (
            ("open_button", gtk.ToolButton(gtk.STOCK_FLOPPY), pj.onOpen),
            ("play_button", gtk.ToolButton(gtk.STOCK_MEDIA_PLAY), pj.onPlay),
            ("play_button", gtk.ToolButton(gtk.STOCK_MEDIA_PAUSE), pj.onPause),
            ("stop_button", gtk.ToolButton(gtk.STOCK_MEDIA_STOP), pj.onStop),
            ("stop_button", gtk.ToolButton(gtk.STOCK_CLOSE), pj.onStop),
        )
        box = gtk.HBox()
        #box.set_size_request(10, 100)
        #box.set_spacing(spacing)
        box.set_border_width(0)
        for name, widget, handler in controls:
            widget.set_can_focus(False)
            widget.connect("clicked", handler)
            #widget.set_size_request(32, 32)
            #print(widget.size_request())
            box.pack_start(widget, False)
            setattr(self, name, widget)
        adj2 = gtk.Adjustment(0.1, 0.0, 1.0, 0.0, 0.2, 0.0)
        #adj2.connect("value_changed", self.cb_digits_scale)
        scale = gtk.HScale(adj2)
        scale.set_value_pos(gtk.POS_LEFT)
        scale.set_digits(10)
        scale.set_draw_value(False)
        #scale.set_can_focus(False)
        layout.pack_start(scale)
        #progressbar = gtk.ProgressBar(adjustment=None)
        #layout.pack_start(progressbar)
        layout.pack_end(box)
        self.frame.add(layout)

    def get_widget(self):
        return self.frame

    def get_viewer(self):
        return self.viewer




# if this file is being run directly, create the demo and run it
if __name__ == '__main__':
    PJ().run()
