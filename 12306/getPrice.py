#! /usr/bin/env python3
"""Train getPrice query via command-line.

Usage:
    getPrice <train_no> <from_station_no> <to_station_no> <seat_types> <train_date>

Options:
    -h,--help   显示帮助菜单

Example:
    tickets beijing shanghai 2016-08-25
"""

#商务座  特等座  一等座  二等座  高级软卧  软卧  硬卧  软座  硬座  无座
#A9        P        M      O       A6       A4    A3    A2     A1    WZ

from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable



def get_price(train_no,from_station_no,to_station_no,seat_types,train_date):
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}'.format(train_no,from_station_no,to_station_no,seat_types,train_date)
    r = requests.get(url, verify=False)
    rows = r.json()['data']
    ret = [
            (('A9' in rows) and rows['A9'] or ""),
            (('P'  in rows) and rows['P']  or ""),
            (('M'  in rows) and rows['M']  or ""),
            (('O'  in rows) and rows['O']  or ""),
            (('A6' in rows) and rows['A6'] or ""),
            (('A4' in rows) and rows['A4'] or ""),
            (('A3' in rows) and rows['A3'] or ""),
            (('A2' in rows) and rows['A2'] or ""),
            (('A1' in rows) and rows['A1'] or ""),
            (('WZ' in rows) and rows['WZ'] or "")
            ]
    return ret
    return rows

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    train_no = arguments['<train_no>']
    from_station_no = arguments['<from_station_no>']
    to_station_no = arguments['<to_station_no>']
    seat_types = arguments['<seat_types>']
    train_date = arguments['<train_date>']
    rows = get_price(train_no,from_station_no,to_station_no,seat_types,train_date)
    print(rows)

if __name__ == '__main__':
    cli()
