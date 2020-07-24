"""
Plot the results produced by the generate_sample.py script.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

from __future__ import print_function

import argparse
import numpy as np
import h5py
import os
import sys
import time

from utils.samplefiles import SampleFile

# We need to load a different backend for matplotlib before import plt to
# avoid problems on environments where the $DISPLAY variable is not set.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa


# -----------------------------------------------------------------------------
# MAIN CODE
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    file = h5py.File('./output/default_snrs1.hdf', 'r')

    plt.plot(np.copy(file['omf_injection_snr_samples']['h1_snr']['0']))
    plt.savefig('./1snr_plot0.pdf', bbox_inches='tight', pad_inches=0.1)