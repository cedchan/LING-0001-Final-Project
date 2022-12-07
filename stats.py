import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.decomposition import FactorAnalysis

results = pd.read_csv('results/complete_12-07.csv', index_col=0)
# print(results['num_tokens':])

print(results)

results_data = results['num_tokens':].drop(['num_tokens', 'num_words', 
    'num_sentences', 'num_unk', 'num_uniq_words', 'avg_word_freq_uniq'])
# results_data = results['num_tokens':]
results_std = StandardScaler().fit_transform(results_data).T
# results_std = normalize(results_data).T

# print([np.max(i)-np.min(i) for i in results_std])

# print(results_std.shape)
# fa = FactorAnalysis(n_components=3)
# f = fa.fit(results_std).components_.T
# # print(np.sum(f.T[0]))
# # print(f)

# # print(fa.fit_transform(results_std.T))

# faf = pd.DataFrame(f, index=list(results_data.index), columns=['1', '2', '3'])
# print(faf.nlargest(10, ['1']))



# PCA
pca = PCA(n_components=3).fit(results_std)
print(pca.explained_variance_ratio_)
print(sum(pca.explained_variance_ratio_))
# print(pca.components_.shape)
# print(pca.components_.T)

comps = pd.DataFrame(pca.components_.T, index=list(results_data.index), columns=['1', '2', '3'])
m = comps.abs().nlargest(20, ['1']).index
print(comps.loc[m])

print('num_tokens' in comps.index)

# print('-'*100)

# cov = np.cov(results_std.T)

# evals, evecs = np.linalg.eig(cov)

# print(evecs)
# print(evecs.shape)

# explained_variances = []
# for i in range(len(evals)):
#     explained_variances.append(evals[i] / np.sum(evals))
 
# print(np.sum(explained_variances), '\n', explained_variances)

