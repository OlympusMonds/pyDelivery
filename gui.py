from math import sin, cos, radians
from collections import defaultdict

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Line, Ellipse, Color
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory


class PyDelMainScreen(Widget):
    
    image_radius = NumericProperty(50)
    rad = NumericProperty(50)
    rad_opac = NumericProperty(1.0)

    disp_count = 0

    peers = defaultdict(dict)
    outside_peers = {"Kayla": {"icon" : "images/peer.png",},
                     #"Ed":    {"icon" : "images/peer.png",},
                     #"Nath":  {"icon" : "images/peer.png",},
                     #"Ben":   {"icon" : "images/peer.png",},
                    }
 # This is a stub
   
    def __init__(self, **kwargs):
        super(PyDelMainScreen, self).__init__(**kwargs)
        # Just in case


    def update_radar(self, dt):
        max_rad = max(self.width / 2.0,  (self.height - (self.height / 10.0)))
        self.rad += 1
        self.rad_opac = 1.0 - (self.rad / max_rad)
        
        if self.rad > max_rad:
            self.rad = self.image_radius


    def update_peers(self, dt):
        self.disp_count += 1

        if self.disp_count % 40 == 0:
            self.outside_peers["name%d" % self.disp_count] = {"icon": "images/peer.png"}


        for name, val in self.outside_peers.iteritems():
            if name in self.peers.keys():
                continue  # Already added to gui 
            else:
                with self.fl.canvas:
                    self.peers[name]["peer_obj"] = Factory.Peer()  # Add a new peer

        self.peer_layout()  # Set peer locations
                

    def peer_layout(self):
        num_peers = len(self.outside_peers.keys())
        
        radar_rad = min(self.width, self.height) / 2.0
        radar_rad -= 50  # border buffer
        semi_circ_segment = 180.0 / (num_peers + 1)

        count = 0
        for name in self.peers.keys():
            count += 1
            peer = self.peers[name]["peer_obj"]

            xpos = radar_rad * cos(radians(semi_circ_segment * count))
            ypos = radar_rad * sin(radians(semi_circ_segment * count))

            pos = (int(self.center_x + xpos - self.image_radius), 
                   int((self.height / 10.0) + ypos))

            peer.source = "images/peer.png"
            peer.size = (self.image_radius * 2, self.image_radius * 2)
            
            need_animation = False
            if pos != peer.pos:
                if "ani_obj" not in self.peers[name].keys():
                    need_animation = True
                    # This if should protect against Key_Error exception
                elif not self.peers[name]["ani_obj"].have_properties_to_animate(peer):
                    need_animation = True

                if need_animation:
                    self.peers[name]["ani_obj"] = Animation(pos = pos, duration = 0.5, t='in_out_circ')
                    self.peers[name]["ani_obj"].start(peer)



class PyDelApp(App):
    
    def build(self):
        mainscreen = PyDelMainScreen()
        Clock.schedule_interval(mainscreen.update_radar, 1.0/60.0)
        Clock.schedule_interval(mainscreen.update_peers, 0.25)
        return mainscreen

