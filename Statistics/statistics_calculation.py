import xml.etree.ElementTree as ET
import os
import pandas as pd
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# layer_definition
layer_concept_definition = './/webanno.custom.CustomMCN'
layer_relation_definition = './/webanno.custom.Relation'

def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def report(directory_path):

    # Initialize dictionaries to store concepts and pairs for all files
    concept_data = {}
    begin_end_pairs = []

    relation_data  = {}

    relation_begin_end_pairs = []

    # Loop through all .xml files in the specified directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory_path, filename)

            # Parse the XML file
            root = parse_xml_file(file_path)

            # Iterate through the XML and extract concepts and begin-end pairs
            for custom_mcn in root.findall(layer_concept_definition):
                concept = custom_mcn.get('Concept')
                begin = custom_mcn.get('begin')
                end = custom_mcn.get('end')

                if concept is not None:
                    if concept not in concept_data:
                        concept_data[concept] = set()
                    concept_data[concept].add((begin, end))

                begin_end_pairs.append((begin, end))


            # Iterate through the XML and extract relations and begin-end pairs
            for custom_mcn in root.findall(layer_relation_definition):
                relation = custom_mcn.get('Relation')
                begin = custom_mcn.get('begin')
                end = custom_mcn.get('end')

                if relation is not None:
                    if relation not in relation_data:
                        relation_data[relation] = set()
                    relation_data[relation].add((begin, end))

                relation_begin_end_pairs.append((begin, end))


    concept_df = pd.DataFrame(concept_data.items(), columns=["Concept", "Begin-End Pairs"])
    concept_df["Number of Instances"] = concept_df["Begin-End Pairs"].apply(len)
    concept_df = concept_df.drop("Begin-End Pairs", axis=1)

    # Create a single DataFrame for relations
    relation_df = pd.DataFrame(relation_data.items(), columns=["Relation", "Begin-End Pairs"])
    relation_df["Number of Instances"] = relation_df["Begin-End Pairs"].apply(len)
    relation_df = relation_df.drop("Begin-End Pairs", axis=1)

    # Count the distinct concepts and begin-end pairs for all files
    count_distinct_concepts = len(concept_df)
    count_concept_instances = len(begin_end_pairs)

    # Count the distinct relations and begin-end pairs for all files
    count_distinct_relations = len(relation_df)
    count_relation_instances = len(relation_begin_end_pairs)

    # Save the results to CSV files
    concept_df.to_csv('concept_results.csv', index=False)
    relation_df.to_csv('relation_results.csv', index=False)

    print(f'total number of distinct concepts: {count_distinct_concepts}')
    print(f'total number of instances of concepts: {count_concept_instances}')
    print(f'total number of distinct relations: {count_distinct_relations}')
    print(f'total number of instances of relations: {count_relation_instances}')

    return concept_df, relation_df, count_distinct_concepts, count_concept_instances, count_distinct_relations, count_relation_instances

def count_tokens_in_file(directory_path, language):
    num_tokens = 0
    num_file = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                num_file += 1
                text = file.read()
                tokens = word_tokenize(text, language=language)  # Tokenize using the German language model
                num_tokens += len(tokens)
    if num_file == 0:
        return 0
    else:
        avg_count = num_tokens / num_file
    print(f'average number of tokens within documents: {avg_count}')
    return avg_count



if __name__ == "__main__":

    # change values of xml_directory_path, doc_directory_path and doc_language

    # directory including the annotated documents (i.e., xml files)
    xml_directory_path = '/home/sareh/Data/Inception/'
    # directory including the input text documents
    doc_directory_path = '/home/sareh/Data/Inception/Documents for Annotation/ST_BEHANDLUNGSBRIEF/'  # PATHO_HISTOLOGIE/'
    # language of the input docs to count the number of the tokens
    doc_language = 'german'

    # calculate the number of distinct concepts and relations along with their instances
    report(xml_directory_path)
    # count the average number of tokens within narratives
    count_tokens_in_file(doc_directory_path, doc_language)










