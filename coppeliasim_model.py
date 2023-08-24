import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# coppeliaSim
import pandas as pd
import timeit, numpy, scipy


def coppeliasim_model(rightVel, leftVel):
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
    print(dt)

    objectName='/PioneerP3DX'
    rightMotor=sim.getObject('/PioneerP3DX/rightMotor')
    leftMotor=sim.getObject('/PioneerP3DX/leftMotor')
    PioneerP3DX=sim.getObject('/PioneerP3DX')
    #
    objectPosition=sim.getObjectPosition(PioneerP3DX,-1)
    objectOrientation=sim.getObjectOrientation(PioneerP3DX,-1)
    objectQuaternion=sim.getObjectQuaternion(PioneerP3DX,-1)
    client.setStepping(True)
    np = rightVel.size
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

        
        sim.setJointTargetVelocity(leftMotor,leftVel[id])
        sim.setJointTargetVelocity(rightMotor,rightVel[id])
        client.step()
    sim.stopSimulation()
    df = pd.DataFrame({'t':t, 'xp':xp, 'yp':yp, 'fp':fp})
    df = df.drop(np) 
    return df