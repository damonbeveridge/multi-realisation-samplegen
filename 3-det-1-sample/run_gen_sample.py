"""
This script runs the `generate_sample.py` script in a loop to generate multiple
files (each file has it's own injection sample and corresponding noise realisations
as well as a number of pure noise samples) to make the process of generating large
datasets very 'hands-off'. The script also makes sure that each sample/noise across
all files is defined by separate seeds to ensure no repeats.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

import argparse
import os
import json

from generate_sample import three_det_main

# -----------------------------------------------------------------------------
# MAIN CODE
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    # -------------------------------------------------------------------------
    # Parse the command line arguments
    # -------------------------------------------------------------------------

    # Set up the parser and add arguments
    parser = argparse.ArgumentParser(description='Generate a GW data sample.')
    parser.add_argument('--config-file',
                        help='Name of the JSON configuration file which '
                             'controls the sample generation process.',
                        default='default.json')
    parser.add_argument('--num-injections',
                        help='Number of injeciton samples (files) to '
                             'generate.',
                        default=3)

    # Parse the arguments that were passed when calling this script
    print('Parsing command line arguments...')
    command_line_arguments = vars(parser.parse_args())
    print('Done!')

    # Define how many injections (# of files) you want to be generated
    n_injections = int(command_line_arguments['num_injections'])

    # -------------------------------------------------------------------------
    # Read in JSON config file specifying the sample generation process
    # -------------------------------------------------------------------------

    json_config_name = command_line_arguments['config_file']
    json_config_path = os.path.join('.', 'config_files', json_config_name)

    # Make sure the config file actually exists
    if not os.path.exists(json_config_path):
        raise IOError('Specified configuration file does not exist: '
                      '{}'.format(json_config_path))

    # Open the config while and load the JSON contents as a dict
    with open(json_config_path, 'r') as json_file:
        pre_config = json.load(json_file)

    # -------------------------------------------------------------------------
    # Get list of sample files already generated
    # -------------------------------------------------------------------------

    snr_range = 'snr10to20'

    sample_files_path = './output/' + snr_range + '/'
    nums=[]

    file_list = sorted(os.listdir(sample_files_path))
    file_list_2 = [x for x in file_list if "samples" in x]
    print(file_list_2)

    for i in file_list_2:
        start = i.index('samples') + len('samples')
        end = i.index('_snr')
        nums.append(int(i[start:end]))
        nums = sorted(nums)

    # -------------------------------------------------------------------------
    # Generate Samples
    # -------------------------------------------------------------------------

    # Generating from scratch
    if len(nums) == 0:

        # Seeds start from 0
        for random_seed in range(n_injections):
            noise_random_seed = random_seed + n_injections
            output_file_name = './' + snr_range + '/samples' + str(random_seed) + '_' + snr_range + '.hdf'

            three_det_main(random_seed, noise_random_seed, output_file_name)

    # Generating from last file
    else:

        # Seeds start from 1 above highest filename
        for random_seed in range(n_injections):
            noise_random_seed = nums[-1] + random_seed + n_injections
            output_file_name = './' + snr_range + '/samples' + str(nums[-1] + random_seed) + '_' + snr_range + '.hdf'

            three_det_main(random_seed, noise_random_seed, output_file_name)



    exit()