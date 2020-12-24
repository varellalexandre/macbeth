from macbeth_interfaces import *
from constraints import *

class ProgramMC2Vars(Vars):
    def __init__(self,solver:pywraplp.Solver,set:list):
        self.s0 = solver.NumVar(0,0,'s0')
        self.s1 = solver.NumVar(1,1,'s1')
        for category in range(2,6):
            var = solver.NumVar(
                -solver.infinity(),
                solver.infinity(),
                's{category}'.format(category=category)
            )
            setattr(
                self,
                's{category}'.format(category=category),
                var
            )
        self.theta = solver.NumVar(0,solver.infinity(),'theta')
        self.Cmin = solver.NumVar(0,solver.infinity(),'Cmin')
        for element in set:
            print(element)
            var = solver.NumVar(
                0,
                solver.infinity(),
                element
            )
            setattr(
                self,
                element,
                var
            )

if __name__ == '__main__':
    frame = pd.read_excel('exemplo MacBeth.xlsx')
    mc2 = ProgramMC2(frame)
    mc2.schematize()
