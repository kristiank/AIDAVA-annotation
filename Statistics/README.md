# Statistics for AIDAVA annotation task

To download your annotation project, first select your project in Inception. Then choose settings -> Export -> Secondary format -> UIMA CAS XMI (XML 1.0).

Save the exported annotation project(s) zip files into a folder named '"export-zips"' in the root folder, next to the script file.

Run the script with the command 'python statistics_calculator.py'. At the first run it unzips the project files, consecutive executions calculate the statistics.


Running the script takes some minutes at NEMC.


Statistics are compiled per user. The csv files are saved reflecting the username under each projects unzipped folder in the 'export-zips' folder.