# AutoJournal

### Basics

Get monthly smart summaries of your daily journal entries to reflect on your life at a higher level.

Autojournal creates AI smart summaries for your journal entries at a periodicity of your choosing (e.g. weekly, monthly), describing important events and common themes and offering an entry point for further journaling.

### Example Journal

An example is provided. An llm-generated set of synthetic journal entries for the 22rd century space explorer Battuta is found here:

https://github.com/ShreyanSen/AutoJournal/tree/main/data/synth_journal

The processed smart summaries are found here:

https://github.com/ShreyanSen/AutoJournal/tree/main/data/synth_journal_smart_summaries


### Using + Modifying Scripts & Prompts

The script gen_synthetic_journal.py was used generate the synthetic journal entries used in our example. Found here:

https://github.com/ShreyanSen/AutoJournal/blob/main/gen_synthetic_journal.py

Example run: `python gen_synthetic_journal.py`

The script backfill_smart_summaries.py reads the journal entries (locally) and generates smart summaries.
Run "backfill_smart_summaries.py" specifying your input directory, an output directory, a date range, and a temporal bucket size (e.g. monthly) to generate higher level entries. Check the argparse flag descriptions for more details. Autojournal relies on journal entries living in one directory indexed by date in YYYY-MM-DD.md format, just like they are in the example in /data. Found here:

https://github.com/ShreyanSen/AutoJournal/blob/main/backfill_smart_summaries.py

Example run: `python backfill_smart_summaries.py -i data/synth_journal/ -o data/synth_journal_smart_summaries/ -sd 2124-01-01 -ed 2125-01-01 -bfm True`

The categories I use to structure smart summaries will not be useful to everyone, and I encourage you to create your own prompts and categories by tweaking subquery 3 of the "gen_smart_summary" function of the TimeAgg class found in src/TimeAgg.py. Found here:

https://github.com/ShreyanSen/AutoJournal/blob/a7875bf556f7a6cdff73c43f6aa17b477ef4cd41/src/TimeAgg.py#L51

### Local LLM Requirements

Autojournal relies on a local llm via ollama, requiring a working ollama configuration on your device and llama3 installed. This is for the best. Do you really want to send your journal to an llm in the cloud? To learn how to install and run ollama, go here:

https://ollama.com/

You'll also need the python libraries indicated in requirements.txt.
