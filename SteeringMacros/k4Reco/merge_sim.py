import pyLCIO
from pyLCIO import IOIMPL

writer = IOIMPL.LCFactory.getInstance().createLCWriter()
writer.open("/scratch/jwatts/mucol/v2.11/sim/pions_0_50/pions_0_50_sim_merged.slcio", pyLCIO.EVENT.LCIO.WRITE_NEW)

reader = IOIMPL.LCFactory.getInstance().createLCReader()
for i in range(100):
    reader.open(f"/scratch/jwatts/mucol/v2.11/sim/pions_0_50/pion_0_50_{i}.slcio")
    for event in reader:
        writer.writeEvent(event)
    reader.close()

writer.close()
print("Done")
