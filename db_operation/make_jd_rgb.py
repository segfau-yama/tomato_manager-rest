import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import crop

# rgb分布作成用プログラム
connection_config = {
    'host': 'containers-us-west-119.railway.app',
    'port': 6442,
    'database': 'research',
    'user': 'postgres',
    'password': 'lYRIXz15NSpu371JXmo4',
}
engine = create_engine(
    'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))
# データベース処理
df = crop.database_conn(engine)
# データフレームを変換
samples = crop.format_change(df)
color_ranges = pd.concat([pd.DataFrame([sample.min(), sample.max()])
                         for sample in samples], ignore_index=True)
print(f"{color_ranges}")
color_ranges.to_csv("color_ranges.csv")
color_rgb = np.array([[1, 2, 1], [3, 4, 5], [53, 14, 5]])
print(color_ranges[0:2])
concordance = crop.check_rgb_range(color_rgb, color_ranges[0:2])
print(concordance)
