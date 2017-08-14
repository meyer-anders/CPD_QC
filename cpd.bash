#!/bin/bash

python get_reads.py &&
python drop_failed_runs.py &&
python parse_runs.py &&
python assign_panel_names.py &&
python drop_panels.py &&
python revise_panel_versions.py &&
python get_categories.py &&
python assign_categories.py &&
python set_keys.py &&
python do_stats.py &&
python new_box_plots.py