from __future__ import print_function

import mdtraj as md

import pytest
import os
import shutil
import tarfile
import tempfile
from fahmunge import fah

# TODO: Add unit tests for components of the code.

def test_dummy():
    """Dummy test to ensure py.test doesn't exist with error code 5."""
    pass

def deprecated_test_fah_core17_1():
    from mdtraj.utils import six
    from mdtraj.testing import get_fn, eq
    filename = get_fn('frame0.xtc')
    tempdir = tempfile.mkdtemp()
    tar_filename = os.path.join(tempdir, "results-000.tar.bz2")
    archive = tarfile.open(tar_filename, mode='w:bz2')

    tar = tarfile.open(tar_filename, "w:bz2")
    tar.add(filename, arcname="positions.xtc")
    tar.close()

    shutil.copy(tar_filename, os.path.join(tempdir, "results-001.tar.bz2"))

    trj0 = md.load(get_fn("frame0.xtc"), top=get_fn("frame0.h5"))
    output_filename = os.path.join(tempdir, "traj.h5")
    fah.concatenate_core17(tempdir, trj0, output_filename)

    trj = md.load(output_filename)
    eq(trj.n_atoms, trj0.n_atoms)
    eq(trj.n_frames, trj0.n_frames * 2)

    shutil.copy(tar_filename, os.path.join(tempdir, "results-002.tar.bz2"))

    fah.concatenate_core17(tempdir, trj0, output_filename)
    # Should notice the new file and append it to the HDF file.

    trj = md.load(output_filename)
    eq(trj.n_atoms, trj0.n_atoms)
    eq(trj.n_frames, trj0.n_frames * 3)
