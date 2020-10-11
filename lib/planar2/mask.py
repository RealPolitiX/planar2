#############################################################################
# Copyright (c) 2020 by R. Patrick Xian
# Distributed under the MIT License
#############################################################################


import numpy as np
import warnings as wn
import planar2 as planar

try:
    import torch
except:
    wn.warn('Cannot import pytorch package! Operations using PyTorch Tensors not supported.')


def coords2d(center=(0, 0), xlen=64, ylen=64, package='numpy'):
    """Generate 2D coordinates.
    """
    
    xlen, ylen = int(xlen), int(ylen)
    center = tuple(map(int, center))
    xaxis = range(-center[1], xlen-center[1])
    yaxis = range(-center[0], ylen-center[0])
    ncoords = xlen * ylen
    
    if package == 'numpy':
        coords = np.stack(np.meshgrid(yaxis, xaxis), axis=2)
        coords = coords.astype('float')
    elif package == 'torch':
        xaxis, yaxis = torch.Tensor(xaxis), torch.Tensor(yaxis)
        coords = torch.stack(torch.meshgrid(yaxis, xaxis), dim=2)
    coords = coords.reshape((ncoords, 2))
    
    return coords


class PolygonMask(planar.Polygon):
    """Polygon mask class."""
    
    def __init__(self, vertices, **kwargs):
        super(PolygonMask, self).__init__(vertices, **kwargs)
        
    def to_mask(self, xlen=64, ylen=64, package='numpy', fill='constant', fillfunc=1, ret=False):
        """Convert boundary to mask."""
        
        self.xycoords = coords2d(self.centroid, xlen, ylen, package)
        self.mask = np.asarray(list(map(self.contains_point, self.xycoords)))
        self.masksize = xlen * ylen
        
        if fill == 'constant':
            self.mask = fillfunc * self.mask
        elif fill == 'xnan':
            self.mask[np.where(self.mask == 0)] = np.nan
        elif fill == 'gaussian':
            self.mask = _fill_gaussian(self.centroid, self.mask, **kwargs)
        elif fill == 'edge_decay':
            self.mask = _fill_edge_decay(self.mask, self.verts, self.mask, **kwargs)
        elif fill == 'udf': # User-defined function
            self.mask = fillfunc(self.mask)
            
        self.mask = self.mask.reshape((xlen, ylen))
        if ret:
            return self.mask
    
    @staticmethod
    def _fill_gaussian(center, mask):
        pass
    
    @staticmethod
    def _fill_edge_decay(center, verts, mask):
        pass