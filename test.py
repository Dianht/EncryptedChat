#!/usr/bin/env python3
# coding: utf-8
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

def on_button_clicked(btn,entry,bf):
        text = entry.get_text() + '\n'
        entry.set_text("")
        bf.insert_markup(bf.get_end_iter(),text,-1)

builder = Gtk.Builder()
builder.add_from_file('glade/client_interface.glade')  # Rentrez évidemment votre fichier, pas le miens!

window = builder.get_object('client_window')
textview = builder.get_object('textView')
btnsend = builder.get_object('btnSend')
entry = builder.get_object('entry')

buffertexte = textview.get_buffer()


entry.connect('activate',on_button_clicked,entry,buffertexte)
btnsend.connect('clicked',on_button_clicked,entry,buffertexte)

# Peut se faire dans Glade mais je préfère le faire ici, à vous de voir
window.connect('delete-event', Gtk.main_quit)

# Le handler

window.show_all()
Gtk.main()
print("salut")