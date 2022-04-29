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
import os

import topologic
from topologic import CellComplex

# From https://stackabuse.com/python-how-to-flatten-list-of-lists/
def flatten(element):
	returnList = []
	if isinstance(element, list) == True:
		for anItem in element:
			returnList = returnList + flatten(anItem)
	else:
		returnList = [element]
	return returnList

def getApertures(topology):
	apertures = []
	apTopologies = []
	_ = topology.Apertures(apertures)
	for aperture in apertures:
		apTopologies.append(topologic.Aperture.Topology(aperture))
	return apTopologies

def processItem(item):
	externalVerticalFaces = []
	internalVerticalFaces = []
	topHorizontalFaces = []
	bottomHorizontalFaces = []
	internalHorizontalFaces = []
	externalVerticalApertures = []
	internalVerticalApertures = []
	topHorizontalApertures = []
	bottomHorizontalApertures = []
	internalHorizontalApertures = []

	faces = []
	_ = item.Faces(None, faces)
	for aFace in faces:
		z = topologic.FaceUtility.NormalAtParameters(aFace, 0.5, 0.5)[2]
		cells = []
		aFace.Cells(item, cells)
		n = len(cells)
		if abs(z) < 0.001:
			if n == 1:
				externalVerticalFaces.append(aFace)
				externalVerticalApertures.append(getApertures(aFace))
			else:
				internalVerticalFaces.append(aFace)
				internalVerticalApertures.append(getApertures(aFace))
		elif n == 1:
			if z > 0.9:
				topHorizontalFaces.append(aFace)
				topHorizontalApertures.append(getApertures(aFace))
			elif z < -0.9:
				bottomHorizontalFaces.append(aFace)
				bottomHorizontalApertures.append(getApertures(aFace))

		else:
			internalHorizontalFaces.append(aFace)
			internalHorizontalApertures.append(getApertures(aFace))
	return1 = []
	return2 = []
	return3 = []
	return4 = []
	return5 = []
	return6 = []
	return7 = []
	return8 = []
	return9 = []
	return10 = []
	if len(externalVerticalFaces) > 0:
		return1 = topologic.Cluster.ByTopologies(flatten(externalVerticalFaces))
	if len(internalVerticalFaces) > 0:
		return2 = topologic.Cluster.ByTopologies(flatten(internalVerticalFaces))
	if len(topHorizontalFaces) > 0:
		return3 = topologic.Cluster.ByTopologies(flatten(topHorizontalFaces))
	if len(bottomHorizontalFaces) > 0:
		return4 = topologic.Cluster.ByTopologies(flatten(bottomHorizontalFaces))
	if len(internalHorizontalFaces) > 0:
		return5 = topologic.Cluster.ByTopologies(flatten(internalHorizontalFaces))
	if len(externalVerticalApertures) > 0:
		return6 = topologic.Cluster.ByTopologies(flatten(externalVerticalApertures))
	if len(internalVerticalApertures) > 0:
		return7 = topologic.Cluster.ByTopologies(flatten(internalVerticalApertures))
	if len(topHorizontalApertures) > 0:
		return8 = topologic.Cluster.ByTopologies(flatten(topHorizontalApertures))
	if len(bottomHorizontalApertures) > 0:
		return9 = topologic.Cluster.ByTopologies(flatten(bottomHorizontalApertures))
	if len(internalHorizontalApertures) > 0:
		return10 = topologic.Cluster.ByTopologies(flatten(internalHorizontalApertures))

	return [return1, return2, return3, return4, return5, return6, return7, return8, return9, return10]


def decompose(sel):
	doc = FreeCAD.ActiveDocument
	sel.ViewObject.Transparency = 75
	doc.recompute()
	selString = sel.Shape.exportBrepToString()
	top = topologic.Topology.ByString(selString)
	items = processItem(top)
	names = ["ext_vert", "int_vert", "top_horz", "btm_horz", "int_horz"]
	for i in range(len(names)):
		item = items[i]
		if isinstance(item, topologic.Cluster):
			sh=Part.Shape()
			sh.importBrepFromString(str(item.String()))
			f = doc.addObject("Part::Feature", sel.Name+"_"+names[i]) # create a document with a feature
			f.Shape = sh # Assign the shape to the shape property
	doc.recompute()

class TPCellComplexDecompose():
	"""CellComplex"""
	
	def GetResources(self):
		return {'Accel' : "Shift+S", # a default shortcut (optional)
				'MenuText': "TPCellComplexDecompose",
				'ToolTip' : "Decompose the CellComplex",
				'Pixmap' : os.path.join(FreeCAD.__path__[2],'Topologic','Resources','icons','TPDecompose.svg')}

	def Activated(self):
		selections = FreeCADGui.Selection.getSelection()
		if isinstance(selections, list) == False:
			selections = [selections]
		for sel in selections:
			decompose(sel)
		"""Do something here"""
		return

	def IsActive(self):
		"""Here you can define if the command must be active or not (greyed) if certain conditions
		are met or not. This function is optional."""
		return True

FreeCADGui.addCommand('TPCellComplexDecompose',TPCellComplexDecompose())