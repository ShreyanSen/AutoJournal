from langchain_community.llms import Ollama
import numpy as np
import datetime
import time

class GenSynthJournal:

    def __init__(self):
        self.get_days_from_first_entry()
        self.get_journal_date_strings()
        self.get_locations()
        #self.get_prompt()

        self.llm = Ollama(model="llama3")

    def get_days_from_first_entry(self):
        num_entries = 100
        avg_days_till_next_entry = 5
        days_to_entry = np.random.exponential(avg_days_till_next_entry, num_entries)
        days_to_entry = days_to_entry.astype(int)  # map to integers to get gaps between dates
        days_to_entry = np.clip(days_to_entry, 1,
                                365)  # let's avoid multiple entries per date; make the min value 1 and max 365
        self.days_from_first_entry = days_to_entry.cumsum()

    def get_journal_date_strings(self):
        first_date_str = '2124-01-01'
        first_date = datetime.datetime.strptime(first_date_str, '%Y-%m-%d')
        journal_dates = [first_date + datetime.timedelta(days=int(el)) for el in self.days_from_first_entry]
        self.journal_date_strings = [datetime.datetime.strftime(el, '%Y-%m-%d') for el in journal_dates]

    def get_locations(self):
        location_1 = ["Zardon, a cold and desolate ice planet. "] * 40
        location_2 = ["Last Call, an unregulated space port open to smugglers. "] * 10
        location_3 = ["Myros, a warm water world filled with strange beautiful creatures. "] * 50
        self.locations = location_1 + location_2 + location_3

    def get_prompt(self, i):
        i_date = self.journal_date_strings[i]
        i_days = str(self.days_from_first_entry[i])
        i_entry = str(i + 1)
        i_location = self.locations[i]

        str_1 = "You are the thoughtful, curious space explorer Battuta sitting down at the end of the day to write a journal entry. The year is " + i_date + ". "
        str_2 = "You are writing Battuta's journal number " + i_entry + " and it has been " + i_days + " days since the first entry. "
        str_3 = "Your ship's navigational charts indicate your location is " + i_location
        str_4 = "Please write a short journal entry of what happened to you, space explorer Battuta, today, and what you felt and learned."

        prompt_strings = [str_1, str_2, str_3, str_4]

        journal_prompt = ('').join(prompt_strings)
        return journal_prompt

    def build_journal_db(self, data_dir="./data/synth_journal/"):
        for i in range(0, len(self.journal_date_strings)):
            print("starting run number " + str(i+1) + " at " + time.ctime())
            prompt = self.get_prompt(i=i)
            response = self.llm(prompt)
            jdate = self.journal_date_strings[i]
            with open(data_dir + jdate + '.md', 'w') as f:
                f.write("Date: ")
                f.write(jdate + "\n\n")
                f.write(response)



