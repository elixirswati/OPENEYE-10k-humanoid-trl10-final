class ServoSim:
 def __init__(self,*a,**k): self.pan=0; self.tilt=0
 def command(self,pan_deg,tilt_deg,dt=0.02): self.pan=pan_deg; self.tilt=tilt_deg
 def pose(self): return {'pan_deg':self.pan,'tilt_deg':self.tilt}
