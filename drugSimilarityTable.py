'''
Similarity Table
Used to create and manage compound similarity tables
'''
import csv
import json
import os


class SimilarityTable:
    """ 
    Class SimilarityTable

    This class allow a compound to calculate the N top of compounds with 
    the higher similarity value with the compound in question.
    
    Attributes
    - drugs_similarities:   Dictionary that store the top of compounds and their similarity
    - less_value:           Lowest value of the top
    - num_elements:         Number of compounds considered to the top of similarity
    """
    drugs_similarities = {}
    less_value = 0.0
    num_elements = 10

    def __init__(self, drug_id):
        """
        __init__: SimilarityTable class initiator

        Parametros:
        - drug_id: compound id
        """
        self.drug_id = drug_id

    def add_item(self, item_id, item_value):
        """
        add_item:   
            Add an item (compound) to the dictionary that handles the top similarity of the current compound
            Stores the id of the compound and the similarity value
        Parameters:
        - item_id: id of the compound to add
        - item_value: similarity value of the compound to add
        """
        if len(self.drugs_similarities) < self.num_elements or item_value > self.less_value:
            self.drugs_similarities.update({item_id: item_value})
            self.order_dictionary()

    def order_dictionary(self):
        """
        order_dictionary:   
            The dictionary compounds are ordered from greatest to least similarity 
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

    def save_similarity_table(self):
        """
        save_similarity_table:   
        
            Saves in a csv file the similarity dictionary of the compound
            If the file does not exist, it is created and then the similarity dictionary is saved
            If the file exist, the new values will be added
            
        """
        path_similarities = 'similarities_tables.csv'
        if not os.path.isfile(path_similarities):
            with open(path_similarities, mode='w') as similarities_file:
                similarities_writer = csv.writer(similarities_file, delimiter=';', quotechar='"',
                                                 quoting=csv.QUOTE_MINIMAL)
                similarities_writer.writerow(['compound-id', 'similarity-table'])
                similarities_writer.writerow([self.drug_id, json.dumps(self.drugs_similarities)])
        else:
            with open(path_similarities, mode='a', newline='') as similarities_file:
                similarities_writer = csv.writer(similarities_file, delimiter=';', quotechar='"',
                                                 quoting=csv.QUOTE_MINIMAL)
                similarities_writer.writerow([self.drug_id, json.dumps(self.drugs_similarities)])

    @staticmethod
    def load_similarity_table(drug_id):
        """
        load_similarity_table:  
            
            Load the file containing all similarity dictionaries and returns the dictionary
            from the compound needed
            
        Parameters:
        - drug_id: id of the compound whose dictionary is obtained

        Return:
        - Returns the compound dictionary of the compound specified
        """
        path_similarities = 'similarities_tables.csv'
        with open(path_similarities) as similarities_file:
            similarities_reader = csv.DictReader(similarities_file, delimiter=';')
            drug_raw = [row for row in similarities_reader if row['compound-id'] == str(drug_id)]
            drug_id = drug_raw[0]['compound-id']
            drug_similarities = json.loads(drug_raw[0]['similarity-table'])

            drug_loaded = SimilarityTable(drug_id)
            drug_loaded.drugs_similarities = drug_similarities

            return drug_loaded

    def print_dictionary(self):
        """
        print_dictionary:   
            Prints the similarity dictionary, it prints the identifier and the similarity value
            
        """
        for key, value in self.drugs_similarities.items():
            print(key, value)
