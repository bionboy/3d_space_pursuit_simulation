#! /usr/bin/python

from dataclasses import dataclass
from typing import List
from enum import Enum
import numpy as np
from numpy.lib.histograms import histogram
from numpy.random import rand
import matplotlib.pyplot as plt


class CraftMode(Enum):
    neutral = 1
    offense = 2
    defense = 3


@dataclass
class Vec3:
    x: float = 0
    y: float = 0
    z: float = 0

    def normal(self, other: "Vec3") -> "Vec3":
        v = np.array(  # type: ignore
            [
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
            ],
            dtype=float,
        )
        v_ = v / np.linalg.norm(v)  # type: ignore
        # print(v, v_, np.linalg.norm(v_))
        return Vec3(v_[0], v_[1], v_[2])  # type: ignore

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
    path: Vec3 = Vec3(rand(), rand(), rand())  # type: ignore

    def advance(self, positions: List[Vec3]):
        oldPos = self.pos
        p = lambda: print("update: ", self.pos - oldPos)

        if self.mode == CraftMode.neutral:
            self.pos += self.path * self.speed
            # ? Stretch: Update path to make it go in circles?
            # p()
            return

        # Get a target for other two modes
        otherPos = Vec3()
        for pos in positions:
            if pos != self.pos:
                otherPos = pos
                break

        if self.mode == CraftMode.offense:
            # FIXME: This is a naive approach
            self.pos += self.pos.normal(otherPos) * self.speed
            # TODO: Calculate angle to target
            normal = self.pos.normal(otherPos)
            # TODO: turn a percentage of that angle (realism)
            # TODO: move foward in new direction proportional to speed
            pass
        elif self.mode == CraftMode.defense:
            # TODO: Avoid nearest craft
            raise NotImplementedError

        # p()

    def calcAngle(self, other: "Craft") -> float:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Pos: {self.pos},\tOri: {self.orientation}"


def simulation(
    alpha: float,
    beta: float,
    speeds: List[float],
    modes: List[CraftMode],
    coords: List[Vec3],
    timeLimit: int = 100,
):
    assert len(modes) == len(coords), "length of modes and coords don't match!"
    assert timeLimit < 10000, "# Too long!"

    #! Init crafts
    crafts = [Craft(alpha, beta, s, m, p) for s, m, p in zip(speeds, modes, coords)]

    #! Main loop
    history: List[List[Vec3]] = []
    endTime: int = timeLimit
    isDraw = True
    for i in range(timeLimit):
        #! Update crafts
        positions = [craft.pos for craft in crafts]
        # print("Postions:", ", ".join([str(pos) for pos in positions]))
        print("Crafts:", "".join(["\n\t" + str(c) for c in crafts]))
        [craft.advance(positions) for craft in crafts]

        #! Save all positions
        history.append(positions)

        #! Exit check
        # FIXME: Make this dynamic if I have time
        # Loop over all crafts to see if one has been destroyed
        for craft in crafts:
            if not craft.alive:
                endTime = i
                isDraw = False
                break

    #! Report results
    result = "peace"
    if not isDraw:
        result = "Destruction"
    print(f"Simulation Resolved at time-step {endTime}, resulting in {result}")

    #! Render 3D visual

    pass


if __name__ == "__main__":
    # todo: change these values
    simulation(
        0.1,
        0.2,
        [2, 1],
        [CraftMode.neutral, CraftMode.offense],
        [Vec3(10, 0, 0), Vec3(0, 0, 0)],
        10,
    )
