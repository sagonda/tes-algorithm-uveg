# TES_UVEG_MOD (This product is based on MODIS products MOD021KM(Level 1B Calibrated Radiances), MOD03(Geolocation Fields 5-Min L1A Swath 1km) and MOD35_L2(Cloud Mask) from TERRA satellite).

# Description
The TES_UVEG_MOD land surface temperature and emissivity (LST&E) product is a product created by the Global Change Unit of the Image Processing Laboratory of the University of Valencia. To obtain the temperature and emissivity, a physics-based TES algorithm is used, based on MODIS thermal infrared bands 29, 31 and 32.


# Collection, Granule and Layers
## Collection
| Characteristic        | Description |
|----------------       |-------------|
|Collection	            |TES_UVEG_MOD_V.1
|DOI	                |
|File Size	            |~5 MB
|Temporal Resolution	|Daily
|Temporal Extent	    |2002-07-01 TO 2022
|Spatial Extent	        |Global
|Coordinate System	    |None (Swath)
|Datum	                |N/A
|File Format	        |netCDF4
|Geographic Dimensions	|2300 km x 2300 km

## Granule
|Characteristic	                 |Description                        |
|--------------------------------|-----------------------------------|
|Number of Science Dataset (SDS) |Layers	11                       |
|Columns/Rows	                 |Varies by scene (2030/2040 x 1354) |
|Pixel Size	                     |1000 m                             |

## Layers
| SDS Name         | Description                                      | Units    | Data Type                 | Fill Value   | No Data Value     | Valid Range        | Scale Factor | Offset|
| -----------      | ------------------------------------------------ | -------- | ------------------------- | -----------  | -----------       | -----------        | -----------  | ------|
|UVEG_LST          | Land surface temperature	                      |  Kelvin	 | 16-bit unsigned integer	 | 0	        | N/A	            | 1 to 65535	     | 0.02	        | N/A   |
|UVEG_e29	       | Band 29 emissivity	                              |  N/A	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.002	    | 0.49  |
|UVEG_e31	       | Band 31 emissivity	                              |  N/A	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.002	    | 0.49  |
|UVEG_e32	       | Band 32 emissivity	                              |  N/A	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.002	    | 0.49  |
|UVEG_LST_error	   | Land surface temperature error	                  |  Kelvin	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.04	        | N/A   |
|UVEG_e29_error    | Band 29 emissivity error	                      |  N/A	 | 16-bit unsigned integer	 | 0	        | N/A	            | 1 to 65535	     | 0.0001	    | N/A   |
|UVEG_e31_error    | Band 31 emissivity error	                      |  N/A	 | 16-bit unsigned integer	 | 0	        | N/A	            | 1 to 65535	     | 0.0001	    | N/A   |
|UVEG_e32_error    | Band 32 emissivity error	                      |  N/A	 | 16-bit unsigned integer	 | 0	        | N/A	            | 1 to 65535	     | 0.0001	    | N/A   |
|View_angle	       | MODIS view angle for current pixel	              |  Degree	 | 8-bit unsigned integer	 | 0	        | N/A	            | 0 to 180	         | 0.5	        | N/A   |
|lat	           | Pixel latitude	                                  |  Degree	 | 32-bit integer        	 | 0	        | N/A	            | 1 to 4294967293	 | 10.000	    | N/A   |
|lon	           | Pixel longitude	                              |  Degree	 | 32-bit integer       	 | 0     	    | N/A	            | 1 to 4294967293	 | 10.000	    | N/A   |

# Contact
If you have any questions about the product, please contact:
jose.sobrino@uv.es
daniel.salinas@uv.es
