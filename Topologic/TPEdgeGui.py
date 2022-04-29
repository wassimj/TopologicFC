# * This file is part of Topologic software library.
# * Copyright(C) 2021, Cardiff University and University College London
# * 
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU Affero General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# * 
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU Affero General Public License for more details.
# * 
# * You should have received a copy of the GNU Affero General Public License
# * along with this program. If not, see <https://www.gnu.org/licenses/>.

import FreeCAD
from FreeCAD import Qt
import FreeCADGui
import Part
import math
import sys

import topologic
from topologic import Vertex
import os

def getEdges(sel):
    doc = FreeCAD.ActiveDocument
    sel.ViewObject.Transparency = 75
    doc.recompute()
    selString = sel.Shape.exportBrepToString()
    top = topologic.Topology.ByString(selString)
    edges = []
    _ = top.Edges(None, edges)
    topologies = []
    for edge in edges:
        copyTopology = topologic.Topology.DeepCopy(edge)
        topologies.append(copyTopology)

    cluster = topologic.Cluster.ByTopologies(topologies)
    sh=Part.Shape()
    sh.importBrepFromString(str(cluster.String()))
    f = doc.addObject("Part::Feature", sel.Name+"_"+"Edges") # create a document with a feature
    f.Shape = sh # Assign the shape to the shape property
    doc.recompute()

class TPEdges():
	"""Edge"""
	
	def GetResources(self):
		return {'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "TPEdges",
                'ToolTip' : "Creates an Edges Cluster from the input object",
                'Pixmap' : os.path.join(FreeCAD.__path__[2],'Topologic','Resources','icons','TPEdges.svg')}

	def Activated(self):
		selections = FreeCADGui.Selection.getSelection()
		if isinstance(selections, list) == False:
			selections = [selections]
		for sel in selections:
			getVertices(sel)
		"""Do something here"""
		return

	def IsActive(self):
		"""Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
		return True

FreeCADGui.addCommand('TPEdges',TPEdges())