from gpiozero import RotaryEncoder, Button, LEDBoard
import time
import board
import adafruit_tcs34725
import adafruit_tca9548a
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import crop

# ピン番号(ロータリーエンコーダ)
sw = 14
enc_a = 15
enc_b = 18

# ピン割り当て
counter = RotaryEncoder(enc_a, enc_b, wrap=True, max_steps=9)
switch = Button(sw, pull_up=True)
maturity_led = LEDBoard(25, 8, 16, 20, 21, 24, 23, 12)
harvest = LEDBoard(17, 27)

# 収穫判定パターン配列
judge = [
    (0, 1), #可能
    (1, 0), #不可
    (1, 1), #判定前
    (0, 0), #判定中
]

# 7セグパターン配列
pattern = [
   # a, b, c, d, e, f, g, dp 
    (1, 1, 1, 1, 1, 1, 0, 0), #0
    (0, 1, 1, 0, 0, 0, 0, 0), #1
    (1, 1, 0, 1, 1, 0, 1, 0), #2
    (1, 1, 1, 1, 0, 0, 1, 0), #3
    (0, 1, 1, 0, 0, 1, 1, 0), #4
    (1, 0, 1, 1, 0, 1, 1, 0), #5
    (1, 0, 1, 1, 1, 1, 1, 0), #6
    (1, 1, 1, 0, 0, 1, 0, 0), #7
    (1, 1, 1, 1, 1, 1, 1, 0), #8
    (1, 1, 1, 1, 0, 1, 1, 0), #9
    (1, 0, 0, 1, 1, 1, 1, 0), #END
]
maturity_led.value = pattern[1]
"""
def crop_sensor_attach(sensor_count = 4, gain = 4, integration_time = 150):
    i2c = board.I2C()
    mux = adafruit_tca9548a.TCA9548A(i2c)
    sensor = []
    
    for i in range(3, 3 + sensor_count):
        sensor.append(adafruit_tcs34725.TCS34725(mux[i]))
        sensor[i - 3].gain = gain
        sensor[i - 3].integration_time = integration_time
    return sensor

def crop_database_conn(engine):
    df = pd.read_sql("SELECT maturity FROM level_setting_level \
                    ORDER BY date_time DESC \
                    LIMIT 1", con=engine)
    df.to_csv('/home/yamamoto/start/maturity.csv', index=False)
    
    df = pd.read_sql("SELECT id, red, green, blue, crop_id FROM datas_tomato", con=engine)
    return df

def crop_format_change(df):
    sample_df = []
    samples = [[], [], [], [], []]
    for crop_id in range(5):
        # 作物idごとに配列を分割．データから作物idを除外
        sample_df.append(df[df['crop_id'] == crop_id + 1]
                         .filter(items=["red", "green", "blue"]))
    # データフレームを統合し、転置を取る
    for crop_id in range(5):
        for i in range(0, 81, 20):
            sample = np.array(sample_df[crop_id][i:i+20])
            samples[crop_id].append(sample.T.flatten())
    samples = np.array(samples)
    print(sample_df)
    return samples

def crop_measurment(sensor):
    sensor_count = len(sensor)
    measurements = []
    
    # 測定(センサ4個*5回)
    for i in range(sensor_count):
        for j in range(5):
            measurement = list(sensor[i].color_rgb_bytes)
            measurements.append(measurement)
        measurements = sorted(measurements)
    measurements = np.array(measurements, dtype="int").T.flatten()
    return measurements
    


def crop_judgement_corrcoef(measurements, samples, forecast):
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

def crop_judgement_rgb(measurements, samples, forecast):
    # RGB分布での判定
    rgb_distributions = []
    for crop_id in range(5):
        rgb_distribution = np.corrcoef(measurements, samples[crop_id])
        if crop_id == 0:
            rgb_distributions = np.mean(rgb_distribution[0][1:])
        else:
            rgb_distributions = np.append(rgb_distributions, np.mean(rgb_distribution[0][1:]))
    result = int(rgb_distributions.argmax() + 1) == int(forecast)
    return result
"""
# メイン処理
while True:
    connection_config = {
        'host': 'containers-us-west-119.railway.app',
        'port': 6442,
        'database': 'research',
        'user': 'postgres',
        'password': 'lYRIXz15NSpu371JXmo4',
    }
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))
    
    judgements = []
    maturity = abs(counter.steps) + 1
    maturity_led.value = pattern[maturity]
    harvest.value = judge[2]
    # ボタンを押すと測定開始
    if switch.is_pressed:
        # 7セグの表示がEなら測定終了
        if maturity == 10:
            exit()
        print(f'forecast is {maturity}')
        for i in range(5):
            blink = 2 if i % 2 else 3
            harvest.value = judge[blink]
            time.sleep(0.4)
        harvest.value = judge[3]
        # TCA9458での4個のI2Cセンサ割り当て
        sensor = crop_sensor_attach()
        # データベース処理
        df = crop_database_conn(engine)
        # データフレームを変換
        samples = crop_format_change(df)
        
        # カラーデータ取得，測定結果取得
        measurements = crop_measurment(sensor)
        result_corrcoef = crop_judgement_corrcoef(measurements, samples, maturity)
        result_rgb = crop_judgement_rgb(measurements, samples, maturity)
        
        harvest.value = judge[result_corrcoef]
        print(result_corrcoef)
        time.sleep(3)
        harvest.value = judge[3]
        
        # 判定結果データフレーム配列作成
        judgements.append([maturity, result_corrcoef])
        
        judgement_df = pd.DataFrame(judgements)
        judgement_df.columns = ["forecast_id", "result"]
        judgement_df.to_sql('datas_judgement', con=engine, index=False, if_exists='append')

