from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class Star(Widget):
    mass = NumericProperty(20)
    momentum_x = NumericProperty(0)
    momentum_y = NumericProperty(0)
    momentum = ReferenceListProperty(momentum_x, momentum_y)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        '''
            Initializes the stars tracer
        '''
        super(Star, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 1, 1)
            self.tracer = Line()

    def add_tracer(self):
        '''
            Adds a list of points. (Line()) that traces the stars position. Deletes after a certain amount of points)
        '''
        self.tracer.points += self.center
        if len(self.tracer.points) > 2500:
            del self.tracer.points[0]
            del self.tracer.points[0]

    def selected_draw(self):
        '''
            Draws a red ring around the selected object.
        '''
        if self.selected:
            with self.canvas:
                Color(1, 0, 0)
                self.outline = Line(circle=(self.center_x, self.center_y, self.width * 1.1, 0, 360,), center=self.center)

    def clear_selected(self):
        '''
            Removes red ring from selected object.
        '''
        with self.canvas:
            self.canvas.remove(self.outline)

    def clear_tracer(self):
        '''
            Removes tracer from object.
        '''
        del self.tracer.points[:]

    def on_touch_down(self, touch):
        '''
            On Touch_down method for object. Determines if object is selected or not and calls the corresponding
            draw/clear methods.
        '''
        if self.collide_point(*touch.pos):
            if self.selected:
                self.selected = False
                print('unselected')
                self.clear_selected()
            else:
                self.selected = True
                self.selected_draw()


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


