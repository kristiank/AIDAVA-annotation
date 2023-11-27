from cassis import *
import os
import pandas as pd
#import nltk
#nltk.download('punkt')
#from nltk.tokenize import word_tokenize
import zipfile


def unzip_all(zip_folder, extract_to):
    with zipfile.ZipFile(zip_folder, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            file_path_parts = file_info.filename.split('/')
            extract_path = os.path.join(extract_to, *file_path_parts)
            os.makedirs(os.path.dirname(extract_path), exist_ok=True)
            with zip_ref.open(file_info) as file:
                with open(extract_path, 'wb') as output_file:
                    output_file.write(file.read())
        #print(f"Successfully extracted {zip_folder} to {extract_to}")

def unzip_all_in_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_file_path = os.path.join(root, file)
                extract_to = os.path.join(root, file.split('.')[0])
                unzip_all(zip_file_path, extract_to)
                # Recursively unzip files in the subfolder
                unzip_all_in_directory(extract_to)

def unzip_all_in_zip(zip_file_path):
    if zip_file_path.lower().endswith('.zip'):
        extract_to = zip_file_path[0:-4]
        unzip_all(zip_file_path, extract_to)
        # Recursively unzip files in the subfolder
        unzip_all_in_directory(extract_to)
        print("Unzipped a project. Run the script again to calculate its statistics.")
    else:
        print("Not a zip file!")


# Compile a report for the exported project directory
def report(project_folder):
    # Initialize dictionaries to store concepts and pairs for all files
    per_user_data = {}

    # Go through the UIMA xmi-file in the specified directory
    annotation_xml_directory = os.path.join(project_folder, 'annotation')
    if not os.path.isdir(annotation_xml_directory):
        print("Skipping folder. Does not seem to be an Inception UIMA export: " + annotation_xml_directory)
        return

    for annotated_file_directory in os.scandir(annotation_xml_directory):
        if not annotated_file_directory.is_dir():
            continue
        # Collect statistics per user
        for user in os.scandir(annotated_file_directory):
            if not user.is_dir():
                continue
            if user.name in user_blacklist:
                continue
            if user.name not in per_user_data:
                per_user_data[user.name] = {"concept_data":             {},
                                            "begin_end_pairs":          [],
                                            "relation_data":            {},
                                            "relation_begin_end_pairs": []}
            
            file_path = os.path.join(user.path, user.name + ".xmi")
            
            xml_file = os.path.join(user.path, 'TypeSystem.xml')
            with open(xml_file, 'rb') as fxml:
                typesystem = load_typesystem(fxml)
            with open(file_path, 'rb') as fxmi:
                cas = load_cas_from_xmi(fxmi, typesystem = typesystem)

                # Iterate through the XML and extract concepts and begin-end pairs
                for surface in cas.select('webanno.custom.CustomMCN'):
                    concept = surface.Concept
                    begin = surface.begin
                    end = surface.end
                    if concept is not None:
                        if concept not in per_user_data[user.name]["concept_data"]:
                            per_user_data[user.name]["concept_data"][concept] = []
                        per_user_data[user.name]["concept_data"][concept].append((begin, end))
                    per_user_data[user.name]["begin_end_pairs"].append((begin, end))

                # Iterate through the XML and extract relations and begin-end pairs
                for surface in cas.select('webanno.custom.Relation'):
                    relation = surface.Relation
                    begin = surface.begin
                    end = surface.end

                    if relation is not None:
                        if relation not in per_user_data[user.name]["relation_data"]:
                            per_user_data[user.name]["relation_data"][relation] = []#set()
                        per_user_data[user.name]["relation_data"][relation].append((begin, end))#add((begin, end))

                    per_user_data[user.name]["relation_begin_end_pairs"].append((begin, end))
    

    # Print the collected statistics per user
    for user in per_user_data:
        concept_df = pd.DataFrame(per_user_data[user]["concept_data"].items(), columns=["Concept", "Begin-End Pairs"])
        concept_df["Number of Instances"] = concept_df["Begin-End Pairs"].apply(len)
        concept_df = concept_df.drop("Begin-End Pairs", axis=1)

        # Create a single DataFrame for relations
        relation_df = pd.DataFrame(per_user_data[user]["relation_data"].items(), columns=["Relation", "Begin-End Pairs"])
        relation_df["Number of Instances"] = relation_df["Begin-End Pairs"].apply(len)
        relation_df = relation_df.drop("Begin-End Pairs", axis=1)

        # Count the distinct concepts and begin-end pairs for all files
        count_distinct_concepts = len(concept_df)
        count_concept_instances = concept_df['Number of Instances'].sum()

        # Count the distinct relations and begin-end pairs for all files
        count_distinct_relations = len(relation_df)
        count_relation_instances = relation_df['Number of Instances'].sum()

        # Save the results to CSV files
        concept_df.to_csv(os.path.join(project_folder, 'concept_results-'+user+'.csv'), index=False)
        relation_df.to_csv(os.path.join(project_folder, 'relation_results-'+user+'.csv'), index=False)

        print(f'Analyzed for user: "' + user + '" file: ' + project_folder.name)
        print(f'total number of distinct concepts: {count_distinct_concepts}')
        print(f'total number of instances of concepts: {count_concept_instances}')
        print(f'total number of distinct relations: {count_distinct_relations}')
        print(f'total number of instances of relations: {count_relation_instances}')

    return #concept_df, relation_df, count_distinct_concepts, count_concept_instances, count_distinct_relations, count_relation_instances


def count_tokens_in_file(directory_path, language):
    num_tokens = 0
    num_file = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                num_file += 1
                text = file.read()
                tokens = word_tokenize(text, language=language) # Tokenize using the German language model
                num_tokens += len(tokens)
    if num_file == 0:
        return 0
    else:
        avg_count = num_tokens / num_file
    print(f'average number of tokens within documents: {avg_count}')
    return avg_count

if __name__ == "__main__":

    #export the whole project in Inception and put its path at export_directory
    export_directory = './export-zips/'

    if not os.path.exists(export_directory):
        exit("Could not find the export folder ('"+export_directory+"'). Make sure it exists and run this script again.")
    
    user_blacklist = ['INITIAL_CAS', 'kristian', 'admin']


    with os.scandir(export_directory) as it:
        for export_folder in it:
            if export_folder.is_file() and export_folder.name.endswith('.zip'):
                if os.path.isdir(export_folder.path[0:-4]):
                    print("Not unzipping. Delete folder to unzip file again: " + export_folder.name)
                else:
                    unzip_all_in_zip(export_folder.path)
                    print("Unzipped a new project. Run the script again to compile its statistics!")
            if export_folder.is_dir():
                print("Hold on, we're counting the statistics...")
                report(export_folder)
                #report(type_system_directory_path, unzip_directory, user_name, 'annotation')#the other type of docs in mug is: ST_BEHANDLUNGSBRIEF_Patien


    ## count the average number of tokens within narratives:
    ## directory including the input text documents
    #doc_directory_path = '/home/sareh/Data/Inception/Documents for Annotation/ST_BEHANDLUNGSBRIEF/'  # PATHO_HISTOLOGIE/'
    ## language of the input docs to count the number of the tokens
    #doc_language = 'german'
    #count_tokens_in_file(doc_directory_path, doc_language)

