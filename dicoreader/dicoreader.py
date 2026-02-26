import numpy as np
from tqdm import tqdm
import gc 
"""
Reading DICOs samples from Siemens twixfile and returns forward and reflected values
Author: Ali Aghaeifar <ali.aghaeifar@tuebingen.mpg.de>
"""

# TerraX_orders = [0, 7, 4, 3, 2, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 16, 17, 20, 19, 18, 21, 22, 23, 24, 25, 28, 27, 26, 29, 30, 31, 32, 33, 36, 35, 34, 37, 38, 39, 40, 41, 44, 43, 42, 45, 46, 47, 48, 49, 52, 51, 50, 53, 54, 55, 56, 57, 60, 59, 58, 61, 62, 63]

def read(twixObj):
    mdb_vop = [mdb for mdb in twixObj[-1]['mdb'] if mdb.is_flag_set('MDH_VOP')]
    # get physical channel 
    channels_ID = [ch_hdr.ChannelId for ch_hdr in mdb_vop[0].channel_hdr]
    channels_max = max(channels_ID) + 1
    # concatenate segments of RFs longer than 1ms
    DICO_comb = []
    
    RFs_lengths = []
    nTx = mdb_vop[0].mdh.UsedChannels
    isTerraX = True if nTx%2 == 1 else False

    # find RFs to allocated memory
    for mdb in tqdm(mdb_vop, desc='Reading DICO'): 
        if mdb.mdh.Counter.Ide == 0:
            RFs_lengths.append(mdb.mdh.SamplesInScan)
        else:
            RFs_lengths[-1] = RFs_lengths[-1] + mdb.mdh.SamplesInScan
    RF_unique_lengths, counts = np.unique(RFs_lengths, return_counts=True)
    print(RF_unique_lengths, '\n', counts, '\n', len(RFs_lengths), nTx, channels_max, '\n', channels_ID)

    DICO = dict()
    RFs_counter = dict()
    for l, c in zip(RF_unique_lengths, counts):
        DICO[l] = np.zeros((nTx, l, c), dtype=mdb_vop[0].data.dtype)
        RFs_counter[l] = 0

    # read DiCo samples
    counter = 0
    for mdb in tqdm(mdb_vop, desc='Reading DICO'): 
        if mdb.mdh.Counter.Ide == 0:
            data = np.empty((nTx, 0))
            current_length = 0
        current_length += mdb.mdh.SamplesInScan
        data = np.concatenate((data, mdb.data), axis=1)
        if(RFs_lengths[counter] == current_length):
            DICO[current_length][:,:,RFs_counter[current_length]] = data
            RFs_counter[current_length] += 1
            counter += 1

    # if TerraX, reorder the RFs
    if isTerraX:
        # remove TAS
        TAS_index = channels_ID.index(7)
        TerraX2Terra = [0,2,1,3,4,6,5,7,8,10,9,11,12,14,13,15,16,18,17,19,20,22,21,23,24,26,25,27,28,30,29,31]
        for key in DICO:
            print(f'removing TAS from MDB channel {TAS_index}')
            DICO[key] = np.delete(DICO[key], TAS_index, axis=0) 
            DICO[key] = DICO[key][TerraX2Terra[:nTx-1], ...]

    forward, reflect = dict(), dict()
    for key, value  in DICO.items():
        forward[key] = value[::2, ...]
        reflect[key] = value[1::2, ...]
        
    return forward, reflect
