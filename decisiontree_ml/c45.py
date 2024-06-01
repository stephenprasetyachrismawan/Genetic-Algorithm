# Mengimpor library yang diperlukan
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Memuat dataset iris
data = load_iris()
X = data.data  # fitur-fitur dari dataset
y = data.target  # label kelas dari dataset

# Membagi dataset menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Membuat model Decision Tree dengan kriteria 'entropy' yang mirip dengan C4.5
model = DecisionTreeClassifier(criterion='entropy')

# Melatih model dengan data latih
model.fit(X_train, y_train)

# Memprediksi label untuk data uji
y_pred = model.predict(X_test)

# Menghitung dan mencetak akurasi dari model
accuracy = accuracy_score(y_test, y_pred)
print(f"Akurasi model: {accuracy * 100:.2f}%")

