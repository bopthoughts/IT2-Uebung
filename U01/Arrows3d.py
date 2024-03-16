# Copyright https://gist.github.com/WetHat Peter Ernst

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.text import Annotation
from matplotlib.patches import FancyArrowPatch

all_points = None

class Annotation3D(Annotation):

    def __init__(self, text, xyz, *args, **kwargs):
        super().__init__(text, xy=(0, 0), *args, **kwargs)
        self._xyz = xyz

    def draw(self, renderer):
        x2, y2, z2 = proj_transform(*self._xyz, self.axes.M)
        self.xy = (x2, y2)
        super().draw(renderer)

def _annotate3D(ax, text, xyz, *args, **kwargs):
    '''Add anotation `text` to an `Axes3d` instance.'''

    annotation = Annotation3D(text, xyz, *args, **kwargs)
    ax.add_artist(annotation)


class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)
        
    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs) 

def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


def plotvec(ax, frompoint, topoint, **kwargs):
    global all_points
    if all_points is not None:
        all_points = np.hstack([all_points, frompoint])
        all_points = np.hstack([all_points, topoint])
    else:
        all_points = np.hstack([frompoint, topoint])
    x1,y1,z1 = frompoint.flat
    x2,y2,z2 = topoint.flat
    kwargs = {
        'mutation_scale': 20,
        'arrowstyle': '-|>', 
    } | kwargs
    ax.arrow3D(x1,y1,z1, x2-x1,y2-y1,z2-z1, **kwargs)
    
def plotpoint(ax, point, **kwargs):
    global all_points
    if all_points is not None:
        all_points = np.hstack([all_points, point])
    else:
        all_points = point
    x,y,z = point.flat
    ax.plot3D(x,y,z, **kwargs)
 
def autoscale(ax, oversize=1.):
    x_range = np.array([all_points[0, :].min(), all_points[0, :].max()])
    y_range = np.array([all_points[1, :].min(), all_points[1, :].max()])
    z_range = np.array([all_points[2, :].min(), all_points[2, :].max()])

    ax.set_xlim(x_range * oversize)
    ax.set_ylim(y_range * oversize)
    ax.set_zlim(z_range * oversize)


    
def install_extensions():
    setattr(Axes3D, 'arrow3D', _arrow3D)
    setattr(Axes3D, 'annotate3D', _annotate3D)