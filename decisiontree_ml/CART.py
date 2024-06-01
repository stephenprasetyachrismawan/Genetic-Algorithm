# Mengimpor library yang diperlukan
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Memuat dataset iris
data = load_iris()
X = data.data  # fitur-fitur dari dataset
y = data.target  # label kelas dari dataset

# Membagi dataset menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)  # 30% data untuk testing

# Membuat model Decision Tree dengan algoritma CART
model = DecisionTreeClassifier(criterion='gini')  # 'gini' menunjukkan penggunaan impurity measure Gini untuk CART

# Melatih model dengan data latih
model.fit(X_train, y_train)

# Memprediksi label untuk data uji
y_pred = model.predict(X_test)

# Menghitung dan mencetak akurasi dari model
accuracy = accuracy_score(y_test, y_pred)
print(f"Akurasi model Decision Tree: {accuracy * 100:.2f}%")

