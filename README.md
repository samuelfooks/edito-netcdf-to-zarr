# edito-netcdf-to-zarr
NetCDF to zarr process for EDITO Process Catalog

This Repo shows the components used to make the NetCDF to Zarr process available to convert NetCDFs directly to zarr in the EDITO Infra Process Catalog.  
Ideploys a containerized application that converts NetCDF files to Zarr format. The application is built using Python and leverages libraries such as xarray, zarr, dask, and numpy.


Application
The application (netcdf_to_zarr.py) takes a URL to a NetCDF file as an argument. It downloads the file, opens it as an xarray dataset, and renames 'lat' and 'lon' variables to 'latitude' and 'longitude' if they exist. The dataset is then chunked based on the latitude and longitude dimensions. The chunked dataset is converted to Zarr format and stored in the path specified by ARCO_ASSET_TEMP_DIR.

Usage
Here are the Helm charts and yaml files used to deploy this process on the EDITO Infra Process Catalog

License:
CC BY-4.0

