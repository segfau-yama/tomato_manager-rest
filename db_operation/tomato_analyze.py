import board
import adafruit_tcs34725
import adafruit_tca9548a
import numpy as np
import pandas as pd
import sys
from sqlalchemy import create_engine
from gpiozero import RotaryEncoder, Button, LEDBoard

sw = 14
enc_a = 15
enc_b = 18

counter = RotaryEncoder(enc_a, enc_b, wrap=True, max_steps=4)
switch = Button(sw, pull_up=True)

seg = LEDBoard(25, 8, 16, 20, 21, 24, 23, 12)
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
    (1, 1, 1, 1, 1, 1, 1, 1), #ok
]
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    while True:
        maturity = abs(counter.steps) + 1
        print(maturity)
        seg.value = pattern[maturity]
        if switch.is_pressed:
            print("end")
            break
    
    # 引数が足りない場合エラー
    argv_len = len(sys.argv)
    if argv_len < 2:
        sys.exit("エラー：引数が足りません。\n例:python3 tomato_analyze.py 1")
    elif argv_len > 2:
        sys.exit("エラー：引数が多すぎます。\n例:python3 tomato_analyze.py 1")
    else:
        forecast = sys.argv[1]
    
    i2c = board.I2C()
    mux = adafruit_tca9548a.TCA9548A(i2c)
    sensor = []
    
    samples = [[], [], [], [], []]
    
    # TCA9458での4個のI2Cセンサ割り当て
    for i in range(3, 7):
        sensor.append(adafruit_tcs34725.TCS34725(mux[i]))
        sensor[i - 3].gain = 4
        sensor[i - 3].integration_time = 150
    
    # データベース処理
    connection_config = {
        'host': 'containers-us-west-119.railway.app',
        'port': 6442,
        'database': 'research',
        'user': 'postgres',
        'password': 'lYRIXz15NSpu371JXmo4',
    }
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))
    df = pd.read_sql("SELECT * FROM datas_tomato", con=engine)
    print(df)
    
    # 成熟度ごとにデータフレームを分割
    sample_df = []
    for crop_id in range(5):
        sample_df.append(df[df['crop_id'] == crop_id + 1]
                         .filter(items=["red", "green", "blue"]))
    
    # データフレームを統合し、転置を取る
    for crop_id in range(5):
        for i in range(0, 81, 20):
            sample = np.array(sample_df[crop_id][i:i+20])
            samples[crop_id].append(sample.T.flatten())
    samples = np.array(samples)
    
    judgements = []
    # 相関測定:20回
    for ms in range(20):
        # カラーデータ取得:カラーセンサ4個×5回
        measurements = []
        for i in range(4):
            for j in range(5):
                measurement = list(sensor[i].color_rgb_bytes)
                measurements.append(measurement)
            measurements = sorted(measurements)
        measurements = np.array(measurements, dtype="int").T.flatten()
        
        # 相関係数導出
        correlations = []
        for crop_id in range(5):
            correlation = np.corrcoef(measurements, samples[crop_id])
            if crop_id == 0:
                correlations = np.mean(correlation[0][1:])
            else:
                correlations = np.append(correlations, np.mean(correlation[0][1:]))
        result = int(correlations.argmax() + 1) == int(forecast)
        print(result)
        judgements.append([forecast, result])
        
    judgement_df = pd.DataFrame(judgements)
    judgement_df.columns = ["forecast_id", "result"]
    print(judgement_df)

    judgement_df.to_sql('datas_judgement', con=engine, index=False, if_exists='append')

        
if __name__ == '__main__':
    main()
