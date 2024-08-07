# AutoJournal

### Basics

Get monthly smart summaries of your daily journal entries to reflect on your life at a higher level.

Autojournal creates AI smart summaries for your journal entries at a periodicity of your choosing (e.g. weekly, monthly), describing important events and common themes and offering an entry point for further journaling.

In this repo you'll find the scripts I use myself. The categories I use will not be useful to everyone, and I encourage you to create your own prompts and categories by tweaking subquery 3 of the "gen_smart_summary" function of the TimeAgg class found in src/TimeAgg.py.

An example is provided. An llm-generated set of synthetic journal entries for the 23rd century space explorer Battuta serves as an input, found at data/synth_journal, while the processed smart summaries are found at data/synth_journal_smart_summaries. 


### Local LLM Requirements

Autojournal relies on a local llm via ollama, requiring a working ollama configuration on your device and llama3 installed. This is for the best. Do you really want to send your journal to an llm in the cloud? To learn how to install and run ollama, go here: 

https://ollama.com/

You'll also need the python libraries indicated in requirements.txt.


### Description of Scripts

The script gen_synthetic_journal.py was used generate the synthetic journal entries used in our example.

The script backfill_smart_summaries.py reads the journal entries (locally) and generates smart summaries.
Run "backfill_smart_summaries.py" specifying your input directory, an output directory, a date range, and a temporal bucket size (e.g. monthly) to generate higher level entries. Autojournal relies on journal entries living in one directory indexed by date in YYYY-MM-DD.md format, just like they are in the example in /data. 

