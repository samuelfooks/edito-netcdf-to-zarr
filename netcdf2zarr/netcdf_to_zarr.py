import os
import sys
import xarray as xr
import zarr
import dask.array as da
import numpy as np

def get_filename_from_url(url):
    # Split the URL by '/'
    parts = url.split('/')
    # The last part after the last '/' should be the filename
    filename = parts[-1]
    return filename

def convert_nc_2_zarr(netcdf_url, arco_asset_temp_dir, metadata_dict):
    # Extract filename from URL
    filename = get_filename_from_url(netcdf_url)
     # Download the NetCDF file
    os.system(f"wget -O {filename} {netcdf_url}")
    

    title = os.path.splitext(os.path.basename(filename))[0]
    
    #use xarrays lazy dask chunking to determine chunk sizes
    dataset = xr.open_dataset(filename, engine = 'netcdf4', chunks='auto')

    # Check if 'lat' and 'lon' variables exist and rename them to 'latitude' and 'longitude'
    if 'lat' in dataset.variables:
        dataset = dataset.rename({'lat': 'latitude'})
    if 'lon' in dataset.variables:
        dataset = dataset.rename({'lon': 'longitude'})


    ##chunking options
     # Unify chunks along the time dimension
    dataset = dataset.unify_chunks()
    # Print the auto-determined chunksizes
    print("Auto-determined chunksizes:", dataset.chunksizes)
    
    # Determine chunk sizes based on latitude and longitude dimensions
    chunk_sizes = {dim: len(dataset[dim]) for dim in ['latitude', 'longitude']}
    
    # Chunk the dataset
    dataset = dataset.chunk(chunk_sizes)
    
    # Print the new chunksizes after chunking
    print("Chunked chunksizes:", dataset.chunksizes)
    
    # Store chunking dimensions in dataset attributes
    dataset.attrs['chunking_dimensions'] = list(chunk_sizes.keys())

    arco_temp_path = f"{arco_asset_temp_dir}/{title}.zarr"
    
    ##options to determine compression type
    # compressor = zarr.Blosc(cname='zstd', clevel=5)
    # encoding = {vname: {'compressor': compressor} for vname in ds.data_vars}

    zarr = dataset.to_zarr(store=arco_temp_path, mode = 'w')
    print(f'zarr made at {arco_temp_path}')

    return arco_temp_path, dataset

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python netcdf_to_zarr.py <URL>")
        sys.exit(1)
    
    netcdf_url = sys.argv[1]
    arco_asset_temp_dir = os.environ.get("ARCO_ASSET_TEMP_DIR")
    metadata_dict = {}  # Add metadata if needed
    
    convert_nc_2_zarr(netcdf_url, arco_asset_temp_dir, metadata_dict)