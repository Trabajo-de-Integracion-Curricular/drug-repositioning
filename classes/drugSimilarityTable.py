"""
Similarity Table
Create and manage compound similarity tables
"""
import json
import os
import pandas as pd


class SimilarityTable:
    """ 
    Class SimilarityTable

    This class allows to calculate the top N similar compounds for a given drug.
    
    Attributes
    - drugs_similarities:       Dictionary that store the top of compounds and their similarity
    - less_value:               Lowest value of the top
    - num_elements:             Number of compounds considered to the top of similarity
    - similarity_threshold:     Minimum threshold to consider for similarity
    - drug_id:                  Unique identifier of the drug
    """
    drugs_similarities = {}
    less_value = 0.0
    num_elements = 10
    similarity_threshold = 0.55

    def __init__(self, drug_id):
        """
        __init__: SimilarityTable class initiator

        Parameters:
        - drug_id: drug compound id
        """
        self.drug_id = drug_id

    def add_item(self, item_id, item_value):
        """
        add_item:   
            Adds an item (drug) to the dictionary that handles the top similarity of the current compound
            Stores the id of the drug and the similarity value

        Parameters:
        - item_id: id of the compound to add
        - item_value: similarity value of the compound to add
        """
        if item_value >= self.similarity_threshold and (
                len(self.drugs_similarities) < self.num_elements or item_value > self.less_value):
            self.drugs_similarities.update({item_id: item_value})
            self.order_dictionary()

    def order_dictionary(self):
        """
        order_dictionary:   
            The drug dictionary is ordered from highest to lowest similarity value
        """
        sorted_similarities = sorted(self.drugs_similarities.items(), key=lambda x: x[1], reverse=True)
        new_drugs_similarities = {}
        dictionary_len = len(sorted_similarities)

        if dictionary_len < self.num_elements:
            for i in range(dictionary_len):
                new_drugs_similarities[sorted_similarities[i][0]] = sorted_similarities[i][1]
                if i == dictionary_len - 1:
                    self.less_value = sorted_similarities[i][1]
        else:
            for i in range(self.num_elements):
                new_drugs_similarities[sorted_similarities[i][0]] = sorted_similarities[i][1]
                if i == self.num_elements - 1:
                    self.less_value = sorted_similarities[i][1]

        self.drugs_similarities = new_drugs_similarities

    def save_similarity_table(self, radius):
        """
        save_similarity_table:
            Saves in a csv file the similarity dictionary of the drug
            If the file does not exist, it is created and then the similarity dictionary is saved
            If the file exist, the new values will be added
        """
        path_similarities = '../data/similarities_tables_radius_{}.csv'.format(radius)
        data_to_save = {'sanitize-id': [self.drug_id], 'similarity-table': [json.dumps(self.drugs_similarities)]}

        similarities_df = pd.DataFrame(data_to_save)
        similarities_df.to_csv(path_similarities, sep=';', mode='a', index=False,
                               header=not os.path.exists(path_similarities), encoding='utf-8')

    @staticmethod
    def load_similarity_table(drug_id, radius):
        """
        load_similarity_table:
            Loads the file containing all similarity dictionaries and returns the dictionary
            from the compound needed
            
        Parameters:
        - drug_id: id of the compound whose dictionary is obtained

        Return:
        - Returns the Similarity Table of the compound specified
        """
        path_similarities = '../data/similarities_tables_radius_{}.csv'.format(radius)
        similarities_tables = pd.read_csv(path_similarities, delimiter=';')
        similarities_tables.set_index("sanitize-id", inplace=True)

        drug_loaded = SimilarityTable(drug_id)
        drug_loaded.drugs_similarities = json.loads(similarities_tables.loc[drug_id]['similarity-table'])
        return drug_loaded

    def print_dictionary(self):
        """
        print_dictionary:   
            Prints the similarity dictionary, it prints the identifier and the similarity value
        """
        print(json.dumps(self.drugs_similarities, sort_keys=False, indent=4))
