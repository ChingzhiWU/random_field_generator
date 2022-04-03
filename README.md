# Random Field Generator

![Python Logo](./python_logo.png)
## Description
Functions for generating normally-distributed, 1D, 2D or 3D random fields. The approach uses the "stepwise covariance matrix decomposition" (SCMD) method, which greatly reduces both the required RAM and computational time compared to the original CMD method. The downside is that it produces a 'streaked' appearance, however this does not affect the field statistics and therefore is not of concern. 

Compared to other methods of generating 3D random fields, this method has comparable speed (although could be a lot faster if programmed in a compiled language), good accuracy, and most importantly can vary the Scale of Fluctuation independantly in the different axes. The code is also very simple.

Two approaches are given, the fully-seperable SCMD method, and the partially-seperable SCMD method. The advantage of the latter is that it does not produced a streaked appearnce in the X-Y plane. However the disadvantage is that a single Scale of Fluctation is used in both the X and Y directions. It also uses more RAM and takes longer to process.

Note that for each approach, two functions are given. The first is a _prep function which computes the covariance matrix decomposition and only needs to be called once for a given set of inputs. The second is a _gen function which produces the actual random field.
Technically, the functions are for 3D random fields, however lower dimensions can be achieved by making the field size equal to 1 element thickness in the relevant directions.

An overview of the process can be found in this freely-available conference paper:
http://rpsonline.com.sg/proceedings/isgsr2019/pdf/IS12-11.pdf

## Repository Ownership
* **Practice**: INSERT HERE
* **Sector**: - INSERT HERE
* **Original Author(s)**: - INSERT HERE
* **Contact Details for Current Repository Owner(s)**: michael.crisp@mottmac.com
## Installation Instructions
The code relies on commonly-available third-party packages Matplotlib, Numpy and Scipy. You can install Anaconda Python which includes these packages and many more: https://www.anaconda.com/
