import numpy as np
from mpi4py import MPI

data = np.array([1.0, 2.0, 3.0, 4.0])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    comm.send(2 * data, dest=1, tag=11)
    comm.send(3 * data, dest=2, tag=11)
    comm.send(4 * data, dest=3, tag=11)
elif rank in [1, 2, 3]:
    data = comm.recv(source=0, tag=11)

print ("rank = {}  , data = {}\n".format(rank, data))
