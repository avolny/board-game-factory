from bgfactory.components.component import Component

"""
TODO: start implementing graphical transformations for transforming arbitrary component draw output
These classes should serve as wrappers around the render method of a component.
They take the render output of the component and apply additional processing on it before returning it
to the component's parent.
"""
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
        # comp_surface.