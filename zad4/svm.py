from sklearn.model_selection import train_test_split
from skopt import BayesSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
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

cls = SVC(C=4.286496948879817, degree=6,
          kernel='rbf', gamma=1.6994661213725195)

# cls = BayesSearchCV(
#     SVC(),
#     {
#         'C': (1e-6, 1e+6, 'log-uniform'),
#         'gamma': (1e-6, 1e+1, 'log-uniform'),
#         'degree': (1, 8),  # integer valued parameter
#         'kernel': ['linear', 'poly', 'rbf'],  # categorical parameter
#     },
#     n_iter=32,
#     cv=10,
#     n_jobs=12,
#     n_points=2
# )

# cls_2 = LinearSVC(max_iter=1500, dual=False, C=0.04)

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
# print(classification_report(Y_test, y_pred))

# cls.fit(vectorizer.transform(X_train), Y_train)

# given_text = input("Your text: ")
# cleaned = clean(given_text)

# outcome = cls.predict(vectorizer.transform([cleaned]))
# print(outcome)

print(cls.score(vectorizer.transform(X_test), Y_test))
# print(cls.best_score_)
# print(cls.best_params_)
# print(cls.best_estimator_)

# 0.5444555444555444 - best score I guess
