# coppeliaSim
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# coppeliaSim
import pandas as pd
import timeit, numpy, scipy
import matplotlib.pyplot as plt
def drawRobot(x,y,q,s,h):
    p=numpy.zeros(36).reshape(12,3)
    p[0,:]=[1,1/7,1/s]
    p[1,:]=[-3/7,1,1/s]
    p[2,:]=[-5/7,6/7,1/s]
    p[3,:]=[-5/7,5/7,1/s]
    p[4,:]=[-3/7,2/7,1/s]
    p[5,:]=[-3/7,0,1/s]
    p[6,:]=[-3/7,-2/7,1/s]
    p[7,:]=[-5/7,-5/7,1/s]
    p[8,:]=[-5/7,-6/7,1/s]
    p[9,:]=[-3/7,-1,1/s]
    p[10,:]=[1,-1/7,1/s]
    p[11,:]=[1,1/7,1/s]
    #
    p=s*p*100
    #
    r=numpy.zeros(6).reshape(3,2)
    r[0,:]=[numpy.cos(q),numpy.sin(q)]
    r[1,:]=[-numpy.sin(q),numpy.cos(q)]
    r[2,:]=[x,y]
    #
    p=numpy.dot(p,r)
    X=p[:,0]
    Y=p[:,1]
    h.plot(X,Y,'r-')
#
#
D=195e-3
R=D/2
L=381e-3
print('Starting simpleTest.py ...')
#
client = RemoteAPIClient()
sim = client.getObject('sim')

# When simulation is not running, ZMQ message handling could be a bit
# slow, since the idle loop runs at 8 Hz by default. So let's make
# sure that the idle loop runs at full speed for this program:
defaultIdleFps = sim.getInt32Param(sim.intparam_idle_fps)
sim.setInt32Param(sim.intparam_idle_fps, 0)

dt=sim.getSimulationTimeStep()

objectName='/PioneerP3DX'
rightMotor=sim.getObject('/PioneerP3DX/rightMotor')
leftMotor=sim.getObject('/PioneerP3DX/leftMotor')
PioneerP3DX=sim.getObject('/PioneerP3DX')
#
objectPosition=sim.getObjectPosition(PioneerP3DX,-1)
objectOrientation=sim.getObjectOrientation(PioneerP3DX,-1)
objectQuaternion=sim.getObjectQuaternion(PioneerP3DX,-1)
client.setStepping(True)
#
#np=350
np=350
tf=np*dt
t=numpy.zeros(np+1)
xp=numpy.zeros(np+1)
yp=numpy.zeros(np+1)
fp=numpy.zeros(np+1)
up=numpy.zeros(np+1)
om=numpy.zeros(np+1)
#
# Staring simulation
sim.startSimulation()
id=-1

while True:
    ts = sim.getSimulationTime()
    if ts >= tf:
         break
    id=id+1
    t[id]=ts
    P3DXPos=sim.getObjectPosition(PioneerP3DX,-1)
    P3DXOri=sim.getObjectOrientation(PioneerP3DX,-1)
    xp[id]=P3DXPos[0]
    yp[id]=P3DXPos[1]
    fp[id]=P3DXOri[2]
    if id < np/4:
        Ups=0.4
        Ome=0.0
    elif (id > np/4) & (id < np/2):
        Ups=0.4
        Ome=0.2
    elif (id > np/2) & (id < 3*np/4):
        Ups=0.4
        Ome=0.4
    else:
        Ups=0.0
        Ome=0.0
    
    up[id]=Ups
    om[id]=Ome
    if id < 160:
        leftVel=5
        rightVel=5
    elif id >=160 and id < 190:
        leftVel=0
        rightVel=5
    else:
        leftVel=5
        rightVel=5 
    
    sim.setJointTargetVelocity(leftMotor,leftVel)
    sim.setJointTargetVelocity(rightMotor,rightVel)
    client.step()
sim.stopSimulation()

df = pd.DataFrame({'t':t, 'xp':xp, 'yp':yp, 'fp':fp})
df.to_csv('./test.csv',index=False)
fig,ax=plt.subplots()
ax.axis('equal')
ax.plot(xp,yp,color='blue',linestyle='dashed',linewidth=1)
plt.grid()
plt.title("Top view: robot trajectory")
plt.xlabel("x, m")
plt.ylabel("y, m")
plt.show(block=False)
#
for i in range(0,len(xp)-1,int(round(len(xp)/20))):
    drawRobot(xp[i],yp[i],fp[i],0.01,ax)
#
plt.show()
