import board
import adafruit_tcs34725
import adafruit_tca9548a
import numpy as np
import pandas as pd
import os

i2c = board.I2C()

mux = adafruit_tca9548a.TCA9548A(i2c)
sensor = []
colors = []
filepath = "color_data.csv"
labels = ["crop_type", "red", "green", "blue"]
SENSOR_COUNT = 4 # センサー個数
DATA_COUNT = 5 # レベルごとのカラーデータセットの数

# TCA9458での5個のI2Cセンサ割り当て
for i in range(3, 7):
    sensor.append(adafruit_tcs34725.TCS34725(mux[i]))
    sensor[i - 3].gain = 4
    sensor[i - 3].integration_time = 150

output_file = "output4a.csv"
sample_df = []
df = pd.read_csv(filepath)
samples = [[], [], [], [], []]
red, green, blue = [], [], []

# 成熟度ごとにデータフレームを分割
for crop_type in range(DATA_COUNT):
    sample_df.append(df[df['crop_type'] == crop_type + 1]
                     .filter(items=["red", "green", "blue"]))

# データフレームを統合，転置，一次元化
for crop_type in range(DATA_COUNT):
    for i in range(0, 81, 20):
        sample = np.array(sample_df[crop_type][i:i+20])
        samples[crop_type].append(sample.T.flatten())
samples = np.array(samples)
print(samples)

# 相関測定:20回
for ms in range(20):
    measurements = []
    correlations = []
    measurements = []
    
    # カラーデータ取得:カラーセンサ4個×5回
    for i in range(SENSOR_COUNT):
        for j in range(DATA_COUNT):
            measurement = list(sensor[i].color_rgb_bytes)
            measurements.append(measurement)
        measurements = sorted(measurements)
    measurements = np.array(measurements, dtype="int").T.flatten()
    
    for crop_type in range(DATA_COUNT):
        correlation = np.corrcoef(measurements, samples[crop_type])
        if crop_type == 0:
            correlations = np.mean(correlation[0][1:])
        else:
            correlations = np.append(correlations, np.mean(correlation[0][1:]))
    print(correlations)
    print(correlations.argmax() + 1)

    df = pd.DataFrame(correlations).T
    df.columns = ["green_apple", "yellow_apple",
                  "red_apple", "orange", "tomato"]
    print(df)

    if os.path.isfile(output_file):
        df.to_csv(output_file, index=False, header=False, mode="a")
    else:
        df.to_csv(output_file, index=False)
