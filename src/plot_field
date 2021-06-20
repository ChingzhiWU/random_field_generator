"""
Code for plotting a 3D field using matplotlib
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib
import matplotlib.colors as colors


def cmap_map(function, cmap):
    """ Applies function (which should operate on vectors of shape 3: [r, g, b]), on colormap cmap.
    This routine will break any discontinuous points in a colormap.
    """
    cdict = cmap._segmentdata
    step_dict = {}
    # Firt get the list of points where the segments start or end
    for key in ('red', 'green', 'blue'):
        step_dict[key] = list(map(lambda x: x[0], cdict[key]))
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step : np.array(cmap(step)[0:3])
    old_LUT = np.array(list(map(reduced_cmap, step_list)))
    new_LUT = np.array(list(map(function, old_LUT)))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i, key in enumerate(['red','green','blue']):
        this_cdict = {}
        for j, step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j, i]
            elif new_LUT[j,i] != old_LUT[j, i]:
                this_cdict[step] = new_LUT[j, i]
        colorvector = list(map(lambda x: x + (x[1], ), this_cdict.items()))
        colorvector.sort()
        cdict[key] = colorvector

    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)


def cube_faces(cube, view): #normalize = False
    if view == 'front':
        (xy, xz, yz) = (cube[0, :, :], cube[:, 0, :], cube[:, :, 0])
    elif view == 'back':
        (xy, xz, yz) = (cube[0, :, :], cube[:, -1, :], cube[:, :, -1])
    elif view == 'left':
        (xy, xz, yz) = (cube[0, :, :], cube[:, 0, :], cube[:, :, -1])
    elif view == 'right':
        (xy, xz, yz) = (cube[0, :, :], cube[:, -1, :], cube[:, :, 0])
    #return(np.log(xy),np.log(xz),np.log(yz))
    return(xy,xz,yz)

def plotcube(cube,x=None,y=None,z=None,normalize=False,view='front',detail=10,minval=True,maxval=True):
    """Use contourf to plot cube marginals"""

    cube = np.moveaxis(cube, [0, 1, 2], [1, 2, 0])

    (Z,Y,X) = cube.shape
    (xy,xz,yz) = cube_faces(cube,view)
    if x == None: x = np.arange(X)
    if y == None: y = np.arange(Y)
    if z == None: z = np.arange(Z)

    #this removes perspective from the 3D plot. Delete this block and use the "proj_type='ortho' when matplotlib updates to version 2.2.2 in conda
    from mpl_toolkits.mplot3d import proj3d
    def orthogonal_proj(zfront, zback):
        a = (zfront + zback) / (zfront - zback)
        b = -2 * (zfront * zback) / (zfront - zback)
        return np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, a, b],
                            [0, 0, -0.0000000000001, zback]])

    proj3d.persp_transformation = orthogonal_proj

    fig = plt.figure()
    ax = fig.gca(projection='3d') # ,proj_type = 'ortho')
    ax.set_aspect('auto')
    ax.set_axis_off()

    # draw edge marginal surfaces

    if view == 'front':
        offsets = (0, 0, 0)
        ax.view_init(elev=215.264, azim=45) #45  # 170.264
    elif view == 'back':
        offsets = (0,Y-1,X-1)
        ax.view_init(elev=215.264, azim=225)  # 170.264
    elif view == 'left':
        offsets = (0,0,X-1)
        ax.view_init(elev=215.264, azim=135)  # 170.264
    elif view == 'right':
        offsets = (0,Y-1,0)
        ax.view_init(elev=215.264, azim=315)  # 170.264

    if isinstance(minval,bool):
        minval = min(np.min(xy),np.min(xz),np.min(yz))/1
    if isinstance(maxval, bool):
        maxval = max(np.max(xy),np.max(xz),np.max(yz))*1
    #levels = np.arange(minval, maxval, (maxval-minval)/detail)

    levels = np.logspace(math.log(minval), math.log(maxval), detail, base=np.exp(1))



    # cset = ax.contourf(x[None,:].repeat(Y,axis=0), y[:,None].repeat(X,axis=1), xy, zdir='z', offset=offsets[0], cmap='copper', alpha=1.0, vmin = minval, vmax = maxval, levels = levels) #, norm = LogNorm()
    # cset = ax.contourf(x[None,:].repeat(Z,axis=0), xz, z[:,None].repeat(X,axis=1), zdir='y', offset=offsets[1], cmap=cmap_map(lambda x: x*0.9, matplotlib.cm.copper), alpha=1.0, levels = levels) #, vmin = minval, vmax = maxval
    # cset = ax.contourf(yz, y[None,:].repeat(Z,axis=0), z[:,None].repeat(Y,axis=1), zdir='x', offset=offsets[2], cmap=cmap_map(lambda x: x*0.8, matplotlib.cm.copper), alpha=1.0, levels = levels) #, vmin = minval, vmax = maxval

    cset = ax.contourf(x[None,:].repeat(Y,axis=0), y[:,None].repeat(X,axis=1), xy, zdir='z', offset=offsets[0], cmap='copper', alpha=1.0, vmin = minval, vmax = maxval, levels = levels,norm=colors.LogNorm(vmin=minval, vmax=maxval)) #, norm = LogNorm()
    cset = ax.contourf(x[None,:].repeat(Z,axis=0), xz, z[:,None].repeat(X,axis=1), zdir='y', offset=offsets[1], cmap=cmap_map(lambda x: x*0.9, matplotlib.cm.copper), alpha=1.0, levels = levels,norm=colors.LogNorm(vmin=minval, vmax=maxval)) #, vmin = minval, vmax = maxval
    cset = ax.contourf(yz, y[None,:].repeat(Z,axis=0), z[:,None].repeat(Y,axis=1), zdir='x', offset=offsets[2], cmap=cmap_map(lambda x: x*0.8, matplotlib.cm.copper), alpha=1.0, levels = levels,norm=colors.LogNorm(vmin=minval, vmax=maxval)) #, vmin = minval, vmax = maxval
    #

    #plt.colorbar(cset)

    # draw wire cube to aid visualization
    #ax.plot([0,X-1,X-1,0,0],[0,0,Y-1,Y-1,0],[0,0,0,0,0],'k-')
    #ax.plot([0,X-1,X-1,0,0],[0,0,Y-1,Y-1,0],[Z-1,Z-1,Z-1,Z-1,Z-1],'k-')
    #ax.plot([0,0],[0,0],[0,Z-1],'k-')
    #ax.plot([X-1,X-1],[0,0],[0,Z-1],'k-')
    #ax.plot([X-1,X-1],[Y-1,Y-1],[0,Z-1],'k-')
    #ax.plot([0,0],[Y-1,Y-1],[0,Z-1],'k-')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    #ax.autoscale()


    ax.set_zlim(0, cube.shape[0])
    ax.set_xlim(0, cube.shape[1])
    ax.set_ylim(0, cube.shape[2])
    plt.show()
    print()
