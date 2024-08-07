import argparse
import time
from pandas.tseries.offsets import MonthEnd
import pandas as pd
from langchain_community.llms import Ollama

from src.TimeAgg import TimeAgg

def get_args():
    """
    sd: start date condition for journal entries we'll analyze (inclusive)
    ed: end date condition for journal entries we'll analyze (inclusive)
    i: input directory where journal entries live with naming convention of date (YYYY-MM-DD)
    o: output directory where we deposit smart summaries
    bfws: if we're not backfilling the default None will use the exact sd and ed provided. If we provide a
        value here then we'll start backfilling, taking chunks each sized the number of days provided, from within the
        sd and ed. for example, if sd=2024-01-01 and ed=2024-03-01, and we have no backfill-wsize, we'll just get a
        AI analysis for those whole two months. but if we set it to 7, we'll get a weekly analysis for every week in
        those two months. there is fencepost behavior. we make tuples of start and end dates, inclusive of the
        sd value provided, such that each tuple is 'backfill_window' days long, until the point where the
        new start date of a pair would exceed the ed given. for example if sd=2024-01-01, ed = 2024-01-08, and
        bfws=7, then our tuples will be 2024-01-01:2024-01-07 and 2024-01-08:2024-01-14
    bfm: for monthly summaries (where there is no fixed backfill window size). providing a bfws will overwrite this!
    """
    parser = argparse.ArgumentParser(description='Arguments for getting device adjusted and unadjusted segment std')
    parser.add_argument('-sd', type=str, help='start date for query format YYYY-MM-DD', default='2020-01-01')
    parser.add_argument('-ed', type=str, help='end date for query format YYYY-MM-DD', default='2020-06-30')
    parser.add_argument('-i', type=str, help='input directory',
                        default = './data/synth_journal/')
    parser.add_argument('-o', type=str, help='output directory',
                        default = './data/synth_journal_smart_summaries/')
    parser.add_argument('-bfws', type=int, help='backfill window size, num days per chunk for backfilling',
                        default=None)
    parser.add_argument('-bfm', type=bool, help='backfill monthly, can be set to True or False',
                        default=False)

    args = parser.parse_args()
    return args.sd, args.ed, args.i, args.o, args.bfws, args.bfm

def parse_backfill_dates_by_window(sd, ed, backfill_window=7):
    """
    sd: overall start date
    ed: overall end date
    backfill: str, 'biweekly' or 'monthly'

    makes tuples of start and end dates, inclusive of the sd value provided, such that each tuple is 'backfill_window' days long,
    until the point where the new start date of a pair would exceed the ed given
    returns a list of tuples
    """
    sdt = pd.to_datetime(sd)
    edt = pd.to_datetime(ed)

    sd_list = []
    ed_list = []

    while sdt <= edt:
        sd_list.append(sdt)
        ed_list.append(sdt + pd.Timedelta(backfill_window - 1, unit='D'))
        sdt = sdt + pd.Timedelta(backfill_window, unit='D')
    sd_list = [el.strftime('%Y-%m-%d') for el in sd_list]
    ed_list = [el.strftime('%Y-%m-%d') for el in ed_list]
    sd_ed_tuples = list(zip(sd_list, ed_list))

    return sd_ed_tuples

def parse_backfill_dates_by_month(sd, ed):
    """
    backfills by month for all months between sd and ed, inclusive of sd and ed month
    so if sd is 2024-03-05 and ed is 2024-05-20, it'll get it for 2024-03, 2024-04, and 2024-05
    """
    sd_month = pd.to_datetime(sd, format='%Y-%m-%d').to_period('M').to_timestamp()
    ed_month = pd.to_datetime(ed, format='%Y-%m-%d').to_period('M').to_timestamp()

    sd_list = pd.date_range(sd_month, ed_month, freq='MS')
    ed_list = [el + MonthEnd(0) for el in sd_list]

    sd_list = [el.strftime('%Y-%m-%d') for el in sd_list]
    ed_list = [el.strftime('%Y-%m-%d') for el in ed_list]
    sd_ed_tuples = list(zip(sd_list, ed_list))

    return sd_ed_tuples

if __name__ == '__main__':
    print('started job at ' + time.ctime())
    sd, ed, input_dir, output_dir, backfill_chunk_size, backfill_monthly = get_args()
    llm_obj = Ollama(model="llama3") # i think initializing outside the timeagg obj will enable our llm to learn from
    #past summarizations which is pretty interesting! it'll make its inference have some long-term time dependence!

    if backfill_chunk_size:
        sd_ed_tuples = parse_backfill_dates_by_window(sd, ed, backfill_chunk_size) # for specific chunk size like 7 days
    elif backfill_monthly:
        sd_ed_tuples = parse_backfill_dates_by_month(sd, ed)
    else: sd_ed_tuples = [(sd, ed)]

    for i in range(0, len(sd_ed_tuples)):
        sd_ed_tuple = sd_ed_tuples[i]
        print("started chunk number " + str(i) + " at " + time.ctime() )
        t_obj = TimeAgg(sd=sd_ed_tuple[0], ed=sd_ed_tuple[1], i_dir=input_dir, o_dir=output_dir, llm_obj=llm_obj)
        t_obj.run()

    print('completed job at ' + time.ctime())