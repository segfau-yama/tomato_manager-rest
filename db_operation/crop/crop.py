import board
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def database_conn(engine):
    df = pd.read_sql("SELECT maturity FROM level_setting_level \
                    ORDER BY date_time DESC \
                    LIMIT 1", con=engine)
    df.to_csv('maturity.csv', index=False)

    df = pd.read_sql(
        "SELECT id, red, green, blue, crop_id FROM datas_tomato", con=engine)
    return df


def format_change(df):
    sample_df = []
    samples = [[], [], [], [], []]
    for crop_id in range(5):
        # 作物idごとに配列を分割．データから作物idを除外
        sample_df.append(df[df['crop_id'] == crop_id + 1]
                         .filter(items=["red", "green", "blue"]))
    return sample_df


def judgement_corrcoef(measurements, samples, forecast):
    correlations = []
    # 5回相関係数を導出(基準データ20*5)
    for crop_id in range(5):
        correlation = np.corrcoef(measurements, samples[crop_id])
        if crop_id == 0:
            correlations = np.mean(correlation[0][1:])
        else:
            correlations = np.append(correlations, np.mean(correlation[0][1:]))
    result = int(correlations.argmax() + 1) == int(forecast)
    return result


def check_rgb_range(rgb_array, rgb_range):
    rgb_range = np.array(rgb_range)
    rgb_array = np.array(rgb_array)
    return np.sum((rgb_range[0] <= rgb_array) & (rgb_array <= rgb_range[1])) / rgb_array.size


def judgement_rgb(measurements, rgb_range, forecast):
    # RGB分布での判定
    rgb_distributions = []
    measurements = np.array(measurements)
    rgb_range = np.array(rgb_range)
    for crop_id in range(5):
        i = crop_id * 2
        concordance_val = np.sum((rgb_range[i] <= measurements) &
                                 (measurements <= rgb_range[i + 1])
                                 )
        rgb_distribution = concordance_val / measurements.size
        np.append(rgb_distributions, rgb_distribution)
    print(rgb_distributions)
    result = int(rgb_distributions.argmax() + 1) == int(forecast)
    return result
