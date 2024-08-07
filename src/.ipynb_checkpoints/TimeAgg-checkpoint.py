import os
import pandas as pd

class TimeAgg:

    def __init__(self, sd: str, ed: str, i_dir: str, o_dir: str, llm_obj=None):
        """
        sd: string start date format YYYY-MM-DD
        ed: string end date format YYYY-MM-DD
        i_dir: directory with text files containing journal entries, with filename convention of dates
        o_dir: output directory
        llm_obj: if running smart summary, pass in an llm object (from langchain_community.llms)
        """
        self.sd = sd
        self.ed = ed
        self.i_dir = i_dir
        self.o_dir = o_dir
        self.files = os.listdir(self.i_dir)

        self.llm = llm_obj

    def run(self):

        self.get_files_in_daterange()
        self.gen_smart_summary()
        self.gen_template()

    def get_files_in_daterange(self):

        self.filter_dates_list = list(pd.date_range(self.sd, self.ed).strftime('%Y-%m-%d'))
        self.pages_dates_list = [file.split('.')[0] for file in self.files]
        self.selected_dates_list = list(set(self.filter_dates_list) & set(self.pages_dates_list))
        self.selected_dates_list.sort()
        self.selected_pages_list = [file + '.md' for file in self.selected_dates_list]

    def gen_smart_summary(self):
        """
        this is the part where we prompt an LLM to summarize our entries from this time period, give us feedback, and offer questions / writing prompts
        """

        # grab the journal text
        j_text = ""
        for page in self.selected_pages_list:
            with open(self.i_dir + page, 'r') as file:
                data = file.read()  # .replace('\n', '')
                j_text = j_text + data
                j_text = j_text + "\n"

        self.subquery_1 = f"Here are my journal entries from {self.sd} to {self.ed}: "
        self.subquery_2 = j_text
        self.subquery_3 = f"**AI Journal Entry Analysis**\
        Analyze my journal entries from {self.sd} to {self.ed}.\
        In your analysis, answer the following questions:\
        What was my focus during this time period--what did I want? Respond to this under the heading **Focus:**.\
        What were my relationships with other people like? Who did I talk to? How did I feel about them? Respond to this under the heading **People:**.\
        What did I work on, achieve, read, or practice (for example: coding, meditation, yoga, my job)? Respond to this under the heading **Practice:**.\
        What did I learn about myself during this time period? Respond to this under the heading **Insights:**.\
        Write the analysis in second person: 'You did...'"

        self.query = self.subquery_1 + self.subquery_2 + self.subquery_3
        self.smart_summary = self.llm(self.query)

    def gen_template(self):

        self.backlinks_str = 'backlinked dates: '
        for date in self.selected_dates_list:
            self.backlinks_str = self.backlinks_str + '[[' + date + ']], '

        with open(self.o_dir + self.sd + ':' + self.ed + '.md', 'w') as f:
            f.write("Date: \n\n")
            f.write(self.backlinks_str + "\n\n")
            f.write("backlinks: \n\n")
            f.write(self.smart_summary)
            f.write("\n\n**Human Reflection:**\n\n")
            f.write(
                "What is the AI analysis bringing up for you? What lessons or shifts in focus do you want to take into the future? Reflect: \n\n")
