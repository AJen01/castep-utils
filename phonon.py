from pathlib import Path
import argparse
import matplotlib.pyplot as plt

class PHONON:
    def __init__(self) -> None:
        self.filename = None
        self.freqs = []
        self.ir_freqs = []
        self.raman_freqs = []

    def is_int(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False
        
    def read_freqs(self, filename):
        self.filename = Path(filename)

        with open(self.filename, "r", encoding="utf-8") as i:
            lines = i.readlines()
        
        for line in lines:
            elem = line.split()
            try:
                if line.startswith(" +") and elem[4] == "Y":
                    self.ir_freqs.append(float(elem[2]))
                if line.startswith(" +") and elem[5] == "Y":
                    self.raman_freqs.append(float(elem[2]))
                if line.startswith(" +") and self.is_int(elem[1]):
                    self.freqs.append(float(elem[2]))
            except IndexError:
                pass
            
        print("TOTAL FREQUENCIES: ", len(self.freqs))
        print("IR FREQUENCIES: ", len(self.ir_freqs))
        print("RAMAN FREQUENCIES: ", len(self.raman_freqs))
    
    def plot_ir(self):
        intensities = [1] * len(self.ir_freqs)
        plt.vlines(self.ir_freqs, [0], intensities, colors='b', linewidth=1)
        plt.xlabel('Wavenumber (cm$^{-1}$)')
        plt.ylabel('Intensity (a.u.)')
        plt.title('IR')
        path = self.filename.parents[0] / "IR.png"
        plt.savefig(path)

    def plot_raman(self):
        intensities = [1] * len(self.raman_freqs)
        plt.vlines(self.raman_freqs, [0], intensities, colors='b', linewidth=1)
        plt.xlabel('Wavenumber (cm$^{-1}$)')
        plt.ylabel('Intensity (a.u.)')
        plt.title('Raman')
        path = self.filename.parents[0] / "Raman.png"
        plt.savefig(path)

    def plot_all(self, color=True):

        if color:
            colors = []
            for freq in self.freqs:
                if freq in self.ir_freqs and freq in self.raman_freqs:
                    colors.append('purple')  # Frequencies present in both
                elif freq in self.ir_freqs:
                    colors.append('blue')    # Frequencies present in IR only
                elif freq in self.raman_freqs:
                    colors.append('green')   # Frequencies present in Raman only
                else:
                    colors.append('red')     # Frequencies present in neither

            plt.vlines(self.freqs, [0], [1] * len(self.freqs), colors=colors, linewidth=1)
            plt.xlabel('Wavenumber (cm$^{-1}$)')
            plt.ylabel('Intensity (a.u)')
            plt.title('All Vibrational Modes - Coloured')
            path = self.filename.parents[0] / "all_coloured.png"
            plt.savefig(path)
        else:
            intensities = [1] * len(self.freqs)
            plt.vlines(self.freqs, [0], intensities, colors='b', linewidth=1)
            plt.xlabel('Wavenumber (cm$^{-1}$)')
            plt.ylabel('Intensity (a.u.)')
            plt.title('All Vibrational Modes')
            path = self.filename.parents[0] / "all.png"
            plt.savefig(path)



if __name__ == "__main__":
    ph = PHONON()

    parser = argparse.ArgumentParser(description="CASTEP-utils Argument Parser")
    parser.add_argument("-f", "--filename", default="mCPPD.castep",type=str, help="Path to the castep file")
    parser.add_argument("-c", "--color", default=True,type=bool, help="Coloring full freqs option")
    args = parser.parse_args()
    ph.read_freqs(args.filename)
    ph.plot_ir()
    ph.plot_raman()
    ph.plot_all(color=args.color)
        
        