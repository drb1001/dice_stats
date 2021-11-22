
def calc_stats(roll_name, rolls):
    """Given a list of dicts representing rolls probabilities, calculate statisctics

    The output is a dict with keys:
        name (str)
        avg (float)
        min (int)
        max (int)
        mode (str)
        perc_10 (int)
        perc_90 (int)
        pct80_range (str)
        max_range (str)
    """

    pips_array = [int(i["pip_total"]) for i in rolls]
    prob_array = [float(i["probability"]) for i in rolls]

    # Easy stats
    min_pips = min(pips_array)
    max_pips = max(pips_array)
    avg_pips = round(sum([i*j for i,j in zip(pips_array,prob_array)]), 2)

    # Get mode / highest prob
    max_prob = max(prob_array)
    mode_pips_list = [i['pip_total'] for i in rolls if float(i['probability']) == max_prob]
    if len(mode_pips_list) == 1:
        mode_pips = str(mode_pips_list[0])
    elif len(mode_pips_list) == 2:
        mode_pips = str(mode_pips_list[0]) + ' & ' + str(mode_pips_list[1])
    else:
        mode_pips = 'N/A'

    # Get 10th / 90th percentile
    cum_sum = 0
    for ix,p in enumerate(prob_array):
        cum_sum = cum_sum + p
        if cum_sum > 0.1:
            perc_10 = pips_array[ix]
            break

    cum_sum = 0
    for ix,p in enumerate(prob_array[::-1]):
        cum_sum = cum_sum + p
        if cum_sum > 0.1:
            perc_90 = pips_array[::-1][ix]
            break

    # Arrange output
    stats_dict = {
        'name': roll_name,
        'avg': avg_pips,
        'min': min_pips,
        'max': max_pips,
        'mode': mode_pips,
        'perc_10': perc_10,
        'perc_90': perc_90,
        'pct80_range': '{} to {}'.format(perc_10, perc_90),
        'max_range': '{} to {}'.format(min_pips, max_pips)
    }

    return stats_dict
