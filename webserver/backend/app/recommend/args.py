import argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='../data/', help='data path')
    parser.add_argument('--grid_file', type=str, default='grid_infra_data_v1.1.csv', help='frid file name')
    parser.add_argument('--infra_file', type=str, default='raw_data/직방크롤링원룸오피스텔.csv', help='infra score file name')

    parser.add_argument('--user_name', type=str, default='1', help='name of user')
    parser.add_argument('--user_loc', type=str, default='강남구', help='location selected')
    
    parser.add_argument('--select_infra', type=str, default='영화관,약국,지하철,카페,편의점', help='infra selected')

    args = parser.parse_args()

    return args