from __future__ import print_function
from math import sin, cos, radians
from collections import defaultdict

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Line, Ellipse, Color
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory


class Peer(FloatLayout):
    animation = None
    name = StringProperty("Peer")
    image_radius = NumericProperty(50)

    def __init__(self, image_radius, **kwargs):
        super(Peer, self).__init__(**kwargs)
        self.image_radius = image_radius

    

class PyDelMainScreen(Widget):
    
    image_radius = NumericProperty(50)
    rad = NumericProperty(50)
    rad_opac = NumericProperty(1.0)

    disp_count = 0

    peers = {}
    outside_peers = None
  

    def __init__(self, **kwargs):
        super(PyDelMainScreen, self).__init__(**kwargs)


    def update_radar(self, dt):
        max_rad = max(self.width / 2.0,  (self.height - (self.height / 10.0)))
        self.rad += 2
        self.rad_opac = 1.0 - (self.rad / max_rad)
        
        if self.rad > max_rad:
            self.rad = self.image_radius


    def update_peers(self, dt):
        self.disp_count += 1

        def diff(list1, list2):
            c = set(list1).union(set(list2))
            d = set(list1).intersection(set(list2))
            return list(c - d)

        diff_peers = diff(self.peers.keys(), self.outside_peers.keys())
        for delta_peer in diff_peers:
            if delta_peer in self.outside_peers.keys():
                with self.fl.canvas:
                    newpeer = Peer(image_radius=self.image_radius)
                    newpeer.name = delta_peer
                    self.peers[delta_peer] = newpeer  # Add a new peer

            elif delta_peer in self.peers.keys():
                self.fl.canvas.clear()
                del self.peers[delta_peer]  # Peer no longer exists

        self.peer_layout()  # Set peer locations
                

    def peer_layout(self):
        num_peers = len(self.outside_peers.keys())
       
        def close_enough(posA, posB, percent_threshold=0.02):
            """
            Tell whether two positions are "close enough" to each other.
            It goes through each coordinate, and Falsafies the statement
            if one is too far away.
            """
            close = True
            for coordA, coordB in zip(posA, posB):
                if not coordA * (1 - percent_threshold) < coordB < coordA * (1 + percent_threshold):
                    close = False
            return close


        if num_peers > 0:
            radar_rad = min(self.width, self.height) / 2.0
            radar_rad -= 50  # border buffer
            semi_circ_segment = 180.0 / (num_peers + 1)

            count = 0
            for name in self.peers.keys():
                count += 1
                peer = self.peers[name]

                xpos = radar_rad * cos(radians(semi_circ_segment * count))
                ypos = radar_rad * sin(radians(semi_circ_segment * count))

                pos = (int(self.center_x + xpos - self.image_radius), 
                       int((self.height / 10.0) + ypos))

                peer.source = "images/peer.png"
                peer.size = (self.image_radius * 2, self.image_radius * 2)
                
                need_animation = False
                if not close_enough(pos, peer.pos):
                    if peer.animation:
                        if not peer.animation.have_properties_to_animate(peer):
                            # Extra if statement to avoid None object error
                            need_animation = True
                    else:
                        need_animation = True

                    if need_animation:
                        peer.animation = Animation(pos = pos, duration = 0.5, t='in_out_circ')
                        peer.animation.start(peer)


    def set_peers(self, peers):
        self.outside_peers = peers

class PyDelApp(App):
    
    peers = None

    def build(self):
        mainscreen = PyDelMainScreen()
        mainscreen.set_peers(self.peers)
        Clock.schedule_interval(mainscreen.update_radar, 1.0/60.0)
        Clock.schedule_interval(mainscreen.update_peers, 0.25)
        return mainscreen

    def set_peers(self, peers):
        self.peers = peers


