import psycopg2
import pandas as pd
from sqlalchemy import create_engine


def main():
    df = pd.read_csv('db_operation/color_data.csv')
    connection_config = {
        'host': 'containers-us-west-119.railway.app',
        'port': 6442,
        'database': 'research',
        'user': 'postgres',
        'password': 'lYRIXz15NSpu371JXmo4',
    }
    engine = create_engine(
        'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))
    # df.to_sql('datas_tomato', con=engine, if_exists='append', index=False)
    df = pd.read_sql("SELECT * FROM datas_tomato", con=engine)
    print(df)


if __name__ == '__main__':
    main()
