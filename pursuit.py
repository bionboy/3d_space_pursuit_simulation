#! /usr/bin/python

import math
from dataclasses import dataclass
from enum import Enum
from typing import List

import numpy as np
from numpy.lib.histograms import histogram
from numpy.random import rand

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d
import matplotlib.collections as mcoll
import matplotlib.path as mpath


class CraftMode(Enum):
    neutral = 1
    offense = 2
    defense = 3


@dataclass
class Vec3:
    x: float = 0
    y: float = 0
    z: float = 0

    def magnitude(self) -> float:
        x, y, z = self.x, self.y, self.z
        x, y, z = x ** 2, y ** 2, z ** 2
        return np.sqrt(np.sum([x, y, z]))

    def toUnit(self):
        v = np.array([self.x, self.y, self.z], dtype=float)
        v_ = v / np.linalg.norm(v)  # type: ignore
        return Vec3(v_[0], v_[1], v_[2])

    def normal(self, other: "Vec3") -> "Vec3":
        v = np.array(
            [
                other.x - self.x,
                other.y - self.y,
                other.z - self.z,
                # self.x - other.x,
                # self.y - other.y,
                # self.z - other.z,
            ],
            dtype=float,
        )
        v_ = v / np.linalg.norm(v)  # type: ignore
        # print(v, v_, np.linalg.norm(v_))
        return Vec3(v_[0], v_[1], v_[2])

    def toList(self) -> List[float]:
        return [self.x, self.y, self.z]

    def __add__(self, other: "Vec3"):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3"):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float) -> "Vec3":
        return Vec3(self.x * other, self.y * other, self.z * other)

    __rmul__ = __mul__

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


@dataclass
class Craft:
    alpha: float
    beta: float
    speed: float
    mode: CraftMode
    pos: Vec3
    orientation: Vec3 = Vec3()
    alive: bool = True
    path: Vec3 = Vec3(0.1, -3, 0.0)
    pathUpdate: Vec3 = Vec3(0.2, 0.1, 0.5)

    def dist(self, other: "Craft") -> float:
        return (self.pos - other.pos).magnitude()

    def Angle3d(self, other: "Craft") -> float:
        def dot(v1, v2):
            return sum(x * y for x, y in zip(v1, v2))

        ang = dot(self.pos.toList(), other.pos.toList())
        ang /= self.pos.magnitude() * other.pos.magnitude()
        ang = math.acos(ang)
        return ang

    def inSight(self, other: "Craft") -> bool:
        if (self.Angle3d(other)) < self.alpha:
            return True
        return False

    def advance(self, crafts: List["Craft"]):
        oldPos = self.pos
        p = lambda: print("update: ", self.pos - oldPos)

        if self.mode == CraftMode.neutral:

            # TODO: make path following have orientation
            # normal = self.pos.normal(self.pos + self.path)
            # desiredUpdate = self.orientation.normal(normal)
            # actualUpdate = desiredUpdate * 0.3
            # self.orientation += actualUpdate
            # self.pos += self.orientation.toUnit() * self.speed

            # Naive
            self.pos += self.path.toUnit() * self.speed

            # Make the path more interesting
            self.path += self.pathUpdate
            if self.path.magnitude() > 150:
                # r = lambda: self.speed * (1 - rand())
                # self.pathUpdate = Vec3(r(), r(), r())
                self.pathUpdate = Vec3() - self.pathUpdate
                # self.path.x = -5
                # self.path.y = -3
                # self.path.z = -1

            # p()
            return

        # positions = [c.pos for c in crafts]
        other: Craft
        for craft in crafts:
            if craft != self:
                other = craft
                break
        assert other != self

        if self.mode == CraftMode.offense:
            # naive approach
            # self.pos += self.pos.normal(otherPos) * self.speed

            # Calculate angle to target
            normal = self.pos.normal(other.pos)
            # Calculate the angle between attackers'
            #  orientation and the target angle
            desiredUpdate = self.orientation.normal(normal)
            # Dampen the angle update for realism
            actualUpdate = desiredUpdate * 0.2
            self.orientation += actualUpdate

            # Throttle speed when closing in on target
            throttledSpeed = self.speed
            dist = self.dist(other)
            # TODO: determine smart distance for throttling
            if dist < self.beta * 1.2:
                print("[[[[[[[[[ THROTTLED ]]]]]]]]")
                throttledSpeed = self.speed * 0.5

            # Move craft forward proportional to speed
            self.pos += self.orientation.toUnit() * throttledSpeed

            if self.dist(other) <= self.beta:
                if self.inSight(other):
                    print("<<<<<<<<<< FIRE >>>>>>>>>>")
                    other.alive = False

        elif self.mode == CraftMode.defense:
            # TODO: Avoid nearest craft
            raise NotImplementedError

        # p()

    def __str__(self) -> str:
        return f"Pos: {self.pos},\tOri: {self.orientation}"


