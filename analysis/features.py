from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import RFE
import numpy as np
from numpy.linalg import norm
import pandas as pd
from sklearn.preprocessing import StandardScaler
from math import sqrt

results = pd.read_csv('results/complete_12-14.csv', header=0, index_col=0).T

ignore = [
    'num_tokens',
    'num_sentences',
    'num_paratactic_clauses',
    'num_unk',
    'num_words',
    'num_uniq_words',
    
    # 'avg_word_freq',
    # 'avg_word_freq_uniq',
    # 'avg_word_freq_stopless',
    # 'avg_word_freq_stopless_uniq'
]

results_data = results['num_tokens':].drop(ignore)
results_std = StandardScaler().fit_transform(results_data).T

# PCA MANUAL
n = 3

cov = np.cov(results_std.T)
evals, evecs = np.linalg.eig(cov)
evecs_pd = pd.DataFrame(evecs[:, 0:n], index=list(results_data.index),
                        columns=['PC' + str(x + 1) for x in range(n)])
top_n = evecs_pd.abs().nlargest(40, ['PC1']).index

print(evecs_pd.loc[top_n])

variance = []
for i in range(len(evals)):
    variance.append(evals[i] / np.sum(evals))

print("Variance: ", variance[0:n])
print("Accounts for ", sum(variance[0:n]))
print("Cutoff:", sqrt(1 / len(evecs_pd)))

# print('-' * 100)
# print('Decision Tree Classifier\n')

# rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=5)
# rfe.fit(results_std, list(results.loc['year']))
# for i in range(results_std.shape[1]):
#     if rfe.support_[i]:
#         print(list(results_data.index)[i])

# print('-' * 100)
# print('Gradient Boosting Classifier\n')

# rfe = RFE(estimator=GradientBoostingClassifier(), n_features_to_select=5)
# rfe.fit(results_std, list(results.loc['year']))
# for i in range(results_std.shape[1]):
#     if rfe.support_[i]:
#         print(list(results_data.index)[i])

# print('-' * 100)
# print('KBest\n')

# selector = SelectKBest(mutual_info_regression, k=5)
# selector.fit(results_std, list(results.loc['year']))
# for i in range(results_std.shape[1]):
#     if selector.get_support()[i]:
#         print(list(results_data.index)[i])