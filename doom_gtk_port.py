#!/usr/bin/python3
"""
Doom Port with Random GTK Elements in Doom Colors
A parody implementation that renders GTK widgets styled with the classic Doom palette.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import random
import math
import time

# Classic Doom palette colors (RGB)
DOOM_COLORS = {
    'black': (0, 0, 0),
    'brown': (139, 69, 19),
    'dark_grey': (85, 85, 85),
    'grey': (171, 171, 171),
    'light_grey': (215, 215, 215),
    'red': (171, 0, 0),
    'green': (0, 171, 0),
    'blue': (0, 0, 171),
    'yellow': (215, 215, 0),
    'orange': (215, 107, 0),
    'purple': (171, 0, 171),
    'pink': (255, 171, 255),
    'flesh': (215, 107, 107),
    'dark_green': (0, 107, 0),
    'bright_green': (0, 255, 0),
    'cyan': (0, 255, 255),
}

class DoomWidget(Gtk.DrawingArea):
    """Base widget that renders with Doom colors"""
    
    def __init__(self):
        super().__init__()
        self.color_scheme = {}
        self.set_size_request(100, 100)
        
    def generate_doom_colors(self):
        """Generate a random Doom color scheme"""
        keys = list(DOOM_COLORS.keys())
        self.color_scheme = {
            'bg': DOOM_COLORS[random.choice(keys)],
            'fg': DOOM_COLORS[random.choice(keys)],
            'accent': DOOM_COLORS[random.choice(keys)],
            'highlight': DOOM_COLORS[random.choice(keys)],
        }
        
    def apply_doom_style(self):
        """Apply Doom colors to the widget"""
        self.generate_doom_colors()
        self.queue_draw()


class DoomButton(DoomWidget):
    """A button rendered in Doom style"""
    
    def __init__(self, label="BUTTON"):
        super().__init__()
        self.label = label
        self.pressed = False
        self.connect("button-press-event", self.on_press)
        self.connect("button-release-event", self.on_release)
        
    def on_press(self, widget, event):
        self.pressed = True
        self.queue_draw()
        
    def on_release(self, widget, event):
        self.pressed = False
        self.queue_draw()
        print(f"*{self.label} PRESSED*")
        
    def do_draw(self, cr):
        self.apply_doom_style()
        
        # Draw background
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['bg']])
        cr.paint()
        
        # Draw button border
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['fg']])
        cr.set_line_width(3)
        cr.rectangle(2, 2, self.get_allocated_width()-4, self.get_allocated_height()-4)
        cr.stroke()
        
        # Draw pressed effect
        if self.pressed:
            cr.set_source_rgb(*[c/255 for c in self.color_scheme['accent']])
            cr.rectangle(5, 5, self.get_allocated_width()-10, self.get_allocated_height()-10)
            cr.fill()
            
        # Draw label text (simplified as rectangle blocks)
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['highlight']])
        char_width = 15
        start_x = (self.get_allocated_width() - len(self.label) * char_width) // 2
        for i, char in enumerate(self.label):
            cr.rectangle(start_x + i * char_width, 
                        self.get_allocated_height()//2 - 10, 
                        char_width - 2, 20)
            cr.fill()


class DoomBar(DoomWidget):
    """A status bar like health/ammo bar"""
    
    def __init__(self, value=100, max_value=100):
        super().__init__()
        self.value = value
        self.max_value = max_value
        self.set_size_request(200, 40)
        
    def do_draw(self, cr):
        self.apply_doom_style()
        
        # Background
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['bg']])
        cr.paint()
        
        # Border
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['fg']])
        cr.set_line_width(4)
        cr.rectangle(2, 2, self.get_allocated_width()-4, self.get_allocated_height()-4)
        cr.stroke()
        
        # Fill bar
        fill_ratio = self.value / self.max_value
        fill_width = (self.get_allocated_width() - 12) * fill_ratio
        
        # Color changes based on value
        if fill_ratio > 0.5:
            bar_color = self.color_scheme['green']
        elif fill_ratio > 0.25:
            bar_color = self.color_scheme['yellow']
        else:
            bar_color = self.color_scheme['red']
            
        cr.set_source_rgb(*[c/255 for c in bar_color])
        cr.rectangle(6, 6, fill_width, self.get_allocated_height()-12)
        cr.fill()


class DoomFace(DoomWidget):
    """The iconic Doom face status indicator"""
    
    def __init__(self):
        super().__init__()
        self.expression = 'normal'
        self.set_size_request(60, 80)
        
    def set_expression(self, expr):
        self.expression = expr
        self.queue_draw()
        
    def do_draw(self, cr):
        self.apply_doom_style()
        
        # Background
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['bg']])
        cr.paint()
        
        # Face outline
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['flesh']])
        cr.rectangle(10, 10, 40, 60)
        cr.fill()
        
        # Eyes
        if self.expression == 'angry':
            # Angry eyebrows
            cr.set_source_rgb(*[c/255 for c in self.color_scheme['fg']])
            cr.move_to(15, 25)
            cr.line_to(25, 30)
            cr.move_to(45, 25)
            cr.line_to(35, 30)
            cr.stroke()
            
        # Eye whites
        white_color = self.color_scheme.get('white', (255, 255, 255))
        cr.set_source_rgb(*[c/255 for c in white_color])
        cr.rectangle(15, 30, 10, 8)
        cr.rectangle(35, 30, 10, 8)
        cr.fill()
        
        # Pupils
        cr.set_source_rgb(0, 0, 0)
        pupil_offset = random.randint(-2, 2)
        cr.rectangle(18 + pupil_offset, 33, 4, 4)
        cr.rectangle(38 + pupil_offset, 33, 4, 4)
        cr.fill()
        
        # Mouth
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['red']])
        if self.expression == 'grin':
            cr.arc(30, 55, 10, 0, math.pi)
            cr.stroke()
        elif self.expression == 'ouch':
            cr.arc(30, 55, 10, math.pi, 0)
            cr.stroke()
        else:
            cr.rectangle(25, 55, 10, 3)
            cr.fill()


class DoomCrate(DoomWidget):
    """A decorative crate like in Doom levels"""
    
    def __init__(self):
        super().__init__()
        self.rotation = 0
        
    def do_draw(self, cr):
        self.apply_doom_style()
        
        # Background
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['bg']])
        cr.paint()
        
        # Crate body
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['brown']])
        margin = 5
        cr.rectangle(margin, margin, 
                    self.get_allocated_width() - 2*margin,
                    self.get_allocated_height() - 2*margin)
        cr.fill()
        
        # X pattern
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['fg']])
        cr.set_line_width(4)
        
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        
        cr.move_to(margin, margin)
        cr.line_to(w - margin, h - margin)
        cr.move_to(w - margin, margin)
        cr.line_to(margin, h - margin)
        cr.stroke()
        
        # Border
        cr.rectangle(margin, margin, w - 2*margin, h - 2*margin)
        cr.stroke()


class DoomPortal(DoomWidget):
    """Animated portal/teleporter effect"""
    
    def __init__(self):
        super().__init__()
        self.animation_frame = 0
        GLib.timeout_add(100, self.animate)
        
    def animate(self):
        self.animation_frame += 1
        self.queue_draw()
        return True
        
    def do_draw(self, cr):
        self.apply_doom_style()
        
        # Background
        cr.set_source_rgb(*[c/255 for c in self.color_scheme['bg']])
        cr.paint()
        
        # Portal center
        cx = self.get_allocated_width() // 2
        cy = self.get_allocated_height() // 2
        
        # Animated rings
        for i in range(5):
            radius = 20 + i * 8 + math.sin(self.animation_frame * 0.2 + i) * 5
            alpha = 1.0 - (i / 5.0)
            
            colors = [self.color_scheme['purple'], self.color_scheme['cyan'], 
                     self.color_scheme['green'], self.color_scheme['red']]
            color = colors[i % len(colors)]
            
            cr.set_source_rgba(*[c/255 for c in color], alpha)
            cr.arc(cx, cy, radius, 0, 2 * math.pi)
            cr.set_line_width(3)
            cr.stroke()


class DoomWindow(Gtk.Window):
    """Main Doom-themed window"""
    
    def __init__(self):
        super().__init__(title="DOOM GTK PORT")
        self.set_default_size(800, 600)
        self.set_border_width(10)
        
        # Apply doom-like background
        screen = Gdk.Screen.get_default()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        
        self.connect("destroy", lambda w: Gtk.main_quit())
        
        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        
        # Title bar area
        title_label = Gtk.Label()
        title_label.set_markup('<span size="xx-large" foreground="#ff0000"><b>DOOM</b></span>')
        main_box.pack_start(title_label, False, False, 5)
        
        # Status bar area (top)
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(status_box, False, False, 5)
        
        # Health bar
        health_label = Gtk.Label(label="HEALTH")
        status_box.pack_start(health_label, False, False, 5)
        self.health_bar = DoomBar(value=100, max_value=100)
        status_box.pack_start(self.health_bar, True, True, 5)
        
        # Ammo bar
        ammo_label = Gtk.Label(label="AMMO")
        status_box.pack_start(ammo_label, False, False, 5)
        self.ammo_bar = DoomBar(value=50, max_value=100)
        status_box.pack_start(self.ammo_bar, True, True, 5)
        
        # Doom face
        self.doom_face = DoomFace()
        status_box.pack_start(self.doom_face, False, False, 5)
        
        # Main game area
        game_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(game_area, True, True, 10)
        
        # Left panel - random widgets
        left_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        game_area.pack_start(left_panel, True, True, 5)
        
        # Right panel - more widgets
        right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        game_area.pack_start(right_panel, True, True, 5)
        
        # Center - viewport with portal
        center_viewport = Gtk.Viewport()
        center_viewport.set_size_request(300, 300)
        self.portal = DoomPortal()
        center_viewport.add(self.portal)
        game_area.pack_start(center_viewport, True, True, 5)
        
        # Populate panels with random Doom widgets
        self.populate_panels(left_panel, right_panel)
        
        # Control panel at bottom
        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(control_box, False, False, 5)
        
        # Action buttons
        fire_button = DoomButton("FIRE")
        fire_button.set_size_request(100, 50)
        fire_button.connect("button-release-event", self.on_fire)
        control_box.pack_start(fire_button, False, False, 5)
        
        use_button = DoomButton("USE")
        use_button.set_size_request(100, 50)
        use_button.connect("button-release-event", self.on_use)
        control_box.pack_start(use_button, False, False, 5)
        
        rand_button = DoomButton("RANDOM")
        rand_button.set_size_request(100, 50)
        rand_button.connect("button-release-event", self.on_randomize)
        control_box.pack_start(rand_button, False, False, 5)
        
        # Crates for decoration
        crate1 = DoomCrate()
        crate1.set_size_request(80, 80)
        control_box.pack_end(crate1, False, False, 5)
        
        crate2 = DoomCrate()
        crate2.set_size_request(80, 80)
        control_box.pack_end(crate2, False, False, 5)
        
        # Animation timer for random effects
        GLib.timeout_add(2000, self.random_effects)
        
    def populate_panels(self, left_panel, right_panel):
        """Fill panels with random Doom widgets"""
        widgets = [DoomButton, DoomBar, DoomCrate]
        
        for panel in [left_panel, right_panel]:
            num_widgets = random.randint(3, 5)
            for _ in range(num_widgets):
                widget_type = random.choice(widgets)
                if widget_type == DoomButton:
                    labels = ["RUN", "STRIFE", "INV", "MAP", "WEAP"]
                    widget = DoomButton(random.choice(labels))
                elif widget_type == DoomBar:
                    widget = DoomBar(value=random.randint(0, 100), max_value=100)
                else:
                    widget = DoomCrate()
                
                widget.set_size_request(150, 50)
                panel.pack_start(widget, False, False, 5)
                
    def on_fire(self, widget, event):
        print("*BANG!* Monster damaged!")
        self.doom_face.set_expression('grin')
        # Reduce ammo
        self.ammo_bar.value = max(0, self.ammo_bar.value - random.randint(5, 15))
        self.ammo_bar.queue_draw()
        
    def on_use(self, widget, event):
        print("*CLICK* Used item")
        self.health_bar.value = min(100, self.health_bar.value + random.randint(5, 20))
        self.health_bar.queue_draw()
        self.doom_face.set_expression('normal')
        
    def on_randomize(self, widget, event):
        print("*RANDOMIZE* Changing level...")
        expressions = ['normal', 'angry', 'grin', 'ouch']
        self.doom_face.set_expression(random.choice(expressions))
        
        # Randomize all widget colors
        for child in self.children_recursive():
            if isinstance(child, DoomWidget):
                child.apply_doom_style()
                
    def random_effects(self):
        """Randomly change face expression and update bars"""
        if random.random() < 0.3:
            expressions = ['normal', 'angry', 'grin', 'ouch']
            self.doom_face.set_expression(random.choice(expressions))
            
        # Simulate damage occasionally
        if random.random() < 0.2:
            self.health_bar.value = max(0, self.health_bar.value - random.randint(1, 5))
            self.health_bar.queue_draw()
            if self.health_bar.value < 25:
                self.doom_face.set_expression('ouch')
                
        return True
        
    def children_recursive(self, container=None):
        """Get all child widgets recursively"""
        if container is None:
            container = self
            
        result = []
        if isinstance(container, Gtk.Container):
            for child in container.get_children():
                result.append(child)
                result.extend(self.children_recursive(child))
        return result


def main():
    print("=" * 50)
    print("DOOM GTK PORT - Random Elements in Doom Colors")
    print("=" * 50)
    print("Controls:")
    print("  FIRE  - Shoot (reduces ammo)")
    print("  USE   - Use item (increases health)")
    print("  RANDOM - Randomize colors and effects")
    print("=" * 50)
    
    win = DoomWindow()
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
