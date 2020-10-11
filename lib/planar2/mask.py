#############################################################################
# Copyright (c) 2020 by R. Patrick Xian
# Distributed under the MIT License
#############################################################################


import numpy as np
import warnings as wn

try:
    import torch
except:
    wn.warn('Cannot import pytorch package! Operations using PyTorch Tensors not supported.')


def coords2d(center=(0, 0), xlen=64, ylen=64, package='torch'):
    """Generate 2D coordinates.
    """
    
    xlen, ylen = int(xlen), int(ylen)
    xaxis = range(-center[1], xlen-center[1])
    yaxis = range(-center[0], ylen-center[1])
    ncoords = xlen*ylen
    
    if package == 'numpy':
        out = np.stack(np.meshgrid(yaxis, xaxis), axis=2)
    elif package == 'torch':
        xaxis, yaxis = torch.Tensor(xaxis), torch.Tensor(yaxis)
        out = torch.stack(torch.meshgrid(yaxis, xaxis), dim=2)
    out = out.reshape((ncoords, 2))
    
    return out