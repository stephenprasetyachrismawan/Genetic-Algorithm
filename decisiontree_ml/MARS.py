# Mengimpor library yang diperlukan
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from pyearth import Earth

# Memuat dataset iris
data = load_iris()
X = data.data
y = data.target

# Membagi data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Membuat model MARS
mars_model = Earth()
mars_model.fit(X_train, y_train)

# Menggunakan model MARS untuk transformasi fitur
X_train_transformed = mars_model.transform(X_train)
X_test_transformed = mars_model.transform(X_test)

# Membuat model Decision Tree
dt_classifier = DecisionTreeClassifier()
dt_classifier.fit(X_train_transformed, y_train)

# Melakukan prediksi pada data uji
y_pred = dt_classifier.predict(X_test_transformed)

# Menghitung dan mencetak akurasi dari model
accuracy = accuracy_score(y_test, y_pred)
print(f"Akurasi model Decision Tree dengan fitur yang ditransformasi oleh MARS: {accuracy:.2f}")

