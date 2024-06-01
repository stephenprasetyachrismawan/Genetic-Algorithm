import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Data: Inisialisasi dataset
data = pd.DataFrame({
    'age': ['youth', 'youth', 'middle_aged', 'senior', 'senior', 'senior', 'middle_aged', 'youth', 'youth', 'senior', 'youth', 'middle_aged', 'middle_aged', 'senior'],
    'income': ['high', 'high', 'high', 'medium', 'low', 'low', 'low', 'medium', 'low', 'medium', 'medium', 'medium', 'high', 'medium'],
    'student': ['no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no'],
    'credit_rating': ['fair', 'excellent', 'fair', 'fair', 'fair', 'excellent', 'excellent', 'fair', 'fair', 'fair', 'excellent', 'excellent', 'fair', 'excellent'],
    'buys_computer': ['no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'no']
})

# Fungsi untuk menghitung entropy
def entropy(target_col):
    elements, counts = np.unique(target_col, return_counts=True)
    entropy = np.sum([(-counts[i]/np.sum(counts)) * np.log2(counts[i]/np.sum(counts)) for i in range(len(elements))])
    return entropy

# Fungsi untuk menghitung Information Gain
def InfoGain(data, split_attribute_name, target_name="buys_computer"):
    # Total entropy
    total_entropy = entropy(data[target_name])
    
    # Nilai entropy dari variabel yang akan dibagi
    vals, counts = np.unique(data[split_attribute_name], return_counts=True)
    Weighted_Entropy = np.sum([(counts[i]/np.sum(counts)) * entropy(data.where(data[split_attribute_name]==vals[i]).dropna()[target_name]) for i in range(len(vals))])
    
    # Information Gain
    Information_Gain = total_entropy - Weighted_Entropy
    return Information_Gain

# Fungsi untuk membuat decision tree
def ID3(data, originaldata, features, target_attribute_name="buys_computer", parent_node_class = None):
    # Basis cases:
    if len(np.unique(data[target_attribute_name])) <= 1:
        return np.unique(data[target_attribute_name])[0]
    elif len(data) == 0:
        return np.unique(originaldata[target_attribute_name])[np.argmax(np.unique(originaldata[target_attribute_name], return_counts=True)[1])]
    elif len(features) == 0:
        return parent_node_class
    else:
        # Node default ini
        parent_node_class = np.unique(data[target_attribute_name])[np.argmax(np.unique(data[target_attribute_name], return_counts=True)[1])]
        
        # Item dengan Information Gain terbesar
        item_values = [InfoGain(data, feature, target_attribute_name) for feature in features]
        best_feature_index = np.argmax(item_values)
        best_feature = features[best_feature_index]
        
        # Struktur pohon
        tree = {best_feature:{}}
        
        # Mengurangi fitur yang terbaik dari dataset
        features = [i for i in features if i != best_feature]
        
        # Membangun sub pohon
        for value in np.unique(data[best_feature]):
            sub_data = data.where(data[best_feature] == value).dropna()
            subtree = ID3(sub_data, originaldata, features, target_attribute_name, parent_node_class)
            tree[best_feature][value] = subtree
        
        return tree
    
# Membagi data menjadi data train dan data test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Fungsi untuk melakukan prediksi dengan decision tree
def predict(query, tree, default = 'yes'):
    for key in list(query.keys()):
        if key in list(tree.keys()):
            try:
                result = tree[key][query[key]] 
            except:
                return default

            result = tree[key][query[key]]
            if isinstance(result, dict):
                return predict(query, result)
            else:
                return result

# Membangun pohon menggunakan data train
features = train_data.columns[:-1].tolist()
tree = ID3(train_data, train_data, features)

# Menggunakan pohon untuk membuat prediksi pada data test
test_data['predicted'] = test_data.apply(lambda x: predict(x.to_dict(), tree), axis=1)

# Menampilkan hasil prediksi
print(test_data[['buys_computer', 'predicted']])

