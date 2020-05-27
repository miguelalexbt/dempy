![](assets/logo.png)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)  
A package that simplifies access and management of datasets and their annotations.

## Getting started

### Documentation
* Check out our fancy [Documentation](https://miguelalexbt.github.io/dempy/)

### Install

* Clone this repository
* Within the dempy folder run:  
```python setup.py install```
* You can now delete the cloned folder

### Uninstall
* To uninstall just run:  
```pip3 uninstall dempy```

## Code Example
```python
# Example of how to make operations only on videos
# with the mp4 extension of a specific dataset and acquisition

import dempy

dataset = dempy.datasets.get("123")
acq = dataset.acquisitions.get("456")
video_samples = acq.video_samples.get()
dev_videos = video_samples.by_device("789")

mp4_video_samples = [vs for vs in dev_videos if vs.media_type == "video/mp4"]

for v in mp4_video_samples:
    # Manipulate these videos

# Clear cache
dempy.cache.clear()
```

## Work developed by:
* Miguel Teixeira - up201605150@fe.up.pt
* Pedro Pinho - up201605166@fe.up.pt
* Ricardo Moura - up201604912@fe.up.pt
