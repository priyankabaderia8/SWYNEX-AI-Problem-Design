import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. Dataset load
df = pd.read_excel("manufacturing_b2b_dataset.xlsx", sheet_name="Orders & Reviews")
print(f"Dataset Loaded: {df.shape[0]} reviews")

# 2. Text Classification Setup
X = df['Client Review']
y = df['Review Sentiment']

vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# 3. Model Train
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 4. Evaluation
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"\n--- RESULT ---")
print(f"Accuracy: {acc*100:.2f}%")
print(classification_report(y_test, pred))

# 5. Business Dashboard Logic
positive_pct = (df['Review Sentiment'] == 'Positive').mean() * 100
print(f"\nBusiness Dashboard: {positive_pct:.1f}% Positive, {100-positive_pct:.1f}% Negative/Neutral")
print("Task ke liye Success Criteria: Accuracy > 85%")