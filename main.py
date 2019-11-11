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
from kivy.uix.popup import Popup


class Star(Widget):
    '''
        This is the Star class which inherits from Widget. Planets and Moons are subclasses of the Star class.
    '''
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
                self.clear_selected()
            else:
                self.selected = True
                self.selected_draw()


class Planet(Star):
    '''
        Same as star class except they are blue.
    '''

    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 1)
            self.tracer = Line()


class Moon(Star):
    '''
        Same as the star class except they are grey.
    '''

    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        with self.canvas.before:
            Color(192, 192, 192)
            self.tracer = Line()


class StarSystemGame(Scatter):
    '''
        This is the StarSystemGame class. It inherits from the Scatter widget, so that it can be translated, rotated, and
        scaled. Everything is drawn onto the StarSystemGame canvas, except for the GUI. The StarSystemGame Scatter is placed
        onto the Screen behind the GUI.
        The physics of the objects is also updated in this class.
        This class also gives most of the GUI buttons their functionality.

        There is a lot of messy code in here, especially with the create/add tool. I'm aware it can be cleaned up, and
        most of it is repetitive. I gave myself a time crunch so please overlook it.

    '''
    create = ObjectProperty(None)
    scroll = BooleanProperty(False)
    selected = BooleanProperty(False)
    auto_bring_to_front = False
    do_collide_after_children = True
    button_add = ObjectProperty(None)
    run = BooleanProperty(True)
    timestep = NumericProperty(1)
    clear = BooleanProperty(True)
    moonB = BooleanProperty(False)
    planetB = BooleanProperty(False)
    starB = BooleanProperty(False)


    def __init__(self, *args, **kwargs):
        super(StarSystemGame, self).__init__(*args, **kwargs)
        self.dt = 1
        self.scale = 1
        self.listofObjects = []
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def clear_canvas(self):
        '''
            Clears all objects from the canvas. When the Game is updating the physics the only objects in self.children
            should be Stars, Planets, or Moons. This makes sure that the GridLayout (info card) is removed before it
            starts updating again.
        '''
        self.canvas.clear()
        for i in self.children:
            if isinstance(i, GridLayout):
                i.canvas.clear()
            else:
                i.canvas.clear()
                i.clear_tracer()
            self.remove_widget(i)

    def create_object(self, object):
        '''
            Takes in a string, and adds functionality to the add button in the GUI. It makes sures to update the respective
            boolean property. The self.clear boolean check is to make sure errors don't occur from a user pressing a button,
            and then pressing another button right after.
        '''
        if self.clear:
            self.create = True
            if object == "star":
                self.starB = True
            if object == 'moon':
                self.moonB = True
            if object == 'planet':
                self.planetB = True

    def remove_star(self):
        '''
            Removes the object that is selected. (not just stars, can be planet or moon)
        '''
        if self.clear:
            for i in self.children:
                if i.selected:
                    self.remove_widget(i)
                    self.remove_star()

    def toggle_pause(self):
        '''
            Toggles wheather the physics gets updated or not.
        '''
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

    def solar_system_starting_conditions(self):
        '''
            Simple solar system that doesn't include Uranus or Neptune, because the scatter isn't large enough. I will
            make a custome scatter size later to accomadate the size of this.
        '''
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

        jupiter.center = (4800, 10000)
        jupiter.pos = (4800, 10000)
        jupiter.mass = 32
        jupiter.momentum = Vector(60, 0).rotate(90)

        self.add_widget(star0)
        self.add_widget(mercury)
        self.add_widget(venus)
        self.add_widget(earth)
        self.add_widget(mars)
        self.add_widget(jupiter)

    def trinary_star_starting_conditions(self):
        star0 = Star()
        star0.center = 9800, 10000
        star0.mass = 1000
        star0.momentum = Vector(0, 750)

        star1 = Star()
        star1.center = (10200, 10000)
        star1.mass = 1000
        star1.momentum = Vector(0, -750)

        star2 = Star()
        star2.center = 10000, 8000
        star2.mass = 100
        star2.momentum = Vector(150, 0)

        self.add_widget(star0)
        self.add_widget(star1)
        self.add_widget(star2)

    def jupiters_moons_starting_conditions(self):
        jupiter = Planet()
        jupiter.center = 10000, 10000
        jupiter.pos = 10000, 10000
        jupiter.mass = 11
        jupiter.momentum = Vector(0, 0)

        io = Moon()
        io.pos = 9720, 10000
        io.center = 9720, 10000
        io.mass = 0.015
        io.momentum = Vector(0, 0.004)

        europa = Moon()
        europa.center = (10448, 10000)
        europa.mass = 0.008
        europa.momentum = Vector(0, -0.0019)

        ganymede = Moon()
        ganymede.center = (10000, 10715)
        ganymede.mass = 0.025
        ganymede.momentum = Vector(0.0043, 0)

        callisto = Moon()
        callisto.center = (10200, 8744)
        callisto.mass = 0.018
        callisto.momentum = Vector(-0.003, 0)

        self.add_widget(jupiter)
        self.add_widget(io)
        self.add_widget(europa)
        self.add_widget(ganymede)
        self.add_widget(callisto)

    def update(self, dt):
        '''
                Handles collision detection and updates the physics of the stars, planets, and moons. Also updates the
                drawing for selected items.
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
                                dist = 0.01
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
        '''
            Takes in the users touch and determines what should be done with it. If it is not on an object it will move
            the scatter object around.
            If create is true, then it will create an outline of where the object will be placed.
            It also calls the make info card method, to prompt the user for the stats of the object they wish to create.
        :param touch:
        '''
        super().on_touch_down(touch)
        # Changes coordinates to proper ones

        touch.apply_transform_2d(self.to_local)
        if self.create:
            if self.starB:
                self.run = False
                with self.canvas:
                    Color(1, 1, 1)
                    self.outline = Line(circle=(touch.x, touch.y, 12.5, 0, 360,),center=touch)
                self.info_card = self.make_info_card(touch)
                self.add_widget(self.info_card)
                self.create = False
            if self.planetB:
                self.run = False
                with self.canvas:
                    Color(1, 1, 1)
                    self.outline = Line(circle=(touch.x, touch.y, 5, 0, 360,), center=touch)
                self.info_card = self.make_info_card(touch)
                self.add_widget(self.info_card)
                self.create = False
            if self.moonB:
                self.run = False
                with self.canvas:
                    Color(1, 1, 1)
                    self.outline = Line(circle=(touch.x, touch.y, 1, 0, 360,), center=touch)
                self.info_card = self.make_info_card(touch)
                self.add_widget(self.info_card)
                self.create = False

    def on_touch_move(self, touch):

        super().on_touch_move(touch)
        touch.apply_transform_2d(self.to_local)

    def on_touch_up(self, touch):

        super().on_touch_up(touch)
        touch.apply_transform_2d(self.to_local)

    def make_info_card(self, touch):
        '''
            Takes in touch location from the user to add the info card to that place. Creates a layout with a label,
            TextInputs, and a Button to prompt the user for the stats of the object they wish to create.
            It adds the layout to the Scatter, but makes sure the game is paused. Once the user selects done. It applies
            the stats to the widget, and calls the kill_info_card method to remove the layout from the children of the
            game. This ensures that it doesn't get updated in the physics and cause an error.
        :param touch:
        '''
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
        if self.starB:
            self.star = Star(pos=touch.pos)
            self.star.center = touch.pos
        if self.moonB:
            self.moon = Moon(pos=touch.pos)
            self.moon_center = touch.pos
        if self.planetB:
            self.planet = Planet(pos=touch.pos)
            self.planet_center = touch.pos
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
                    if self.starB:
                        self.star.mass = 10
                    if self.planetB:
                        self.planet.mass = 1
                    if self.moonB:
                        self.moon.mas = 0.1
                else:
                    if self.starB:
                        self.star.mass = int(i.children[6].text)
                    if self.planetB:
                        self.planet.mass = int(i.children[6].text)
                    if self.moonB:
                        self.moon.mass = int(i.children[6].text)
                if i.children[4].text == '':
                    if self.starB:
                        self.star.momentum_x = 0
                    if self.planetB:
                        self.planet.momentum_x = 0
                    if self.moonB:
                        self.moon.momentum_x = 0
                else:
                    if self.starB:
                        self.star.momentum_x = int(i.children[4].text)
                    if self.planetB:
                        self.planet.momentum_x = int(i.children[4].text)
                    if self.moonB:
                        self.moon.momentum_x = int(i.children[4].text)
                if i.children[2].text == '':
                    if self.starB:
                        self.star.momentum_y = 0
                    if self.planetB:
                        self.planet.momentum_y = 0
                    if self.moonB:
                        self.moon.momentum_y = 0
                else:
                    if self.starB:
                        self.star.momentum_y = int(i.children[2].text)
                    if self.planetB:
                        self.planet.momentum_y = int(i.children[2].text)
                    if self.moonB:
                        self.moon.momentum_y = int(i.children[2].text)


                with self.canvas:
                    self.canvas.remove(self.outline)
                if self.starB:
                    self.add_widget(self.star)
                if self.planetB:
                    self.add_widget(self.planet)
                if self.moonB:
                    self.add_widget(self.moon)
                self.create = False
                self.remove_widget(i)
                self.do_rotation = True
        self.clear = True
        self.starB = False
        self.moonB = False
        self.planetB = False
        self.toggle_pause()

    def end_game(self):
        '''
            Clears the game and resets the scatter widget that the game is built on.
        '''
        del self.children[:]
        with self.canvas:
            self.canvas.clear()
        self.rotation = 0
        self.scale = 1
        self.center = self.parent.center


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
            popup = Popup(title='Notice',
                          content=Label(text='Must enter a number between 1-1000', font_size= self.parent.height / 8),
                          size_hint=(None, None), size=(200, 100))
            popup.open()



'''
    ScreenManager deals with which screen is displayed. All the other screens are below it. The GUI's are built onto the
    screen so to keep them separate from the children in the StarSystemGame class. Their code is done in the kivy language,
    because I wanted to learn it, and it seemed easier at the time. In the future I would like to build all the GUI's
    in python code in these classes.
'''


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
    '''
        Builds the game.
    '''
    def build(self):
        return Manager(transition=NoTransition())


if __name__ == '__main__':
    StarSystemApp().run()