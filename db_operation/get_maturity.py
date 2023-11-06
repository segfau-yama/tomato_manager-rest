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
    df = pd.read_sql("SELECT maturity FROM level_setting_level \
                    ORDER BY date_time DESC \
                    LIMIT 1", con=engine)
    df.to_csv('/home/yamamoto/start/maturity.csv', index=False)


if __name__ == '__main__':
    main()
