from __future__ import print_function
from abaqus import *
from abaqusConstants import *
from viewerModules import *

vps = session.viewports.values()[0]
odbName = vps.displayedObject.name
odb = session.odbs[odbName]


disp = session.viewports[vps.name].odbDisplay.primaryVariable

var = disp[0]

pos = disp[1]
# 0: UNDEFINED_POSITION
# 1: NODAL
# 2: INTEGRATION_POINT
# 3: ELEMENT_FACE
# 4: ELEMENT_NODAL
# 5: WHOLE_ELEMENT
# 6: ELEMENT_CENTROID
# 7: WHOLE_REGION
# 8: WHOLE_PART_INSTANCE
# 9: WHOLE_MODEL
# 10: GENERAL_PARTICLE


ref = disp[3]
# 0: NO_REFINEMENT
# 1: INVARIANT
# 2: COMPONENT

label = disp[5]

######################################################################

stepcount=0
maxlist = []
minlist = []
listtime = []

numsteps = len(session.odbs[odbName].steps.keys())


for stepid in range(numsteps):
	mystep = session.odbs[odbName].steps.keys()[stepid]
	if session.odbs[odbName].steps[mystep].domain != TIME:
		continue
	stepcount += 1
	numframes = len(session.odbs[odbName].steps[mystep].frames)

	#for myframe in session.odbs[odbName].steps[mystep].frames:
	for frameid in range(numframes):
		myframe=session.odbs[odbName].steps[mystep].frames[frameid]
		frametime = myframe.frameValue

		if stepcount > 1 and frametime == 0.0:
			continue

		session.viewports[vps.name].odbDisplay.setFrame(step=stepid, frame=frameid)
		ttime=0
		if stepcount>1:
			ttime=session.odbs[odbName].steps[mystep].totalTime
		ctime = ttime+frametime
		listtime.append(round(ctime,5))
		
		maxvalue = session.defaultOdbDisplay.contourOptions.autoMaxValue
		minvalue = session.defaultOdbDisplay.contourOptions.autoMinValue

		maxlist.append(maxvalue)
		minlist.append(minvalue)

######################################################################

if len(listtime) != len(maxlist):
	print('Lists unequal')

maxdata = zip(listtime, maxlist)
mindata = zip(listtime, minlist)

##

xQuantity = visualization.QuantityType(type=TIME)
yQuantity = visualization.QuantityType(type=NONE)

session.XYData(name=var+' - '+label+' max vs time', data=tuple(maxdata), 
    sourceDescription='Extracted with script', axis1QuantityType=xQuantity, 
    axis2QuantityType=yQuantity, )

session.XYData(name=var+' - '+label+' min vs time', data=tuple(mindata), 
    sourceDescription='Extracted with script', axis1QuantityType=xQuantity, 
    axis2QuantityType=yQuantity, )

print('Done')

