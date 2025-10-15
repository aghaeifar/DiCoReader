import numpy as np
from tqdm.auto import tqdm

"""
Reading DICOs samples from Siemens twixfile and returns forward and reflected values
Author: Ali Aghaeifar <ali.aghaeifar@tuebingen.mpg.de>
"""

TerraX_orders = [0, 7, 4, 3, 2, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 16, 17, 20, 19, 18, 21, 22, 23, 24, 25, 28, 27, 26, 29, 30, 31, 32, 33, 36, 35, 34, 37, 38, 39, 40, 41, 44, 43, 42, 45, 46, 47, 48, 49, 52, 51, 50, 53, 54, 55, 56, 57, 60, 59, 58, 61, 62, 63]

def read(twixObj, isTerraX = False, integral = False):
    mdb_vop = [mdb for mdb in twixObj[-1]['mdb'] if mdb.is_flag_set('MDH_VOP')]
    # get physical channel 
    channels_ID = [ch_hdr.ChannelId for ch_hdr in mdb_vop[0].channel_hdr]
    channels_max = max(channels_ID) + 1
    # concatenate segments of RFs longer than 1ms
    DICO_comb = []
    RF_lengths = []
    for mdb in tqdm(mdb_vop, desc='Reading DICO'):   
        data = mdb.data 
        # integral over samples
        if integral:
            data = np.sum(np.abs(data), axis=1, keepdims=True)
        # unsqueeze data 
        unsqueezed_data = np.zeros((channels_max, data.shape[1]), dtype=data.dtype)
        unsqueezed_data[channels_ID, :] = data
        # concatenate if length is longer than 1ms
        if mdb.mdh.Counter.Ide == 0:
            DICO_comb.append(unsqueezed_data)
            RF_lengths.append(mdb.data.shape[1])
        else:
            RF_lengths[-1] = RF_lengths[-1] + mdb.data.shape[1]
            if integral:
                DICO_comb[-1] = DICO_comb[-1] + unsqueezed_data
            else:
                DICO_comb[-1] = np.concatenate((DICO_comb[-1], unsqueezed_data), axis=1)

    # separate different RF pulses if there are more than one RF pulse
    DICO = []
    RF_lengths_unq = sorted(set(RF_lengths), key=RF_lengths.index)  # unique shapes
    print(f'Found {len(RF_lengths_unq)} different RF pulses with lengths: {RF_lengths_unq}')
    
    for i, RF_length in enumerate(RF_lengths_unq):
        temp = [dico for j, dico in enumerate(tqdm(DICO_comb, desc=f'RF Pulse {i}')) if RF_lengths[j] == RF_length]
        DICO.append(np.stack(temp, axis=-1))

    if integral and isTerraX:
        DICO = [dico / rf_len for dico, rf_len in zip(DICO, RF_lengths_unq)]  # mean signal -> voltage
        
    # if TerraX, reorder the RFs
    if isTerraX:
        TerraX_orders_limitted = TerraX_orders[:channels_max]
        DICO = [dico[TerraX_orders_limitted, :, :] for dico in DICO]
        
    # split forward and reflected RFs
    forward = [dico_frw[::4] for dico_frw in DICO]
    reflect = [dico_rfl[2::4] for dico_rfl in DICO]

    return forward, reflect
