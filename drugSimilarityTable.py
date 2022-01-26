class SimilarityTable:
    drugs_similarities = {}
    less_value = 0.0
    num_elements = 10

    def __init__(self, drug_id):
        self.drug_id = drug_id

    def add_item(self, item_id, item_value):
        if len(self.drugs_similarities) < self.num_elements or item_value > self.less_value:
            self.drugs_similarities.update({item_id: item_value})
            self.order_dictionary()

    def order_dictionary(self):
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

    def print_dictionary(self):
        for key, value in self.drugs_similarities.items():
            print(key, value)
