from src.GenSynthJournal import GenSynthJournal
import time

if __name__ == '__main__':
    print('started job at ' + time.ctime())
    synth_j = GenSynthJournal()
    synth_j.build_journal_db()

