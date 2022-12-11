import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.decomposition import FactorAnalysis

results = pd.read_csv('results/complete_12-10.csv', header=0, index_col=0).T

results_data = results['num_tokens':].drop(['num_tokens', 'num_words', 'num_sentences', 'num_unk', 'num_uniq_words', 'avg_word_freq_uniq'])
results_std = StandardScaler().fit_transform(results_data).T

# # PCA SKLEARN
# pca = PCA(n_components=3).fit(results_std)
# print(pca.explained_variance_ratio_)
# print(sum(pca.explained_variance_ratio_))

# comps = pd.DataFrame(pca.components_.T, index=list(results_data.index), columns=['1', '2', '3'])
# m = comps.abs().nlargest(20, ['1']).index
# print(comps.loc[m])

# PCA MANUAL
n = 3

cov = np.cov(results_std.T)
evals, evecs = np.linalg.eig(cov)
evecs_pd = pd.DataFrame(evecs[:, 0:n], index=list(results_data.index), columns=['PC' + str(x + 1) for x in range(n)])
top_n = evecs_pd.abs().nlargest(20, ['PC1']).index
# print(evecs[0:10,0:3])
print(evecs_pd.loc[top_n])

variance = []
for i in range(len(evals)):
    variance.append(evals[i] / np.sum(evals))
 
print(variance[0:n])
print(sum(variance[0:n]))


from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron

print('-'*100)

rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=5)
rfe.fit(results_std, list(results.loc['year']))
for i in range(results_std.shape[1]):
    if rfe.support_[i]:
        print(list(results_data.index)[i])

print('-'*100)

rfe = RFE(estimator=GradientBoostingClassifier(), n_features_to_select=5)
rfe.fit(results_std, list(results.loc['year']))
for i in range(results_std.shape[1]):
    if rfe.support_[i]:
        print(list(results_data.index)[i])

print('-' * 100)

from sklearn.feature_selection import SelectKBest, mutual_info_regression
selector = SelectKBest(mutual_info_regression, k=5)
selector.fit(results_std, list(results.loc['year']))
for i in range(results_std.shape[1]):
    if selector.get_support()[i]:
        print(list(results_data.index)[i])

#                                   PC1       PC2       PC3
# avg_word_freq_stopless       0.841776 -0.172820 -0.451594
# avg_word_freq_stopless_uniq  0.430487 -0.049878  0.878628
# avg_tree_edit_dist_adjacent -0.177938 -0.212407  0.073391
# max_dependency_distance     -0.171111 -0.882417 -0.033702
# avg_sentence_length_by_tok  -0.095837 -0.019925  0.003547
# avg_sentence_length_by_word -0.094050 -0.010420  0.002086
# avg_clause_length           -0.076354 -0.013714 -0.017228
# stop_words_per_sentence     -0.062587  0.020502 -0.001010
# max_node_depth              -0.061192 -0.181164  0.060793
# avg_words_before_root       -0.048693  0.030415 -0.013727
# avg_node_depth              -0.027916  0.049915 -0.013040
# stop_words_per_clause       -0.026249  0.073279 -0.027414
# avg_word_freq               -0.025914  0.027505  0.002175
# avg_num_np_modifiers        -0.025160  0.062392 -0.018430
# clauses_per_sent            -0.024682  0.070718 -0.020704
# avg_stopless_aoa_min        -0.024245  0.078007 -0.027504
# pronouns_per_sent           -0.023914  0.071301 -0.016475
# sbars_per_sent              -0.023459  0.074548 -0.022595
# avg_stopless_aoa_uniq_min   -0.023426  0.077800 -0.031154
# avg_aoa_uniq_min            -0.023252  0.077756 -0.035103
# [0.7973247439643265, 0.14004069634710647, 0.03231802141848286]
# 0.9696834617299158
# ----------------------------------------------------------------------------------------------------
# RFE with DecisionTreeClassifier
# 
# avg_tree_edit_dist_adjacent
# root_parataxis_per_sent_loose
# avg_words_before_root
# avg_stopless_aoa_uniq_min
# avg_word_freq_stopless_uniq
# ----------------------------------------------------------------------------------------------------
# RFE with GradientBoostingClassifier
# 
# avg_tree_edit_dist_adjacent
# max_node_clause_depth
# max_dependency_distance
# proportion_uniq
# stop_words_per_sentence
# ----------------------------------------------------------------------------------------------------
# SelectKBest with mutual_info_regression
# 
# avg_tree_edit_dist_adjacent
# avg_sentence_length_by_tok
# avg_sentence_length_by_word
# stop_words_per_sentence
# avg_word_freq_stopless