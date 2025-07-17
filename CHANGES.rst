CHANGES
=======

Version 0.4.0 (2025-07-17)
--------------------------
- Fix bug in single phenometric calculation by replacing geojson parameter with ts_list  
- Add new phenometrics_data_cube function for  calculate phenological metrics from Xarray  
- Rename calc_phenometrics_cube to calc_phenometrics_multi for clearer functionality distinction  

Version 0.3.0 (2025-04-03)
--------------------------

- Add `max-requests` 256 - Configured maximum concurrent requests limit to optimize server
- Add `timeout` 30 - Implemented 30-second timeout threshold for all requests
- Add function `wcpms_get_timeseries_region` - returning time series in list format for pixel centers within a given region using WTSS and satellite time series
- Fixed CORS headers  Resolved cross-origin issues by  'Access-Control-Allow-Headers' `Origin, X-Requested-With`
- Remove region methods from `get_phenometrics_region` - Now only use wtss to get all pixel centers within a given region
- Refactored `get_timeseries_region` function - Completely rebuilt the core function to Enhance performance.


Version 0.2.0 (2025-02-24)
--------------------------

- Revisar Dockerfile para uso do gunicorn ao inves do Flask (#2)
- Correção nos cabeçalhos CORS do serviço
- Mapeamento de parametros na função de filtro


Version 0.1.0 (2024-11-05)
--------------------------

- Add initial commit supporting Phenology metrics with the following features: `list_collections`, `get_description`, `get_phenometrics` and `get_phenometrics_region`
- Add Docker support
- License GPL v3
