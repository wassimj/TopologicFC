import topologic

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
