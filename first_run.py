import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn import covariance


raw_data = json.load(open('data/data_v2.json'))
data = raw_data['subj1_16regions_1845time']

# model = covariance.GraphLasso(alpha=0.001)
model = covariance.GraphLassoCV()
model.fit(data)
cov_ = model.covariance_

plt.figure(figsize=(8, 8))
vmax = cov_.max()
plt.imshow(cov_, interpolation='nearest', vmin=-vmax, vmax=vmax, cmap=plt.cm.RdBu_r)
plt.xticks(())
plt.yticks(())
plt.title('covariance by GraphLassoCV()')

plt.figure(figsize=(4, 3))
plt.axes([.2, .15, .75, .7])
plt.plot(model.cv_alphas_, np.mean(model.grid_scores, axis=1), 'o-')
plt.axvline(model.alpha_, color='.5')
plt.title('Model selection')
plt.ylabel('Cross-validation score')
plt.xlabel('alpha')

plt.show()
