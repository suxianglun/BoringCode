#! /usr/bin/env python3
"""Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beijing shanghai 2016-08-25
"""
from docopt import docopt
import requests
from prettytable import PrettyTable
from stations import stations
from getPrice import get_price


def colored(color, text):
    table = {
        'red': '\033[91m',
        'green': '\033[92m',
        # no color
        'nc': '\033[0m'
    }
    cv = table.get(color)
    nc = table.get('nc')
    return ''.join([cv, text, nc])

class TrainCollection(object):

    # 显示车次、出发/到达站、 出发/到达时间、历时、一等坐、二等坐、软卧、硬卧、硬座
    header = 'train station time duration first second softsleep hardsleep hardsit'.split()

    def __init__(self, rows):
        self.rows = rows

    def _get_duration(self, row):
        """
        获取车次运行时间
        """
        duration = row.get('lishi').replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    def formatPrint(self,valTop,valBot):
        return '\n'.join([colored('nc',valTop),colored('green',valBot)])
    @property
    def trains(self):
        global date
        for row in self.rows:
            pricerow = ['','','','','','','','','']
            # next line is very slow  comment it will be faster
            pricerow = get_price(row['train_no'],row['from_station_no'],row['to_station_no'],row['seat_types'],date)
            train = [
                # 车次
                row['station_train_code'],
                # 出发、到达站
                '\n'.join([colored('green', row['from_station_name']),colored('red', row['to_station_name'])]),
                # 出发、到达时间
                '\n'.join([colored('green', row['start_time']),colored('red', row['arrive_time'])]),
                # 历时
                self._get_duration(row),
                # 一等坐
                self.formatPrint(row['zy_num'], pricerow[2]),
                # 二等坐
                self.formatPrint(row['ze_num'], pricerow[3]),
                # 软卧
                self.formatPrint(row['rw_num'], pricerow[5]),
                # 硬卧
                self.formatPrint(row['yw_num'], pricerow[6]),
                # 硬坐
                self.formatPrint(row['yz_num'], pricerow[8])
            ]
            yield train

    def pretty_print(self):
        """
        数据已经获取到了，剩下的就是提取我们要的信息并将它显示出来。
        `prettytable`这个库可以让我们它像MySQL数据库那样格式化显示数据。
        """
        pt = PrettyTable()
        # 设置每一列的标题
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    global date
    date = arguments['<date>']
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station
    )
    print(url)
    r = requests.get(url, verify=False)
    rows = r.json()['data']['datas']
    #print(r.json())
    trains = TrainCollection(rows)
    trains.pretty_print()

if __name__ == '__main__':
    cli()
