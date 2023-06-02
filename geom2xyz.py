from pprint import pprint as pp
import numpy as np
from pathlib import Path
import argparse


class GEOMOPT:
    def __init__(self) -> None:
        self.positions = {}
        self.steps = []
        self.append = False
        self.filename = None

    def is_int(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def read(self, line):
        line = line.split()
        if len(line) == 7:
            if self.is_int(line[1]) and line[0].isalpha() and line[-1] == "R":
                return True
        else:
            return False

    def read_geom(self, filename):
        self.filename = Path(filename)
        with open(self.filename, "r", encoding="utf-8") as i:
            lines = i.readlines()
        step = 0
        coord = 0
        for line in lines:
            if self.read(line):
                self.append = True
                self.positions[coord] = [line.split()[0]]
                self.positions[coord].append(np.array(line.split()[2:5], dtype=float))
                coord += 1
            if not self.read(line) and self.append:
                self.steps.append(len(self.positions))
                self.steps.append(f"Step {step}")
                self.steps.append(self.positions)
                step += 1
                coord = 0
                self.positions = {}
                self.append = False

    def bohr2ang(self, coord):
        return coord * 0.529177249

    def write_geom(self):
        
        with open(self.filename.with_suffix('.xyz'), "w", encoding="utf-8") as o:
            pp(self.steps)
            for item in self.steps:
                if isinstance(item, str):
                    o.writelines(item + "\n")
                elif isinstance(item, int):
                    o.writelines(str(item) + "\n")
                elif isinstance(item, dict):
                    for line in item.values():
                        line[1] = self.bohr2ang(line[1])
                        o.writelines(
                            f"{line[0]:<3} {line[1][0]:>10.5f} {line[1][1]:>10.5f} {line[1][2]:>10.5f}\n"
                        )


if __name__ == "__main__":
    cs = GEOMOPT()

    parser = argparse.ArgumentParser(description="CASTEP-utils Argument Parser")
    parser.add_argument("-f", "--filename", type=str, help="Path to the geometry file")

    args = parser.parse_args()
    cs.read_geom(args.filename)
    cs.write_geom()
