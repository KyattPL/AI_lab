from sklearn.model_selection import train_test_split
from skopt import BayesSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

from cleanup import get_data, clean

labels, descs = get_data()

X_train, X_test, Y_train, Y_test = train_test_split(
    descs, labels, test_size=0.1)

batch_size = len(Y_train) // 10

labels_batched = []
descs_batched = []

i = 0
temp = []
for label in Y_train:
    temp.append(label)
    i += 1
    if i == batch_size:
        labels_batched.append(temp)
        i = 0
        temp = []

i = 0
temp = []
for desc in X_train:
    temp.append(desc)
    i += 1
    if i == batch_size:
        descs_batched.append(temp)
        i = 0
        temp = []


vectorizer = TfidfVectorizer(decode_error="ignore", analyzer="word", max_features=3000,
                             strip_accents='ascii', max_df=0.1)

vectorizer.fit(X_train)

# cls = BayesSearchCV(
#     MultinomialNB(),
#     {
#         'alpha': (1e-5, 1e+1, 'log-uniform')
#     },
#     n_iter=32,
#     cv=10,
#     n_jobs=12,
#     n_points=2
# )

cls = MultinomialNB(alpha=0.21128133153466064)

scores_avg = 0

for i in range(10):
    xs = []
    ys = []

    for (index, label) in enumerate(labels_batched):
        if index != i:
            ys += label
    for (index, desc) in enumerate(descs_batched):
        if index != i:
            xs += desc

    xtest = descs_batched[i]
    ytest = labels_batched[i]

    cls.fit(vectorizer.transform(xs), ys)
    y_pred = cls.predict(vectorizer.transform(xtest))
    score = accuracy_score(ytest, y_pred)
    scores_avg += score

print(scores_avg / 10)

# cls.fit(vectorizer.transform(X_train), Y_train)

print(cls.score(vectorizer.transform(X_test), Y_test))

# print(cls.best_score_)
# print(cls.best_params_)
# print(cls.best_estimator_)
