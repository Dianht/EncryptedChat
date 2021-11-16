#!/usr/bin/env python3
# coding: utf-8
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

class User:
        def __init__(self):
                self.nickname = "Anonyme"
                self.notMyKey = [0,1]
                self.myKey = [0,1]
                self.message = ""
                self.entryEmpty = False
                builder = Gtk.Builder()
                builder.add_from_file('glade/client_interface.glade')  # Rentrez évidemment votre fichier, pas le miens!

                window = builder.get_object('client_window')
                self.textview = builder.get_object('textView')
                self.btnsend = builder.get_object('btnSend')
                self.entry = builder.get_object('entry')
                self.e_entry = builder.get_object('e_entry')
                self.n_entry = builder.get_object('n_entry')
                
                self.cle_publique = builder.get_object('cle_publique')
                self.cle_privee = builder.get_object('cle_privee')

                self.bf = self.textview.get_buffer()

                self.e_entry.connect('activate',self.onActivateE)
                self.n_entry.connect('activate',self.onActivateN)
                self.entry.connect('activate',self.onBtnN)
                self.btnsend.connect('clicked',self.onBtnN)

                # Peut se faire dans Glade mais je préfère le faire ici, à vous de voir
                window.connect('delete-event', Gtk.main_quit)
                window.show_all()


        def onBtnN(self,e):
                text = self.entry.get_text()
                if self.nickname == "Anonyme":
                        self.nickname = text
                        print(self.nickname)
                else : 
                        self.entryEmpty = True
                        self.message = text 
                        self.entry.set_text("")

        def onActivateE(self,e):
                text = self.e_entry.get_text()
                self.notMyKey[0] = int(text)

        def onActivateN(self,e):
                text = self.n_entry.get_text()
                self.notMyKey[1] = int(text)
        
        def enterText(self,text):
                self.bf.insert_markup(self.bf.get_end_iter(),text + '\n',-1)
                self.textview.set_buffer(self.bf)

        def completed(self):
                if((self.nickname != "Anonyme") and (self.notMyKey != [])):
                        return True;
                return False;
        
        def setUserKey(self,key):
                self.myKey = key
                self.cle_publique.set_text(str(key[0]))
                self.cle_privee.set_text(str(key[1]))
        
        
        def main(self):
                Gtk.main()
                return 0





