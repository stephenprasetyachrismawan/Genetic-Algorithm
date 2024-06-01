from CHAID import Tree
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

# Load the Titanic dataset
df = sns.load_dataset('titanic').dropna(subset=['age', 'fare', 'embarked', 'class', 'who', 'survived'])

# Simplify the dataset
df = df[['age', 'fare', 'embarked', 'class', 'who', 'survived']]
df['embarked'] = df['embarked'].astype(str)
df['class'] = df['class'].astype(str)
df['who'] = df['who'].astype(str)

# Bin continuous variables 'age' and 'fare'
df['age_bin'] = pd.cut(df['age'], bins=5, labels=False)
df['fare_bin'] = pd.cut(df['fare'], bins=5, labels=False)

# Split features and target
X = df[['age_bin', 'fare_bin', 'embarked', 'class', 'who']]
y = df['survived']

# Encode categorical variables as one-hot encoding for the Decision Tree
X_encoded = pd.get_dummies(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.25, random_state=42)

# Create and train Decision Tree model
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predict and calculate accuracy
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Akurasi model Decision Tree: {accuracy:.2f}')

# Create CHAID tree
tree = Tree.from_pandas_df(df, {
    'age_bin': 'ordinal',
    'fare_bin': 'ordinal',
    'embarked': 'nominal',
    'class': 'nominal',
    'who': 'nominal'
}, 'survived')

# Display CHAID tree structure
print("Struktur Tree dari model CHAID:")
tree.print_tree()
