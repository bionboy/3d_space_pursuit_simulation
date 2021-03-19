#! /usr/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d
import matplotlib.collections as mcoll
import matplotlib.path as mpath

import numpy as np


def colorline(
    x,
    y,
    z,
    c=None,
    cmap=plt.get_cmap("copper"),
    norm=plt.Normalize(0.0, 1.0),
    linewidth=3,
    alpha=1.0,
):
    if c is None:
        c = np.linspace(0.0, 1.0, len(x))

    if not hasattr(c, "__iter__"):
        c = np.array([c])

    c = np.asarray(c)

    segments = make_segments(x, y, z)
    lc = mcoll.LineCollection(
        segments, array=c, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha
    )

    ax = plt.gca()
    ax.add_collection(lc)
    return lc


def make_segments(x, y, z):
    # points = np.array([x, y]).T.reshape(-1, 1, 2)
    points = np.array([x, y, z]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments


# N = 10
# np.random.seed(101)
# x = np.random.rand(N)
# y = np.random.rand(N)
# fig, ax = plt.subplots()
# path = mpath.Path(np.column_stack([x, y]))
# verts = path.interpolated(steps=3).vertices
# x, y = verts[:, 0], verts[:, 1]
# z = np.linspace(0, 1, len(x))
# colorline(x, y, z, cmap=plt.get_cmap("jet"), linewidth=2)

plt.show()

mpl.rcParams["legend.fontsize"] = 10
fig = plt.figure()
ax = fig.gca(projection="3d")

N = 100
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z ** 2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

# fig, ax = plt.subplots()
path = mpath.Path(np.column_stack([x, y, z]))
verts = path.interpolated(steps=3).vertices
x, y = verts[:, 0], verts[:, 1]
z = np.linspace(0, 1, len(x))
colorline(x, y, z, cmap=plt.get_cmap("jet"), linewidth=2)

ax.plot(x, y, z, label="Target")
ax.legend()
plt.show()