# TES-UVEG (PRODUCT MODIS MOD21)

Description
The MYD21 Land Surface Temperature and Emissivity (LST&E) swath data product is produced daily in five minute temporal increments of satellite acquisition. The swath is approximately 2,030 pixels along track and 1,354 pixels per line, at a nadir resolution of 1,000 meters. The MYD21 Land Surface Temperature (LST) algorithm differs from the MYD11 algorithm in that the MYD21 LST algorithm is based on the ASTER Temperature/Emissivity Separation (TES) technique, whereas the MYD11 uses the split-window technique. The MYD21 TES algorithm uses a physics-based algorithm to dynamically retrieve both LST and spectral emissivity simultaneously from the MODIS thermal infrared bands 29, 31, and 32. The TES algorithm is combined with an improved Water Vapor Scaling (WVS) atmospheric correction scheme to stabilize the retrieval during very warm and humid conditions. MYD21 products are available two months after acquisition due to latency of data inputs. Additional details regarding the method used to create this Level 2 (L2) product are available in the Algorithm Theoretical Basis Document (ATBD).

Characteristics
Product Maturity
Validation at stage 1 has been achieved for the MODIS Land Surface Temperature and Emissivity data products. Further details regarding MODIS land product validation for the MYD21 data products are available from the MODIS Land Team Validation site.

Collection and Granule

## Collection
| Characteristic        | Description |
|----------------       |-------------|
|Collection	            |TES_UVEG_MOD21_V.1
|DOI	                |
|File Size	            |~5 MB
|Temporal Resolution	|Daily
|Temporal Extent	    |2002-07-01 to Present
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
| SDS Name     | Description                                      | Units    | Data Type                 | Fill Value   | No Data Value     | Valid Range        | Scale Factor | Offset|
| -----------  | ------------------------------------------------ | -------- | ------------------------- | -----------  | -----------       | -----------        | -----------  | ------|
|LST           | Land surface temperature	                      |  Kelvin	 | 16-bit unsigned integer	 | 0	        | N/A	            | 7500 to 65535	     | 0.02	        | N/A   |
|Emis_29	   | Band 29 emissivity	                              |  N/A	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.002	    | 0.49  |
|Emis_31	   | Band 31 emissivity	                              |  N/A	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.002	    | 0.49  |
|Emis_32	   | Band 32 emissivity	                              |  N/A	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.002	    | 0.49  |
|LST_err	   | Land surface temperature error	                  |  Kelvin	 | 8-bit unsigned integer	 | 0	        | N/A	            | 1 to 255	         | 0.04	        | N/A   |
|Emis_29_err   | Band 29 emissivity error	                      |  N/A	 | 16-bit unsigned integer	 | 0	        | N/A	            | 1 to 65535	     | 0.0001	    | N/A   |
|Emis_31_err   | Band 31 emissivity error	                      |  N/A	 | 16-bit unsigned integer	 | 0	        | N/A	            | 1 to 65535	     | 0.0001	    | N/A   |
|Emis_32_er    | Band 32 emissivity error	                      |  N/A	 | 16-bit unsigned integer	 | 0	        | N/A	            | 1 to 65535	     | 0.0001	    | N/A   |
|View_angle	   | MODIS view angle for current pixel	              |  Degree	 | 8-bit unsigned integer	 | N/A	        | N/A	            | 0 to 180	         | 0.5	        | N/A   |
|Latitude	   | Pixel latitude	                                  |  Degree	 | 32-bit floating point	 | 999.99	    | N/A	            | -90 to 90	         | N/A	        | N/A   |
|Longitude	   | Pixel longitude	                              |  Degree	 | 32-bit floating point	 | 999.99	    | N/A	            | -180 to 180	     | N/A	        | N/A   |

Ocean-land mask Classes
Value	Description
0	Land
1	Water
Product Quality
The Quality Control (QC) layer is stored in an efficient bit-encoded manner. The unpack_sds_bits executable from the LDOPE Tools is available to the user community to help parse and interpret the quality layer.

Quality assurance information should be considered when determining the usability of data for a particular science application. The ArcGIS MODIS-VIIRS Python Toolbox contains tools capable of decoding quality data layers while producing thematic quality raster files for each quality attribute.

The bit definition index for the quality layer is available in the User Guide on page 18.

Known Issues
Users of MODIS LST products may notice an increase in occurrences of extreme high temperature outliers in the unfiltered MxD21 Version 6 and 6.1 products compared to the heritage MxD11 LST products. This can occur especially over desert regions like the Sahara where undetected cloud and dust can negatively impact both the MxD21 and MxD11 retrieval algorithms.

In the MxD11 LST products, these contaminated pixels are flagged in the algorithm and set to fill values in the output products based on differences in the band 32 and band 31 radiances used in the generalized split window algorithm. In the MxD21 LST products, values for the contaminated pixels are retained in the output products (and may result in overestimated temperatures), and users need to apply Quality Control (QC) filtering and other error analyses for filtering out bad values. High temperature outlier thresholds are not employed in MxD21 since it would potentially remove naturally occurring hot surface targets such as fires and lava flows.

High atmospheric aerosol optical depth (AOD) caused by vast dust outbreaks in the Sahara and other deserts highlighted in the example documentation are the primary reason for high outlier surface temperature values (and corresponding low emissivity values) in the MxD21 LST products. Future versions of the MxD21 product will include a dust flag from the MODIS aerosol product and/or brightness temperature look up tables to filter out contaminated dust pixels. It should be noted that in the MxD11B day/night algorithm products, more advanced cloud filtering is employed in the multi-day products based on a temporal analysis of historical LST over cloudy areas. This may result in more stringent filtering of dust contaminated pixels in these products.

In order to mitigate the impact of dust in the MxD21 V6 and 6.1 products, the science team recommends using a combination of the existing QC bits, emissivity values, and estimated product errors, to confidently remove bad pixels from analysis. For more details, refer to this dust and cloud contamination example documentation.

For complete information about the MOD21 known issues please refer to the MODIS Land Quality Assessment website.