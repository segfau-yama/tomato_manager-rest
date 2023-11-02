import pandas as pd

from sqlalchemy import create_engine


def main():
    connection_config = {
        'host': 'containers-us-west-119.railway.app',
        'port': 6442,
        'database': 'research',
        'user': 'postgres',
        'password': 'lYRIXz15NSpu371JXmo4',
    }
    engine = create_engine(
        'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))

    df = pd.read_sql("SELECT * FROM datas_judgement", con=engine)
    print(df)
    """
    df.to_sql('datas_tomato', con=engine, index=False, if_exists='append')
    df = pd.read_csv("color_data.csv")
    df.to_sql('datas_tomato', con=engine, index=False, if_exists='append')
    df.to_csv('crops.csv', index=False)
    d = {"id": [1], "forecast_id": [1], "result": [False],
         "date_time": [None]}
    df = pd.DataFrame(data=d)
    df.to_sql('datas_judgement', con=engine, index=False, if_exists='replace')
    print(df)
    """


if __name__ == '__main__':
    main()
