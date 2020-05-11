from abc import ABC, abstractmethod

import cairocffi as cairo


class LayoutError(ValueError):
    pass


class LayoutManager(ABC):
    
    def __init__(self):
        pass
    
    def set_parent(self, parent):
        self.parent = parent
    
    @abstractmethod
    def _draw(self, surface: cairo.Surface, w, h):
        pass
    
    @abstractmethod
    def get_size(self):
        pass
    
    @abstractmethod
    def validate_child(self, child):
        pass

# class FlowLayoutHorizontal(LayoutManager):
#     
#     def __init__(self, padding=(5,5)):
#         """
#         :param padding: (left, top) 
#         """
#         self.padding = padding
#         
#     def get_size(self):
#         w, h = None, None
# 
#         if self.parent.w != INFER:
#             w = self.parent.w
# 
#         if self.parent.h != INFER:
#             h = self.parent.h
#         
#     def _draw(self, im: Image):
#         children = self.parent.children
#         
#         x, y = self.padding[:2]
#         for child in children:
#             im_ = child.draw_(im)
#             im.paste(im_, (x, y), im_)
#             
#             x += im_.size[0] + self.padding[0] + self.padding[2]

