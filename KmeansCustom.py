from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
#kneed
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler
#
def optimal_number_cluster_kmeans(X, columns,max_number_cluster=10, title="elbow method"):
  global distortions
  distortions = [] #sse
  for i in range(1, max_number_cluster):
      km = KMeans(
          n_clusters=i, init='random',
          n_init=10, max_iter=300,
          tol=1e-04, random_state=0
      )
      km.fit(X[columns])
      distortions.append(km.inertia_)


  # k = np.argmax(diffs) + 2
  kn = KneeLocator(range(1, max_number_cluster), distortions, curve='convex', direction='decreasing')

  k = kn.knee
  return k, distortions

