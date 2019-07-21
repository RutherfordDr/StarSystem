import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import DragBehavior
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from random import randint
from kivy.properties import ListProperty
from vpython import *


class Star(DragBehavior, Widget):
    '''
        Have to implement Properties at class level. Not sure why I can't do this in the __init__ method?
    '''
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    mass = NumericProperty(0)
    momentum_x = NumericProperty(0)
    momentum_y = NumericProperty(0)
    momentum = ReferenceListProperty(momentum_x, momentum_y)
    selected = BooleanProperty(False)


    '''
        Initializes the stars tracer
    '''
    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 1)
            self.tracer = Line()

    '''
        Adds a list of points (Line()) that traces the stars position. Deletes after a certain amount of points
    '''
    def add_tracer(self):
        self.tracer.points += self.center
        if len(self.tracer.points) > 2500:
            del self.tracer.points[0]
            del self.tracer.points[0]

    def set_star_mass(self, mass):
        self.mass = mass


class StarSystemGame(Scatter):
    star0 = ObjectProperty(None)
    star1 = ObjectProperty(None)
    starList = ReferenceListProperty(star0, star1)
    scroll = BooleanProperty(False)
    selected = BooleanProperty(False)
    do_collide_after_children = False
    auto_bring_to_front = True



    '''
        Edit the stars starting velocity, mass, etc.
    '''
    def starting_conditions(self):
        self.star0.center = self.center
        self.star1.momentum = Vector(3, 0).rotate(90)
        self.star1.center = self.center
        self.star0.momentum = Vector(3, 0).rotate(-90)
        self.star0.set_star_mass(20)
        self.star1.set_star_mass(20)


    '''
        Handles collision detection and updates the physics of the stars
    '''
    def update(self, dt):

        # Collision detection
        for i in self.starList:
            for j in self.starList:
                if i.collide_widget(j):
                    if i != j:
                        print('Supernova')

        # Physics of the stars
        dt = 1
        dist = Vector(*self.star0.pos) - Vector(*self.star1.pos)
        '''
            Makes sure there is no division by 0
        '''
        if dist.length2() == 0:
            print('Full Supernova')
        else:
            force = self.star0.mass * self.star1.mass * dist.normalize() / dist.length2()

            ## leapfrog method
            self.star0.momentum = Vector(*self.star0.momentum) - Vector(*force) * dt
            self.star0.velocity = Vector(*self.star0.velocity) - Vector(*force) * dt / self.star0.mass
            self.star1.momentum = Vector(*self.star1.momentum) + Vector(*force) * dt
            self.star1.velocity = Vector(*self.star1.velocity) - Vector(*force) * dt / self.star1.mass

            # Adds momentum to position (update pos)
            for i in self.starList:
                i.pos = Vector(*i.pos) + Vector(*i.momentum) / i.mass * dt
                i.add_tracer()


class StarSystemApp(App):
    def build(self):
        game = StarSystemGame()
        game.starting_conditions()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    StarSystemApp().run()