class StarSystemGame(Scatter):
    createstar = ObjectProperty(None)
    scroll = BooleanProperty(False)
    selected = BooleanProperty(False)
    auto_bring_to_front = False
    do_collide_after_children = True
    button_add = ObjectProperty(None)
    run = BooleanProperty(True)
    timestep = NumericProperty(1)
    clear = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super(StarSystemGame, self).__init__(*args, **kwargs)
        self.dt = 1
        self.scale = 1
        self.listofObjects = []
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def clear_canvas(self):
        self.canvas.clear()
        for i in self.children:
            if isinstance(i, GridLayout):
                i.canvas.clear()
            else:
                i.canvas.clear()
                i.clear_tracer()
            self.remove_widget(i)

    def create_star(self):
        if self.clear:
            self.createstar = True

    def remove_star(self):
        if self.clear:
            for i in self.children:
                if i.selected:
                    self.remove_widget(i)
                    self.remove_star()


    def toggle_pause(self):
        if self.clear:
            if self.run:
                self.run = False
            else:
                self.run = True

    def earth_moon_sun_starting_conditions(self):
        star0 = Star()
        earth = Planet()
        moon = Moon()
        star0.center = (10000, 10000)
        star0.mass = 10000
        star0.momentum = 0, 0
        self.add_widget(star0)

        earth.center = (9000, 10000)
        earth.pos = (9000, 10000)
        moon.center = (8990, 10000)
        moon.pos = (8990, 10000)
        earth.mass = 1
        moon.mass = 0.1

        earth.momentum = Vector(4.5, 0).rotate(90)
        moon.momentum = Vector(0.4, 0).rotate(90)
        self.add_widget(moon)
        self.add_widget(earth)

    def binary_star_starting_conditions(self):
        star0 = Star()
        star0.center = 9800, 10000
        star0.mass = 1000
        star0.momentum = Vector(0, 750)
        self.add_widget(star0)
        star1 = Star()
        star1.center = (10200, 10000)
        star1.mass = 1000
        star1.momentum = Vector(0, -750)
        self.add_widget(star1)

    # TODO
    def solar_system_starting_conditions(self):
        star0 = Star()
        mercury = Planet()
        venus = Planet()
        earth = Planet()
        mars = Planet()
        jupiter = Planet()
        saturn = Planet()
        uranus = Planet()
        neptune = Planet()

        star0.center = (10000, 10000)
        star0.mass = 10000
        star0.momentum = 0, 0

        mercury.center = (9700, 10000)
        mercury.pos = (9700, 10000)
        mercury.mass = 0.05
        mercury.momentum = Vector(0.425, 0).rotate(90)

        venus.center = (9300, 10000)
        venus.pos = (9300, 10000)
        venus.mass = 0.95
        venus.momentum = Vector(5, 0).rotate(90)

        earth.center = (9000, 10000)
        earth.pos = (9000, 10000)
        earth.mass = 1
        earth.momentum = Vector(4.5, 0).rotate(90)

        mars.center = (8500, 10000)
        mars.pos = (8500, 10000)
        mars.mass = 0.1
        mars.momentum = Vector(0.385, 0).rotate(90)



        self.add_widget(star0)
        self.add_widget(mercury)
        self.add_widget(venus)
        self.add_widget(earth)
        self.add_widget(mars)

    # TODO
    def trinary_star_starting_conditions(self):
        pass

    # TODO
    def saturns_moons_starting_conditions(self):
        pass

    def update(self, dt):
        '''
                Handles collision detection and updates the physics of the stars
        '''
        if self.run:
            for i in self.children:
                if i.selected:
                    i.clear_selected()
                    i.selected_draw()
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
        if not self.collide_point(*touch.pos):
            print("Out of bounds")
        touch.apply_transform_2d(self.to_local)
        if self.createstar:
            self.run = False
            with self.canvas:
                Color(1, 1, 1)
                self.outline = Line(circle=(touch.x, touch.y, 12.5, 0, 360,),center=touch)
            self.info_card = self.make_info_card(touch)
            self.add_widget(self.info_card)
            self.createstar = False

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        touch.apply_transform_2d(self.to_local)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        touch.apply_transform_2d(self.to_local)

    def make_info_card(self, touch):
        self.rotation = 0
        self.clear = False
        layout = GridLayout(cols=2, row_force_default=True, row_default_height=self.parent.height / 22, center=(touch.x + 50, touch.y + 50))
        layout.add_widget(Label(text='Mass:'))
        mass_input = TextInputFiltered(input_filter='float', text='1', multiline=False, focus=False, write_tab=False, font_size=self.parent.height / 50)
        layout.add_widget(mass_input)
        layout.add_widget(Label(text='Vel x:'))
        layout.add_widget(TextInput(input_filter='float',text='1', multiline=False, focus=False, write_tab=False, font_size=self.parent.height / 50))
        layout.add_widget(Label(text='Vel y:'))
        layout.add_widget(TextInput(input_filter='float',text='1', multiline=False, focus=False, write_tab=False, font_size=self.parent.height / 50))
        layout.add_widget(Label())
        done = Button(text='Done')
        done.bind(on_press=self.kill_info_card)
        layout.add_widget(done)
        self.do_rotation = False
        self.star = Star(pos=touch.pos)
        self.star.center = touch.pos
        return layout

    def kill_info_card(self, *args):
        '''
            Finds info card, checks to make sure info card is filled out. Finishes updating appropriate star.
        :param args:
        :return:
        '''
        for i in self.children:
            if isinstance(i, GridLayout):
                if i.children[6].text == '':
                    self.star.mass = 1
                else:
                    self.star.mass = int(i.children[6].text)
                if i.children[4].text == '':
                    self.star.momentum_x = 0
                else:
                    self.star.momentum_x = int(i.children[4].text)
                if i.children[2].text == '':
                    self.star.momentum_y = 0
                else:
                    self.star.momentum_y = int(i.children[2].text)

                with self.canvas:
                    self.canvas.remove(self.outline)
                self.add_widget(self.star)
                self.createstar = False
                self.remove_widget(i)
                self.do_rotation = True
        self.clear = True
        self.toggle_pause()

    def end_game(self):
        del self.children[:]
        with self.canvas:
            self.canvas.clear()


class TextInputFiltered(TextInput):
    '''
        This is just for the star mass since mass can't be equal to 0.
    '''
    def insert_text(self, string, from_undo=False):
        new_text = self.text + string
        try:
            num = float(new_text)
            if new_text != "":
                if 1 <= float(new_text) <= 1000:
                    TextInput.insert_text(self, string, from_undo=from_undo)
        except ValueError:
            print('Not a number')



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