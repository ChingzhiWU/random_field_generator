"""
Functions for generating normally-distributed, 1D, 2D or 3D random fields. 
The approach uses the "stepwise covariance matrix decomposition" (SCMD) method,
which greatly reduces both the required RAM and computational time compared to
the original CMD method. The downside is that it produces a 'streaked' appearance,
however this does not affect the field statistics and therefore is not of concern.

Compared to other methods of generating 3D random fields, this method has comparable
speed (although could be a lot faster if programmed in a compiled language), good 
accuracy, and most importantly can vary the Scale of Fluctuation independantly in
the different axes.

Two approaches are given, the fully-seperable SCMD method, and the partially-seperable
SCMD method. The advantage of the latter is that it does not produced a streaked
appearnce in the X-Y plane. However the disadvantage is that a single Scale of Fluctation
is used in both the X and Y directions. It also uses more RAM and takes longer to
process.

Note that for each approach, two functions are given. The first is a _prep function which
computes the covariance matrix decomposition and only needs to be called once for a
given set of inputs. The second is a _gen function which produces the actual random field.
Technically, the functions are for 3D random fields, however lower dimensions can be 
achieved by making the field size equal to 1 element thickness in the relevant directions.

An overview of the process can be found in this freely-available conference paper:
http://rpsonline.com.sg/proceedings/isgsr2019/pdf/IS12-11.pdf

"""

import matplotlib.pyplot as plt #Library for plotting
import numpy as np #library for multi-dimensional arrays and associated functions


# Separable correlation function
def CorrFun1(d, t):
    return np.exp(-2 * d / t)



def StepwiseCMD_3D_prep(fsize,sof,de):

    """
    Demonstration for univariate 3-D random field simulation using stepwise
        covariance matrix decomposition method
    Written by Te XIAO [short_xiaote@whu.edu.cn] (2018/12/01)
    For more details, please refer to:
        Li DQ, Xiao T, Zhang LM, & Cao ZJ. (2019). Stepwise covariance
        matrix decomposition for efficient simulation of multivariate
        large-scale three-dimensional random fields. Applied Mathematical
        Modelling, 68, 169-181. DOI: 10.1016/j.apm.2018.11.011
    Converted to Python code by Michael Crisp. The best way to install Python
        and the commonly-used libraries referened here is with Anaconda:
                                  https://www.anaconda.com/distribution/
                                  
    """


    # Node
    x = np.arange(0, fsize[0],de[1])
    y = np.arange(0, fsize[1],de[1])
    z = np.arange(0, fsize[2],de[2])
    # Relative distance
    [d2, d1] = np.meshgrid(x,x); Dx = np.abs(d1-d2)
    [d2, d1] = np.meshgrid(y,y); Dy = np.abs(d1-d2)
    [d2, d1] = np.meshgrid(z,z); Dz = np.abs(d1-d2)
    # Correlation matrix & Cholesky decomposition
    R = CorrFun1(Dx, sof[0]); Lx = np.linalg.cholesky(R)
    R = CorrFun1(Dy, sof[1]); Ly = np.linalg.cholesky(R)
    R = CorrFun1(Dz, sof[2]); Lz = np.linalg.cholesky(R)

    return (Lx, Ly, Lz)


def StepwiseCMD_3D_gen(cor_vecs, fsize):

        # Independent random variable
    X = np.random.normal(0,1,[fsize[0], fsize[1], fsize[2]])           # nx-ny-nz array
    # Random field simulation, U --> X
    X = np.dot(cor_vecs[0] ,np.reshape(X, [fsize[0], fsize[1]*fsize[2]]))     # nx-ny*nz matrix
    X = np.reshape(X, [fsize[0], fsize[1], fsize[2]])       # nx-ny-nz array
    X = np.transpose(X, [1, 2, 0])                      # ny-nz-nx array
    X = np.dot(cor_vecs[1] ,np.reshape(X, [fsize[1], fsize[2]*fsize[0]]))     # ny-nz*nx matrix
    X = np.reshape(X, [fsize[1], fsize[2], fsize[0]])       # ny-nz-nx array
    X = np.transpose(X, [1, 2, 0])                      # nz-nx-ny array
    X = np.dot(cor_vecs[2] ,np.reshape(X, [fsize[2], fsize[0]*fsize[1]]))     # nz-nx*ny matrix
    X = np.reshape(X, [fsize[2], fsize[0], fsize[1]])       # nz-nx-ny array
    X = np.transpose(X, [1, 2, 0])                      # nx-ny-nz array

    return X



def partial_3D_prep(fsize,sof,de):
    """
    Demonstration for univariate 3-D random field simulation using stepwise
        covariance matrix decomposition method
    Written by Te XIAO [short_xiaote@whu.edu.cn] (2018/12/01)
    For more details, please refer to:
        Li DQ, Xiao T, Zhang LM, & Cao ZJ. (2019). Stepwise covariance
        matrix decomposition for efficient simulation of multivariate
        large-scale three-dimensional random fields. Applied Mathematical
        Modelling, 68, 169-181. DOI: 10.1016/j.apm.2018.11.011
    """


    # Node
    x = np.arange(0, fsize[0],de[1])
    y = np.arange(0, fsize[1],de[1])
    z = np.arange(0, fsize[2],de[2])
    # Relative distance
    [x2, x1] = np.meshgrid(x,x); Dx = np.abs(x1-x2)
    [y2, y1] = np.meshgrid(y,y); Dy = np.abs(y1-y2)
    [z2, z1] = np.meshgrid(z,z); Dz = np.abs(z1-z2)
# Relative distance
    [xh, yh] = np.meshgrid(x, y); xh=xh.ravel().astype('f4'); yh=yh.ravel().astype('f4')
    [x2, x1] = np.meshgrid(xh,xh); Dx = np.abs(x1-x2); del x1,x2,xh
    [y2, y1] = np.meshgrid(yh,yh); Dy = np.abs(y1-y2); del y1,y2,yh
    Dxy = np.sqrt(Dx**2+Dy**2); del Dx,Dy
    [z2, z1] = np.meshgrid(z,z); Dz = np.abs(z1-z2).astype('f4'); del z1,z2
# Correlation matrix & Cholesky decomposition
    Rxy = CorrFun1(Dxy, sof[0]); del Dxy

    Lxy = np.linalg.cholesky(Rxy); del Rxy
    Rz = CorrFun1(Dz, sof[-1]); Lz = np.linalg.cholesky(Rz)


    return (Lxy, Lz)

def partial_3D_gen(cor_vecs, fsize):
# Random field simulation


    U = np.random.normal(0,1,[fsize[0]*fsize[1], fsize[2]]).astype(dtype='f4')           # nx-ny-nz array
    U = np.dot(np.dot(cor_vecs[0],U), cor_vecs[1])
    U = np.reshape(U, [fsize[0], fsize[1], fsize[2]])

    return U