def plotResults(history):
    mpl.rcParams["legend.fontsize"] = 10
    fig = plt.figure()
    ax = fig.gca(projection="3d")

    def getCraftHist(idx):
        targetHist = [step[idx] for step in history]
        return zip(*[(v.x, v.y, v.z) for v in targetHist])

    x, y, z = getCraftHist(0)
    x2, y2, z2 = getCraftHist(1)

    #! Non-color
    # ax.plot(x, y, z, label="Target")
    # ax.plot(x2, y2, z2, label="Attacker")

    #! Color scatter
    c = np.linspace(0, 1, len(z))
    ax.scatter(x, y, z, label="Target", c=plt.cm.winter(c))
    ax.scatter(x2, y2, z2, label="Attacker", c=plt.cm.spring(c))

    #! Color line
    # N = 100
    # for i in range(N - 1):
    # ax.plot(x[i : i + 2], y[i : i + 2], z[i : i + 2], color=plt.cm.jet(255 * i / N))
    # ax.plot(x2[i : i + 2], y2[i : i + 2], z2[i : i + 2], color=plt.cm.jet(255 * i / N))

    ax.legend()
    plt.show()


def simulation(
    alpha: float,
    beta: float,
    speeds: List[float],
    modes: List[CraftMode],
    coords: List[Vec3],
    timeLimit: int = 100,
):
    assert len(modes) == len(coords), "length of modes and coords don't match!"
    assert timeLimit <= 10000, "# Too long!"

    #! Init crafts
    crafts = [Craft(alpha, beta, s, m, p) for s, m, p in zip(speeds, modes, coords)]

    #! Main loop
    history: List[List[Vec3]] = []
    endTime: int = timeLimit
    isDraw = True
    print("Crafts:", "".join(["\n\t" + str(c) for c in crafts]))
    for i in range(timeLimit):
        #! Update crafts
        positions = [craft.pos for craft in crafts]
        [craft.advance(crafts) for craft in crafts]
        print("Crafts:", "".join(["\n\t" + str(c) for c in crafts]))
        print(
            f"Dist: {crafts[0].dist(crafts[1])}\t Ang3D: {crafts[0].Angle3d(crafts[1])}"
        )

        #! Save all positions
        history.append(positions)

        #! Exit check
        for craft in crafts:
            if not craft.alive:
                endTime = i
                isDraw = False
                break
        if not isDraw:
            break

    #! Report results
    result = "peace"
    if not isDraw:
        result = "Destruction"
    print(f"Simulation Resolved at time-step {endTime}, resulting in {result}")

    #! Render 3D visual
    plotResults(history)


if __name__ == "__main__":
    # todo: change these values
    simulation(
        alpha=0.1,
        beta=10,
        speeds=[1, 1],
        modes=[CraftMode.neutral, CraftMode.offense],
        coords=[Vec3(10, 5, 0), Vec3(0, 150, -50)],
        timeLimit=10000,
    )
