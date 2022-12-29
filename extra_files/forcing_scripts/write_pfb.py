#%%
from parflowio.pyParflowio import PFData

def writeoutpfb(towrite,outname):
    test = PFData()
    # data = np.random.random_sample((50, 49, 31))
    test.setDataArray(towrite)        
    test.setDX(1)
    test.setDY(1)
    test.setDZ(1)
    test.setX(0)
    test.setY(0)
    test.setZ(0)
    test.setP(1)
    test.setQ(1)
    test.setR(1)
    test.writeFile((outname))
