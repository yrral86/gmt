#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gobject
import gtk
import gst
from datetime import datetime
from datetime import timedelta
import sys

class GMT:
    def ding(self):
        player = gst.Pipeline("player")
        source = gst.element_factory_make("filesrc", "file-source")
        decoder = gst.element_factory_make("mad", "mp3-decoder")
        conv = gst.element_factory_make("audioconvert", "converter")
        sink = gst.element_factory_make("autoaudiosink", "audio-output")
        player.add(source, decoder, conv, sink)
        gst.element_link_many(source, decoder, conv, sink)

        player.get_by_name("file-source").set_property('location', "bell.mp3")
        player.set_state(gst.STATE_PLAYING)


    def update(self):
        if not self.running:
            return False
        now = datetime.now()
        diff = now - self.start
        if timedelta(minutes=self.duration) >= diff:
            sec = (timedelta(minutes=self.duration) - diff).seconds
            self.set_time_string(sec)
            return True
        else:
            self.toggle_timer(self.button)
            self.ding()
            return False

    def toggle_timer(self, widget, data=None):
        if self.running:
            self.running = False
            self.button.set_label("Start")
            self.set_time_string(self.duration*60)
        else:
            self.running = True
            self.start = datetime.now()
            gobject.timeout_add(self.seconds/2, self.update)
            self.button.set_label("Stop")

    def __init__(self, duration):
        self.seconds = 1000
        self.minutes = 60*self.seconds
        self.duration = duration
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.vbox = gtk.VBox(True, 12)
        self.window.add(self.vbox)


        self.label = gtk.Label("GNOME Meditation Timer")
        self.vbox.pack_start(self.label)

        self.time_label = gtk.Label("")
        self.vbox.pack_start(self.time_label)
        self.set_time_string(self.duration*60)

        self.button = gtk.Button("Start")
        self.vbox.pack_start(self.button)
        self.running = False

        self.button.connect("clicked", self.toggle_timer, None)
        
        self.window.connect("destroy", gtk.main_quit)

        self.window.show_all()
    
    def main(self):
        gtk.main()

    def set_time_string(self, time):
        self.time_label.set_text("%d:%.2d" % (time/60, time%60))

if len(sys.argv) == 2:
    gmt = GMT(float(sys.argv[1]))
else:
    gmt = GMT(15)
gmt.main()
