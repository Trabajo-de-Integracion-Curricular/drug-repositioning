'''
Tabla de similaridad
Utilizada para la creacion y manejo de tablas de similaridad de compuestos
'''
import csv
import json
import os


class SimilarityTable:
    """ 
    Clase SimilarityTable

    Esta clase permitira a un compuesto calcular el top n de compuestos
    que tienen un mayor valor de similaridad con el compuesto en cuestion.
    
    Atributos
    - drugs_similarities:   Diccionario que almacenara el top de compuestos y su similaridad
    - less_value:           Valor perteneciente al menor valor del top
    - num_elements:         Numero de compuestos que se considerara para el top de similaridad
    """
    drugs_similarities = {}
    less_value = 0.0
    num_elements = 10

    def __init__(self, drug_id):
        """
        __init__: iniciador de la clase SimilarityTable

        Parametros:
        - drug_id: id del compuesto

        """
        self.drug_id = drug_id

    def add_item(self, item_id, item_value):
        """
        add_item:   
            Añade un item (compuesto) al diccionario que maneja el top de similaridad del compuesto actual
            Almacena el id del compuesto y el valor de similaridad para este
        Parametros:
        - item_id: id del compuesto a añadir
        - item_value: valor de similaridad para el compuesto añadido
        """
        if len(self.drugs_similarities) < self.num_elements or item_value > self.less_value:
            self.drugs_similarities.update({item_id: item_value})
            self.order_dictionary()

    def order_dictionary(self):
        """
        order_dictionary:   
            Ordena de mayor a menor similaridad los compuestos que se encuentran en el diccionario
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
            Guarda en un archivo csv el diccionario de similaridad del compuesto
            En caso de que no exista el archivo se lo creara uno nuevo y guardara el diccionario de similaridad
            En caso de que exista se añadiran los nuevos valores sin necesidad de borrar los anteriores 
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
            Carga el archivo que contiene a todos los diccionarios de similaridades y retorna
            unicamente el diccionario del compuesto que se especifica
        Parametros:
        - drug_id: id del compuesto del que se desea obtener su diccionario.

        Return:
        - Retorna el diccionario del compuesto especificado 
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
            Imprime el diccionario de similaridad del compuesto
            Se imprime su identificador y el valor de similaridad
        """
        for key, value in self.drugs_similarities.items():
            print(key, value)
