
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior



class Star(Widget):
    '''
        Have to implement Properties at class level. Not sure why I can't do this in the __init__ method?
    '''
    mass = NumericProperty(20)
    momentum_x = NumericProperty(0)
    momentum_y = NumericProperty(0)
    momentum = ReferenceListProperty(momentum_x, momentum_y)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    selected = BooleanProperty(False)





    '''
        Initializes the stars tracer
    '''
    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 1, 1)
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

    def clear_tracer(self):
        del self.tracer.points[:]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selected = True
            print('True')
        else:
            self.selected = False



class StarSystemGame(DragBehavior, Scatter):
    star0 = ObjectProperty(None)
    star1 = ObjectProperty(None)
    createstar = ObjectProperty(None)
    starList = ReferenceListProperty(star0, star1)
    scroll = BooleanProperty(False)
    selected = BooleanProperty(False)
    auto_bring_to_front = False
    control = ObjectProperty(None)

    size_hint = (10000,10000)

    temp = ObjectProperty(None)


    def __init__(self, *args, **kwargs):
        super(StarSystemGame, self).__init__(*args, **kwargs)
        self.dt = 1
        self.scale = 1
        Clock.schedule_interval(self.update, 1.0 / 60.0)







    def adjust_time(self):
        pass

    def create_star(self):
        self.createstar = True

    def remove_star(self):
        for i in self.children:
            if i.selected:
                self.remove_widget(i)


    '''
        Edit the stars starting velocity, mass, etc.
    '''
    def starting_conditions(self):

        for i in self.children:
            i.clear_tracer()
        self.star0.center = self.center
        self.star1.momentum = Vector(1000, 0).rotate(90)
        self.star1.center = self.center
        self.star0.momentum = Vector(1000, 0).rotate(-90)
        self.star0.set_star_mass(1000)
        self.star1.set_star_mass(1000)
        self.star0.pos = (Window.width / 3, Window.height / 2)
        self.star1.pos = (Window.width * 2 / 3, Window.height / 2)



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
        # Physics for the stars, updates the children of the StarSystemApp widget
        if len(self.children) > 1:
            for i in self.children:
                for j in self.children:
                    if j != i:
                        dist = Vector(*i.pos) - Vector(*j.pos)
                        if dist.length2() == 0:
                            print('Full Supernova')
                        else:
                            force = i.mass * j.mass * dist.normalize() / dist.length2()
                            i.momentum = Vector(*i.momentum) - Vector(*force) * self.dt
                            j.momentum = Vector(*j.momentum) + Vector(*force) * self.dt
                            i.velocity = Vector(*i.momentum) / i.mass
                            j.velocity = Vector(*i.momentum) / j.mass
                i.pos = Vector(*i.pos) + Vector(*i.momentum) / i.mass * self.dt
                i.add_tracer()
        else:
            # This fixes the bug where if theres only 1 star left instead of stopping its momentum, it stays constant.
            for i in self.children:
                i.pos = Vector(*i.pos) + Vector(*i.momentum) / i.mass * self.dt
                i.add_tracer()

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        # Changes coordinates to proper ones
        touch.apply_transform_2d(self.to_local)
        if self.createstar:
            with self.canvas:
                self.temp = Line(circle=(touch.x, touch.y, 12.5, 0, 360))

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        touch.apply_transform_2d(self.to_local)
        if self.createstar:
            print('Yay')



    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        touch.apply_transform_2d(self.to_local)
        if touch.y < self.parent.height / 10:
            pass
        if self.createstar:
            with self.canvas:
                self.canvas.remove(self.temp)
                star = Star(pos=touch.pos)
                star.center = touch.pos
                star.mass = 100
                star.momentum_y = 100
                star.selected = True
                self.add_widget(star)
                self.createstar = False


class Manager(ScreenManager):
    pass


class MenuScreen(Screen):
    pass


class FreePlayScreen(Screen):
    pass

class StarSystemApp(App):
    def build(self):
        return Manager(transition=NoTransition())


if __name__ == '__main__':
    StarSystemApp().run()