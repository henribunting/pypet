__author__ = 'Henri Bunting'

from pypet.tests.testutils.data import TrajectoryComparator
from pypet.tests.testutils.ioutils import make_temp_dir, make_trajectory_name, get_log_config, parse_args, run_suite
from pypet import Environment, load_trajectory
from pypet.brian2.parameter import Brian2Parameter
from brian2.units.stdunits import mvolt, mV, mA, ms, kHz
import numpy as np
from brian2.units.fundamentalunits import Quantity
from pypet.pypetlogging import HasLogger
from pypet.storageservice import HDF5StorageService, StorageService

import os


class Brian2hdf5Test(TrajectoryComparator):

    tags = 'integration', 'brian2', 'parameter', 'hdf5', 'henri'

    def test_hdf5_store_load(self):
        traj_name = make_trajectory_name(self)
        file_name = make_temp_dir(os.path.join('brian2', 'tests', 'hdf5', 'test_%s.hdf5' % traj_name))
        env = Environment(trajectory=traj_name, filename=file_name, log_config=get_log_config(),
                            dynamic_imports=[Brian2Parameter], add_time=False, storage_service=HDF5StorageService)
        traj = env.v_trajectory
        traj.v_standard_parameter = Brian2Parameter
        traj.f_add_parameter('brian2.single.millivolts', 10*mvolt, comment='single value')
        traj.f_add_parameter('brian2.array.millivolts', [11, 12]*mvolt, comment='array')
        traj.f_add_parameter('mV1', 42.0*mV)
        traj.f_add_parameter('ampere1', 1*mA)
        traj.f_add_parameter('integer', 16)
        traj.f_add_parameter('kHz05', 0.5*kHz)
        traj.f_add_parameter('nested_array', np.array([[6.,7.,8.],[9.,10.,11.]]) * ms)
        traj.f_add_parameter('b2a', np.array([1., 2.]) * mV)
        traj.f_store()

        traj2 = load_trajectory(filename=file_name, name=traj_name, dynamic_imports=[Brian2Parameter],
                                load_data=2)
        self.compare_trajectories(traj, traj2)



if __name__ == '__main__':
    opt_args = parse_args()
    run_suite(**opt_args)