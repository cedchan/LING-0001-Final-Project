# Syntactic Complexity Trends over Time | LING 0001 Final Project

## Navigating Project Directories

- `main.py` runs the text analysis on the inaugural addresses. 
- `tools` is a module containing key methods for conducting the analysis. The module that `main.py` directly interfaces with is `text_analysis.py`.
- `data/text_jsons` contains the inaugural addresses and relevant information about them, stored as JSON files. The other folders in the `data` directory contain portions of other datasets from the UCSB Presidency Project, although they are not used in the analysis.
- `reference` has word frequency and age of acquisition lists, as well as `special_chars.txt`, which stores particular tokens that should be replaced when converting parsed text into XML format.
- `results` contains saved analysis results in CSV format.
- `analysis` includes `features.py` and `plots.r`, which respectively apply dimensionality reduction to the collected features and graph them with respect to time (year).
- `collection_tools` contains the programs used to scrape data and reformat word frequency and age of acquisition files for easier use in analysis.

## Collected Features

Below are the "features" and other analytic data that `main.py` collects and stores.

### Collected Features
- `num_tokens`
- `num_sentences`
- `avg_tree_edit_dist`
- `avg_node_depth`
- `max_node_depth`
- `avg_node_clause_depth`
- `max_node_clause_depth`
- `avg_clause_length`
- `clauses_per_sent`
- `sbars_per_sent`
- `pronouns_per_sent`
- `pronouns_per_clause`
- `pronoun_prop_of_leaf_nps`
- `avg_num_np_modifiers`
- `loose_parataxis_per_sent`
- `root_parataxis_per_sent_strict`
- `root_parataxis_per_sent_loose`
- `num_unk`
- `num_words`
- `avg_dependency_distance`
- `max_dependency_distance`
- `avg_sentence_length_by_tok`
- `avg_sentence_length_by_word`
- `avg_words_before_root`
- `num_uniq_words`
- `proportion_uniq`
- `stop_words_per_clause`
- `stop_words_per_sentence`
- `avg_aoa`
- `avg_aoa_uniq`
- `avg_stopless_aoa`
- `avg_stopless_aoa_uniq`
- `avg_word_freq`
- `avg_word_freq_uniq`
- `avg_word_freq_stopless`
- `avg_word_freq_stopless_uniq`

### Collected Analytics
- `date`
- `pres_name`
- `byline`
- `title`
- `benepar_analysis_time`
- `spacy_analysis_time`
- `tree_edit_distance_time`
- `total_file_analysis_time`