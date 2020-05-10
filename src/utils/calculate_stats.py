import numpy as np

# def weighted_percentile_of_score(a, weights, score, kind='weak'):
#     npa = np.array(a)
#     npw = np.array(weights)
#
#     if kind == 'rank':  # Equivalent to 'weak' since we have weights.
#         kind = 'weak'
#
#     if kind in ['strict', 'mean']:
#         indx = npa < score
#         strict = 100 * sum(npw[indx]) / sum(weights)
#     if kind == 'strict':
#         return strict
#
#     if kind in ['weak', 'mean']:
#         indx = npa <= score
#         weak = 100 * sum(npw[indx]) / sum(weights)
#     if kind == 'weak':
#         return weak
#
#     if kind == 'mean':
#         return (strict + weak) / 2


# a = [1, 2, 3, 4]
# weights = [2, 2, 3, 3]
# print(weighted_percentile_of_score(a, weights, 3))  # 70.0 as desired.


def calc_stats(app, name, rolls):

    pips_array = [int(i["pip_total"]) for i in rolls]
    prob_array = [float(i["probability"]) for i in rolls]

    avg_pips = round(np.average(pips_array, weights=prob_array),2)
    min_pips = min(pips_array)
    max_pips = max(pips_array)

    # 10%
    # 90%

    stats_dict = {
        'v1_name': name,
        'v2_avg': avg_pips,
        'v3_min': min_pips,
        'v4_max': max_pips
    }

    app.logger.info(stats_dict)

    return stats_dict
