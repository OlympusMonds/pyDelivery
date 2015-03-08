from __future__ import print_function
from math import sin, cos, radians
from collections import defaultdict

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Line, Ellipse, Color
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory



class Peer(ButtonBehavior, RelativeLayout):
    animation = None
    name = StringProperty("Peer")
    image_radius = NumericProperty(50)
    image_path = StringProperty("images/peer.png")

    def __init__(self, image_radius, **kwargs):
        super(Peer, self).__init__(**kwargs)
        self.image_radius = image_radius
        self.size = [100, 100]
        self.pos = [400, 400]
        print(self.size)
        print(self.pos)

    def clicked(self):
        print("Hello", self.size)
        print(self.pos)


class PyDelMainScreen(Widget):
    
    image_radius = NumericProperty(50)
    radar_radius = NumericProperty(50)
    radar_opacity = NumericProperty(1.0)

    radar_max_line_width = 10
    radar_min_line_width = 2
    radar_line_width = NumericProperty(radar_min_line_width)

    disp_count = 0

    peers = {}
    outside_peers = None
  

    def __init__(self, **kwargs):
        super(PyDelMainScreen, self).__init__(**kwargs)


    def update_radar(self, dt):
        max_rad = max(self.width / 2.0,  (self.height - (self.height / 10.0)))
        percent_complete = self.radar_radius / max_rad

        self.radar_radius += 2
        self.radar_opacity = 1.0 - percent_complete
        self.radar_line_width = (self.radar_max_line_width - self.radar_min_line_width) * percent_complete
        self.radar_line_width += self.radar_min_line_width
        
        if self.radar_radius > max_rad:
            self.radar_radius = self.image_radius


    def update_peers(self, dt):
        """
        Check to see if new peers have been found, and remove any
        who are no longer around.
        """
        self.disp_count += 1

        def diff(list1, list2):
            c = set(list1).union(set(list2))
            d = set(list1).intersection(set(list2))
            return list(c - d)

        need_position_update = False
        diff_peers = diff(self.peers.keys(), self.outside_peers.keys())
        for delta_peer in diff_peers:
            need_position_update = True
            if delta_peer in self.outside_peers.keys():
                newpeer = Peer(image_radius=self.image_radius)
                newpeer.name = delta_peer
                self.fl.add_widget(newpeer)
                self.peers[delta_peer] = newpeer  # Add a new peer

            elif delta_peer in self.peers.keys():
                self.fl.remove_widget(self.peers[delta_peer])
                del self.peers[delta_peer]  # Peer no longer exists

        if need_position_update:
            self.peer_layout()  # Set peer locations
                

    def peer_layout(self):
        """
        The actual layout of peers is done in here. This function is called by
        update_peers, and should only ever expect to have to display the peers
        in the self.peer dict (that means it shouldn't need to deal with deletions,
        and there should never be extra peers that don't need to be shown)
        """
        num_peers = len(self.peers.keys())
       
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


