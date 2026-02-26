# DiCoReader

Script used to extract directional coupler (DiCo) values from Siemens twix rawdata format.

### Installation & Requirements:
The tool is tested under Python 3.12 with the following packages installed:

 - numpy
 - tqdm
 - twixtools ([+](https://github.com/pehses/twixtools))

Clone the reposidoty, then navigate to the dicoreader folder in the terminal and install with pip:

    pip install .

### Usage:

```python
import twixtools
import dicoreader

twixfile = 'path to twix file'
twixObj  =  twixtools.read_twix(filepath)
forward, reflect = dicoreader.read(twixObj)

print("Size of forward and reflect (Cha, Samples, RF No.):")
for i, (f, r) in enumerate(zip(forward, reflect)):
    print(f"RF Pulse Type {i}:", forward[f].shape, reflect[r].shape)
```
`forward` and `reflect` are dict of NumPy arrays, where each array represents a distinct RF object. All RF arrays of the same length are assumed to belong to the same RF object. 


### Citation:
Please refer to the following publication for citation of this work:

https://doi.org/10.1002/mrm.30078
