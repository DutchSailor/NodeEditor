# implemenation of the compute methods for category 

import numpy as np
import random
import time
import os.path
from os import path
import matplotlib.pyplot as plt
import scipy.interpolate

from nodeeditor.say import *
import nodeeditor.store as store
import nodeeditor.pfwrap as pfwrap


print ("reloaded: "+ __file__)



from nodeeditor.cointools import *





'''
Discretizes the curve and returns a list of points.
The function accepts keywords as argument:
discretize(Number=n) => gives a list of 'n' equidistant points
discretize(QuasiNumber=n) => gives a list of 'n' quasi equidistant points (is faster than the method above)
discretize(Distance=d) => gives a list of equidistant points with distance 'd'
discretize(Deflection=d) => gives a list of points with a maximum deflection 'd' to the curve
discretize(QuasiDeflection=d) => gives a list of points with a maximum deflection 'd' to the curve (faster)
discretize(Angular=a,Curvature=c,[Minimum=m]) => gives a list of points with an angular deflection of 'a'
                                    and a curvature deflection of 'c'. Optionally a minimum number of points
                                    can be set which by default is set to 2.        
'''


def run_FreeCAD_Discretize(self,*args, **kwargs):
    sayl()
    count=self.getData("count")
    edge=self.getPinObject("Wire")
    say(edge)
    if edge is None: return
    
    
    k=self.getData('deflection') 
    if k>0:
        ptsa=edge.discretize(QuasiDeflection=k*0.01)
    else:
        ptsa=edge.discretize(count)

    self.setPinObject("Shape_out",Part.makePolygon(ptsa))
    if 0:
        sc=Part.BSplineCurve()
        sc.buildFromPoles(ptsa)
        self.setPinObject("Shape_out",sc.toShape())
    

    return

    pts=edge.discretize(count*10)
    #Part.show(Part.makePolygon(pts))
    face=FreeCAD.ActiveDocument.BePlane.Shape.Face1
    sf=face.Surface
    r=200
    pts2=[]
    pts3=[]
    for i in range(len(pts)-1):
        p=pts[i]
        u,v=sf.parameter(p)
        say(u,v)
        t=(pts[i+1]-p).normalize()
        say(t)
        n=sf.normal(u,v)
        say(n)
        u,v=sf.parameter(p+n.cross(t)*r)
        pts2 += [sf.value(u,v)]
        u,v=sf.parameter(p-n.cross(t)*r)
        pts3 += [sf.value(u,v)]
    closed=True
    if 0:
        if closed:
            Part.show(Part.makePolygon(pts2+[pts2[0]]))
            Part.show(Part.makePolygon(pts3+[pts3[0]]))
        else:
            Part.show(Part.makePolygon(pts2))
            Part.show(Part.makePolygon(pts3))




