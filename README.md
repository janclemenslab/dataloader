# dataloader
Data - raw data, analysis results - is organized in a specified folder structure on the lab volume, one folder per experiment. `dataloader` simplifies loading data.

## Installation
```
pip install git+http://github.com/janclemenslab/dataloader
```

## Usage
Import and initialize `dataloader`:

```python
from dataloader import DataLoader
root_dir = '/Volumes/ukme04/#Common/chainingmic'
dl = DataLoader(root_dir)
```
 This will load a [default config file][1], which contains information about where to find a specific data type for each experiment, and how to load it. Currently, the following data types are supported:
- `video` (returns [videoreader](https://github.com/postpop/videoreader))
- `tracks` (returns a dictionary, read with [deepdish][2])
- `poses` (returns a dictionary, read with [deepdish][2])
- `timestamps` (todo)
- `daq` (todo)
- `segmentedsong` (todo)

The only required argument is the `root_dir`, the path that points to the `chainingmic` folder.

Data files from a specific experiment can be loaded using `get`:
```python
expt_id = 'localhost-20180618_151056'
vr = dl.get('video', expt_id)
tracks = dl.get('tracks', expt_id)
poses = dl.get('poses', expt_id)
```

## Customization
The config file describes where each type of data is found on the lab volume and how to read it. While the [default config file][1] supports all common data types, `dataloader` can be initialized with a custom config file via: `DataLoader(root_dir, custom_config_file_name)`. Config files are written in [yaml](https://pyyaml.org/wiki/PyYAMLDocumentation) and contain two sections: `types` and `loaders`.

### File types
`types` defines all data types. Definitions must contain
- the base folder relative to `root_dir`,
- the suffix.

The file path is constructed from the folder, the experiment ID, and the suffix as `root_dir/folder/ID/IDsuffix`. Folder and suffix can be lists.

Optionally, a `loader` can be specified (any of the sections defined in `loaders`, see next paragraph). Be default, the loader is inferred from the suffix.

```yaml
types:
    poses:
      folder: res
      suffix: _poses.h5
      loader: hdf5
    video:
      folder: [dat, dat.processed]
      suffix: .mp4
      loader: video
    tracks:
      folder: res
      suffix: [_tracks_fixed.h5, _tracks.h5]
      loader: hdf5
    poses_tsne:
      folder: res
      suffix: _tsne.h5
      loader: hdf5
```
### File loaders
`loaders` defines how different file types are read. Definitions contain
- `extensions`: Used to match file names with loaders if not explicitly specified in the types definition. Based on the filenames ending in any of the extensions. Can be a list.
- `module`: automatically imported
- `function`: function in `module` to use a loader.
- `args`, `kwargs`: Optional arguments to be passed to the function.

This information is used load the data, by creating a command that roughly looks like this: `module.function(filepath, *args, **kwargs).

```yaml
loaders:
    hdf5:
        extensions: [h5, hdf, hdf5]
        module: deepdish
        function: io.load
    video:
        extensions: [mp4, avi]
        module: videoreader
        function: VideoReader
    npy:
        extensions: [npy, npz]
        module: numpy
        function: load
    csv:
        extensions: [csv]
        module: pandas
        function: from_csv
        # args: [arguments]
        # kwargs: {Delimiter: \t}
```


[1]: http://github.com/janclemenslab/dataloader/blob/master/src/dataloader/config/default.yaml
[2]: https://github.com/uchicago-cs/deepdish
