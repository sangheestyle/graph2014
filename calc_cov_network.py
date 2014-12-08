import json
import numpy as np
import matplotlib.pyplot as plt
from brain_data import BrainData


raw_data = json.load(open('data/data_v2.json'))
b1 = BrainData(raw_data)
b1.calc_covariance(method="graphlassocv", values="cov")
cov_ = b1.model.covariance_

plt.figure(figsize=(8, 8))
vmax = cov_.max()
plt.imshow(cov_, interpolation='nearest', vmin=-vmax, vmax=vmax, cmap=plt.cm.RdBu_r)
plt.xticks(())
plt.yticks(())
plt.title('covariance by GraphLassoCV()')

plt.figure(figsize=(4, 3))
plt.axes([.2, .15, .75, .7])
plt.plot(b1.model.cv_alphas_, np.mean(b1.model.grid_scores, axis=1), 'o-')
plt.axvline(b1.model.alpha_, color='.5')
plt.title('Model selection')
plt.ylabel('Cross-validation score')
plt.xlabel('alpha')

plt.show()
