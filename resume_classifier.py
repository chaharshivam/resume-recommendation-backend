import sys
import os
incomingFileName = sys.argv[1]
filePath = os.path.dirname(os.path.abspath(__file__)) + "/incomingFile/" + incomingFileName
print(filePath)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score
from pandas.plotting import scatter_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

resumeDataSet = pd.read_csv(filePath, encoding='utf-8')
resumeDataSet['cleaned_resume'] = ''
resumeDataSet.head()
# print("Displaying the distinct categories of resume -")
# print(resumeDataSet['Category'].unique())
# print("Displaying the distinct categories of resume and the number of records belonging to each category -")
# print(resumeDataSet['Category'].value_counts())
import seaborn as sns

# plt.figure(figsize=(18, 10), dpi=600)
# plt.xticks(rotation=90)
# sns.countplot(y="Category", data=resumeDataSet, palette='Blues', edgecolor="black", linewidth=2)
# plt.savefig("figurefinal.png")
# plt.show()

from matplotlib.gridspec import GridSpec

targetCounts = resumeDataSet['Category'].value_counts()
targetLabels = resumeDataSet['Category'].unique()
# # Make square figures and axes
# plt.figure(1, figsize=(25, 25))
# the_grid = GridSpec(2, 2)
# #
# #
# cmap = plt.get_cmap('plasma')
# colors = [cmap(i) for i in np.linspace(0, 1, 3)]
# plt.subplot(the_grid[0, 1], aspect=1, title='CATEGORY DISTRIBUTION')
# source_pie = plt.pie(targetCounts, labels=targetLabels, autopct='%1.1f%%', shadow=True)
# plt.show()

import re


def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                        resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText


resumeDataSet['cleaned_resume'] = resumeDataSet.Resume.apply(lambda x: cleanResume(x))
# print(resumeDataSet['cleaned_resume'][31])

import nltk
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud

oneSetOfStopWords = set(stopwords.words('english') + ['``', "''"])
totalWords = []
Sentences = resumeDataSet['Resume'].values
cleanedSentences = ""
for i in range(0, 160):
    cleanedText = cleanResume(Sentences[i])
    cleanedSentences += cleanedText
    requiredWords = nltk.word_tokenize(cleanedText)
    for word in requiredWords:
        if word not in oneSetOfStopWords and word not in string.punctuation:
            totalWords.append(word)

wordfreqdist = nltk.FreqDist(totalWords)
mostcommon = wordfreqdist.most_common(50)
# print(mostcommon)

# wc = WordCloud().generate(cleanedSentences)
# plt.figure(figsize=(15, 15))
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.show()

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import plot_confusion_matrix

var_mod = ['Category']
le = LabelEncoder()
for i in var_mod:
    resumeDataSet[i] = le.fit_transform(resumeDataSet[i])
# print("CONVERTED THE CATEGORICAL VARIABLES INTO NUMERICALS")

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.metrics import recall_score
requiredText = resumeDataSet['cleaned_resume'].values
requiredTarget = resumeDataSet['Category'].values
word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    stop_words='english',
    max_features=1500,
    ngram_range=(3, 5),
    analyzer='word'
)
word_vectorizer.fit(requiredText)
WordFeatures = word_vectorizer.transform(requiredText)

# print("Feature completed .....")

X_train, X_test, y_train, y_test = train_test_split(WordFeatures, requiredTarget, random_state=0, test_size=0.2)
# print(X_train.shape)
# print(X_test.shape)


from sklearn.ensemble import RandomForestClassifier
clf_RF = RandomForestClassifier()
clf_RF.fit(X_train, y_train)
prediction = clf_RF.predict(X_test)
print("\n Classification report for classifier %s:\n%s\n" % (clf_RF, metrics.classification_report(y_test, prediction)))


# print('--------------------------------------------')
#
# clf_KNN = KNeighborsClassifier()
# clf_KNN.fit(X_train, y_train)
# prediction = clf_KNN.predict(X_test)
# print('Accuracy of KNeighbors Classifier on test set: {:.2f}'.format(clf_KNN.score(X_test, y_test)))
# print("\n Classification report for classifier %s:\n%s\n" % (clf_KNN, metrics.classification_report(y_test, prediction)))
#
#
# print('--------------------------------------------')
#
# clf_MNB = MultinomialNB()
# clf_MNB.fit(X_train, y_train)
# prediction = clf_MNB.predict(X_test)
# print('Accuracy of MNB Classifier on test set: {:.2f}'.format(clf_MNB.score(X_test, y_test)))
# print("\n Classification report for classifier %s:\n%s\n" % (clf_MNB, metrics.classification_report(y_test, prediction)))

# print('--------------------------------------------')
#
# from sklearn.ensemble import GradientBoostingClassifier
# clf_GB = GradientBoostingClassifier()
# clf_GB.fit(X_train, y_train)
# prediction = clf_GB.predict(X_test)
# print('Accuracy of GB Classifier on test set: {:.2f}'.format(clf_GB.score(X_test, y_test)))
# print("\n Classification report for classifier %s:\n%s\n" % (clf_GB, metrics.classification_report(y_test, prediction)))
#
#
# print('--------------------------------------------')
#
# from sklearn import svm
# clf_SVM = svm.SVC()
# clf_SVM.fit(X_train, y_train)
# prediction = clf_SVM.predict(X_test)
# print('Accuracy of SVM Classifier on test set: {:.2f}'.format(clf_SVM.score(X_test, y_test)))
# print("\n Classification report for classifier %s:\n%s\n" % (clf_SVM, metrics.classification_report(y_test, prediction)))
#
#
# print('--------------------------------------------')
# from sklearn.linear_model import LogisticRegression
# clf_LR = LogisticRegression()
# clf_LR.fit(X_train, y_train)
# prediction = clf_LR.predict(X_test)
# print('Accuracy of LR Classifier on test set: {:.2f}'.format(clf_LR.score(X_test, y_test)))
# print("\n Classification report for classifier %s:\n%s\n" % (clf_LR, metrics.classification_report(y_test, prediction)))
#
#
# print('--------------------------------------------')
#
# from sklearn.tree import DecisionTreeClassifier
# clf_DT = DecisionTreeClassifier()
# clf_DT.fit(X_train, y_train)
# prediction = clf_DT.predict(X_test)
# print('Accuracy of DT Classifier on test set: {:.2f}'.format(clf_DT.score(X_test, y_test)))
# print("\n Classification report for classifier %s:\n%s\n" % (clf_DT, metrics.classification_report(y_test, prediction)))
#
#
# print('--------------------------------------------')
