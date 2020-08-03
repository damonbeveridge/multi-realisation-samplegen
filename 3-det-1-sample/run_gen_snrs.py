"""
This script runs the `generate_sample.py` script in a loop to generate
multiple files (each file has it's own injection sample and corresponding
noise realisations as well as a number of pure noise samples) to make the
process of generating  large datasets very 'hands-off'. The script also
makes sure that each sample/noise across all files is defined by separate
seeds to ensure no repeats.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

import argparse
import os
import sys

from functools import wraps
from traceback import print_exc

from generate_snr_series import three_det_main

# -----------------------------------------------------------------------------
# Suppress Broken Pipe Messages
# -----------------------------------------------------------------------------

def suppress_broken_pipe_msg(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SystemExit:
            raise
        except:
            print_exc()
            sys.exit(1)
        finally:
            try:
                sys.stdout.flush()
            finally:
                try:
                    sys.stdout.close()
                finally:
                    try:
                        sys.stderr.flush()
                    finally:
                        sys.stderr.close()
    return wrapper

# -----------------------------------------------------------------------------
# MAIN CODE
# -----------------------------------------------------------------------------

@suppress_broken_pipe_msg
def main():

    # Disable output buffering ('flush' option is not available for Python 2)
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)

    # -------------------------------------------------------------------------
    # Parse the command line arguments
    # -------------------------------------------------------------------------

    # Set up the parser and add arguments
    parser = argparse.ArgumentParser(description='Generate a GW data sample.')
    parser.add_argument('--config-file',
                        help='Name of the JSON configuration file which '
                             'controls the sample generation process.',
                        default='default.json')
    parser.add_argument('--sample-files',
                        help='Name of a directory containing '
                             'the entire set of sample files.',
                        default='./output/snr10to20/')
    parser.add_argument('--template-file',
                        help='Name of a directory containing '
                             'the entire set of sample files.',
                        default='./output/templates.hdf')

    # Parse the arguments that were passed when calling this script
    print('Parsing command line arguments...')
    command_line_arguments = vars(parser.parse_args())
    print('Done!')

    # Define how many injections (# of files) you want to be generated
    sample_files_path = str(command_line_arguments['sample_files'])

    # -------------------------------------------------------------------------
    # Read in JSON config file specifying the sample generation process
    # -------------------------------------------------------------------------

    json_config_name = command_line_arguments['config_file']
    json_config_path = os.path.join('.', 'config_files', json_config_name)

    # Make sure the config file actually exists
    if not os.path.exists(json_config_path):
        raise IOError('Specified configuration file does not exist: '
                      '{}'.format(json_config_path))

    # -------------------------------------------------------------------------
    # Get list of sample files to compute SNR series for
    # -------------------------------------------------------------------------

    file_list = sorted(os.listdir(sample_files_path))
    file_list_2 = [x for x in file_list if "samples" in x]
    print(file_list_2)

    # -------------------------------------------------------------------------
    # Generate Samples
    # -------------------------------------------------------------------------

    # Seeds start from 0 and control file names
    for file in file_list_2:
        num = file[7:-14]
        print(num)
        snr_range = file[-13:-4]
        output_file_name = 'snrs' + num + '_' + snr_range + '.hdf'

        if os.path.exists(os.path.join(sample_files_path,output_file_name)):
            print(os.path.join(sample_files_path,output_file_name))
        else:
            three_det_main(file, 'templates.hdf', output_file_name, snr_range)



if __name__ == '__main__':

    main()

    exit()
