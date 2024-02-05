from game_qu.gui_components.component import Component
from game_qu.base.colors import light_blue


class Tile(Component):
    """A tile on the tile map"""

    is_active = False
    is_temporarily_invisible = False
    tile_color = None

    def set_color(self, color):
        self.color = color
        self.tile_color = color

    def set_is_active(self, is_active):
        self.is_active = is_active

    def get_is_active(self):
        return self.is_active

    def get_is_visible(self):
        return self.is_visible or self.is_active

    def set_is_temporarily_invisible(self, is_temporarily_invisible):
        self.is_temporarily_invisible = is_temporarily_invisible

    def get_is_temporarily_invisible(self):
        return self.is_temporarily_invisible

    def render(self):
        """Renders the tile"""

        self.color = light_blue if self.is_temporarily_invisible else self.tile_color
        super().render()

