from bgfactory.components.component import Component


class Rotation(Component):
    
    def __init__(self, component, n_clockwise=1):
        self.component = component
        self.n_counterclockwise = n_clockwise
        
    def get_size(self):
        size = self.component.get_size()
        return reversed(size)
    
    def draw(self, w, h):
        
        surface = super(Rotation, self).draw(w, h)
        
        comp_surface = self.component.draw(h, w)
        comp_surface.