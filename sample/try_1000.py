"""
======================================
Sparse inverse covariance estimation
======================================

Using the GraphLasso estimator to learn a covariance and sparse precision
from a small number of samples.

To estimate a probabilistic model (e.g. a Gaussian model), estimating the
precision matrix, that is the inverse covariance matrix, is as important
as estimating the covariance matrix. Indeed a Gaussian model is
parametrized by the precision matrix.

To be in favorable recovery conditions, we sample the data from a model
with a sparse inverse covariance matrix. In addition, we ensure that the
data is not too much correlated (limiting the largest coefficient of the
precision matrix) and that there a no small coefficients in the
precision matrix that cannot be recovered. In addition, with a small
number of observations, it is easier to recover a correlation matrix
rather than a covariance, thus we scale the time series.

Here, the number of samples is slightly larger than the number of
dimensions, thus the empirical covariance is still invertible. However,
as the observations are strongly correlated, the empirical covariance
matrix is ill-conditioned and as a result its inverse --the empirical
precision matrix-- is very far from the ground truth.

If we use l2 shrinkage, as with the Ledoit-Wolf estimator, as the number
of samples is small, we need to shrink a lot. As a result, the
Ledoit-Wolf precision is fairly close to the ground truth precision, that
is not far from being diagonal, but the off-diagonal structure is lost.

The l1-penalized estimator can recover part of this off-diagonal
structure. It learns a sparse precision. It is not able to
recover the exact sparsity pattern: it detects too many non-zero
coefficients. However, the highest non-zero coefficients of the l1
estimated correspond to the non-zero coefficients in the ground truth.
Finally, the coefficients of the l1 precision estimate are biased toward
zero: because of the penalty, they are all smaller than the corresponding
ground truth value, as can be seen on the figure.

Note that, the color range of the precision matrices is tweeked to
improve readibility of the figure. The full range of values of the
empirical precision is not displayed.

The alpha parameter of the GraphLasso setting the sparsity of the model is
set by internal cross-validation in the GraphLassoCV. As can be
seen on figure 2, the grid to compute the cross-validation score is
iteratively refined in the neighborhood of the maximum.
"""
print(__doc__)
# author: Gael Varoquaux <gael.varoquaux@inria.fr>
# License: BSD 3 clause
# Copyright: INRIA

import numpy as np
from scipy import linalg
from sklearn.datasets import make_sparse_spd_matrix
from sklearn.covariance import GraphLassoCV, ledoit_wolf
import matplotlib.pyplot as plt

##############################################################################
# Generate the data
n_samples = 3000
n_features = 1000

prng = np.random.RandomState(1)
prec = make_sparse_spd_matrix(n_features, alpha=.98,
                              smallest_coef=.4,
                              largest_coef=.7,
                              random_state=prng)
cov = linalg.inv(prec)
d = np.sqrt(np.diag(cov))
cov /= d
cov /= d[:, np.newaxis]
prec *= d
prec *= d[:, np.newaxis]
X = prng.multivariate_normal(np.zeros(n_features), cov, size=n_samples)
X -= X.mean(axis=0)
X /= X.std(axis=0)

##############################################################################
# Estimate the covariance
emp_cov = np.dot(X.T, X) / n_samples

model = GraphLassoCV()
model.fit(X)
cov_ = model.covariance_
prec_ = model.precision_

