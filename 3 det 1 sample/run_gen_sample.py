import os
import json

from generate_sample import three_det_main

if __name__ == '__main__':

    n_injections = 2

    # Make sure the config file actually exists
    if not os.path.exists('./config_files/default.json'):
        raise IOError('Specified configuration file does not exist: '
                      '{}'.format('./config_files/default.json'))

    # Open the config while and load the JSON contents as a dict
    with open('./config_files/default.json', 'r') as json_file:
        pre_config = json.load(json_file)



    for random_seed in range(n_injections):
        noise_random_seed = random_seed + n_injections
        output_file_name = './snr30to50/samples' + str(random_seed) + '_snr30to50.hdf'

        three_det_main(random_seed, noise_random_seed, output_file_name)



    exit()