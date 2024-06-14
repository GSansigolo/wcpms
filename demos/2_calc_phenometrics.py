from wcpms import calc_phenometrics, params_phenometrics, wcpms_array, smooth_timeseries

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1
)

print(config)

evi_array = wcpms_array(
    timeserie=smooth_timeseries([5034.0, 1538.0, 4338.0, 4715.0, 4769.0, 3495.0, 4337.0, 3555.0, 4258.0, 3299.0, 3375.0, 3490.0, 3179.0, 3331.0, 2852.0, 3134.0, 1590.0, 1688.0, 3547.0, 5257.0, 4596.0, 6000.0, 3755.0, 1817.0, 2979.0, 6064.0, 6210.0, 4429.0, 4625.0, 2731.0, 4075.0, 1682.0, 3635.0, 3359.0, 3489.0, 3416.0, 3405.0, 3063.0, 3030.0, 2936.0, 1476.0, 2909.0, 3384.0, 3722.0, 4163.0, 2343.0, 4719.0, 5323.0, 2797.0, 3587.0, 4674.0, 3902.0, 3163.0, 4350.0, 3783.0, 3309.0, 3382.0, 3330.0, 3296.0, 3451.0, 3149.0, 3312.0, 2975.0, 4569.0, 4707.0, 4348.0, 3561.0, 3015.0, 133.0, 4642.0, 4549.0, 5955.0, 4680.0, 4523.0, 5017.0, 4358.0, 3742.0, 3729.0, 3329.0, 3229.0, 3133.0, 3131.0, 2923.0, 2809.0, 2885.0, 2939.0, 3569.0], method='savitsky'),
    start_date='2021-01-01',
    freq='16D'
)

print(evi_array)

ds_phenos = calc_phenometrics(
    da=evi_array,
    engine='phenolopy',
    config=config,
    start_date='2021-01-01'
)

print(ds_phenos)