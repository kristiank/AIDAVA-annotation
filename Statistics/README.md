# Statistics for AIDAVA annotation task

## Exporting the annotated use-cases as Inception projects

To download your annotation projects, first open your project in Inception. Then choose from the menus:
'Settings -> Export -> Secondary format -> UIMA CAS XMI (XML 1.0)'

Inception generates the export (takes up to 15 minutes at NEMC), a link appears on the right pane when ready to download.

Save the exported annotation project(s) zip files into the '"export-zips"' folder, next to the statistics script file. You don't need to unzip the file.


## Running the statistics script

Run the script with the command 'python statistics_calculator.py'.

If any new, unzipped files are present, the script unzips the project files and you need to run the script again to produce statistics. Consecutively running the script only calculates the statistics and does not unzip the files. To unzip a project afresh simply delete the corresponding unzipped project folder.

Running the script takes approximately a minute at NEMC.

## Generated statistics

Statistics are compiled per each annotator and corresponding CSV files are saved reflecting their username. Two statistics are compiled, one for annotated concept frequencies and another for annotated relations/predicates. The CSV files are saved under each projects' unzipped folder in the 'export-zips' folder, e.g.:

Statistics/
+ export-zips/
++ projectA/
+++ concept_results-user1.csv
+++ concept_results-user2.csv
+++ relation_results-user1.csv
+++ relation_results-user2.csv

If statistics are not needed for some users, the username can be added to the 'user_blacklist' list in the script.

## Dependencies

The script has dependencies to 'Pandas' and 'dkpro-cassis'. Install them with the following commands:
'''
pip install dkpro-cassis
pip install pandas
'''