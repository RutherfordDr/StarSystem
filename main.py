
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

from kivy.uix.spinner import Spinner


class Star(Widget):

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


    def clear_tracer(self):
        del self.tracer.points[:]


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selected = True
        else:
            self.selected = False


class Planet(Star):
    mass = NumericProperty(10)
    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 1)
            self.tracer = Line()


class Moon(Star):
    mass = NumericProperty(1)

    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        with self.canvas.before:
            Color(192, 192, 192)
            self.tracer = Line()


class StarSystemGame(DragBehavior, Scatter):
    createstar = ObjectProperty(None)
    scroll = BooleanProperty(False)
    selected = BooleanProperty(False)
    auto_bring_to_front = False
    do_collide_after_children = True
    button_add = ObjectProperty(None)
    run = BooleanProperty(True)
    size_hint = (100,100)


    timestep = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(StarSystemGame, self).__init__(*args, **kwargs)
        self.dt = 1
        self.scale = 1
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    # TODO
    def adjust_time(self):
        self.timestep *= 1.1

    def create_star(self):
        self.createstar = True

    def remove_star(self):
        for i in self.children:
            if i.selected:
                i.canvas.clear()
                i.clear_tracer()
                self.remove_widget(i)

    def toggle_pause(self):
        if self.run:
            self.run = False
        else:
            self.run = True



    def earth_moon_sun_starting_conditions(self):
        star0 = Star()
        star0.center = (5000, 5000)
        star0.mass = 1000
        star0.momentum = 0, 0
        star0.selected = True
        self.add_widget(star0)

        star0.center = self.center
        self.earth.center = self.center
        self.moon.center = self.center
        self.star0.set_star_mass(1000)
        self.earth.set_star_mass(10)
        self.moon.set_star_mass(0.1)
        self.star0.pos = (5000, 5000)
        self.earth.pos = (Window.width / 4, Window.height / 2)
        self.moon.pos = (Window.width / 4.5, Window.height / 2)
        self.earth.momentum = Vector(25, 0).rotate(90)
        self.moon.momentum = Vector(0.36, 0).rotate(90)

    # TODO
    def binary_star_starting_conditions(self):
        star0 = Star()
        star0.center = 4800, 5000
        star0.mass = 1000
        star0.momentum = Vector(0, 750)
        self.add_widget(star0)
        star1 = Star()
        #star1.size_hint = 0.5, 0.5
        star1.center = (5200, 5000)
        star1.mass = 1000
        star1.momentum = Vector(0, -750)
        self.add_widget(star1)

    # TODO
    def solar_system_starting_conditions(self):
        pass

    # TODO
    def trinary_star_starting_conditions(self):
        pass

    # TODO
    def saturns_moons_starting_conditions(self):
        pass

    '''
        Handles collision detection and updates the physics of the stars
    '''
    def update(self, dt):
        #for i in self.children:
        #    print(i.pos)
        if self.run:
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
                                i.momentum = Vector(*i.momentum) - Vector(*force) * self.dt * self.timestep
                                j.momentum = Vector(*j.momentum) + Vector(*force) * self.dt * self.timestep
                                i.velocity = Vector(*i.momentum) / i.mass * self.timestep
                                j.velocity = Vector(*i.momentum) / j.mass * self.timestep
                    i.pos = Vector(*i.pos) + Vector(*i.momentum) / i.mass * self.dt * self.timestep
                    i.add_tracer()
            else:
                # This fixes the bug where if theres only 1 star left instead of stopping its momentum, it stays constant.
                for i in self.children:
                    i.pos = Vector(*i.pos) + Vector(*i.momentum) / i.mass * self.dt * self.timestep
                    i.add_tracer()

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        # Changes coordinates to proper ones
        touch.apply_transform_2d(self.to_local)
        if self.createstar:
            self.starvel = 0
            print(self.starvel)
            with self.canvas:
                Color(1, 1, 1)
                self.outline = Line(circle=(touch.x, touch.y, 12.5, 0, 360))

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        touch.apply_transform_2d(self.to_local)
        if self.createstar:
            self.starvel += 0.25

            print(self.starvel)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        touch.apply_transform_2d(self.to_local)
        print(touch.pos)
        if self.createstar:
            with self.canvas:
                self.canvas.remove(self.outline)
            star = Star(pos=touch.pos)
            star.center = touch.pos
            star.mass = 100
            star.momentum_y = self.starvel
            self.add_widget(star)
            self.createstar = False





class Manager(ScreenManager):
    pass

class MenuScreen(Screen):
    pass

class FreePlayScreen(Screen):
    pass

class SimulationScreen(Screen):
    pass

class AboutScreen(Screen):
    pass





class StarSystemApp(App):
    def build(self):
        return Manager(transition=NoTransition())


if __name__ == '__main__':
    StarSystemApp().run()