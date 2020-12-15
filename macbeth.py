from macbeth_interfaces import *


class Program_MC1_Vars:
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
            var = solver.NumVar(
                -solver.infinity(),
                solver.infinity(),
                element
            )
            setattr(
                self,
                element,
                var
            )

class Program_MC1_Constraints:
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Program_MC1_Vars,
        set:pd.DataFrame
    ):
        ordered_prefs = [row[0] for idx,row in set.iterrows()]
        #Constraint (2)
        for category in range(2,6):
            var_k = getattr(
                vars,
                's{category}'.format(category=category)
            )
            var_k_1 = getattr(
                vars,
                's{category}'.format(category=category-1)
            )
            constr = solver.Constraint(
                1,
                solver.infinity()
            )
            constr.SetCoefficient(var_k,1)
            constr.SetCoefficient(var_k_1,-1)
            setattr(
                self,
                'c2_s{category}_s{category2}'.format(
                    category=category,
                    category2=category-1
                ),
                constr
            )

        for x,name_x in enumerate(ordered_prefs):
            next = x+1
            for y,name_y in enumerate(ordered_prefs[next:]):
                ux = getattr(
                    vars,
                    name_x
                )
                uy = getattr(
                    vars,
                    name_y
                )
                #Constraint (3)
                constr = solver.Constraint(
                    0,
                    solver.infinity()
                )
                constr.SetCoefficient(ux,1)
                constr.SetCoefficient(uy,-1)
                constr.SetCoefficient(vars.theta,-1)

                #Constraint(5)
                value = set[name_y][x]
                sk_1 = getattr(
                        vars,
                        "s{category}".format(category=value-1)
                )
                lower_constr = solver.Constraint(
                    -solver.infinity(),
                    0
                )
                lower_constr.SetCoefficient(sk_1,1)
                lower_constr.SetCoefficient(vars.theta,1)
                lower_constr.SetCoefficient(vars.Cmin,-1)
                lower_constr.SetCoefficient(ux,-1)
                lower_constr.SetCoefficient(uy,1)
                if value < 6:
                    upper_constr = solver.Constraint(
                        -solver.infinity(),
                        0
                    )
                    sk = getattr(
                            vars,
                            "s{category}".format(category=value)
                    )
                    upper_constr.SetCoefficient(sk,-1)
                    upper_constr.SetCoefficient(vars.Cmin,-1)
                    upper_constr.SetCoefficient(ux,1)
                    upper_constr.SetCoefficient(uy,-1)

class Program_MC1_Objective:
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Program_MC1_Vars,
        set:pd.DataFrame
    ):
        self.solver = solver
        self.objective = solver.Objective()
        self.objective.SetCoefficient(vars.Cmin,1)
        self.objective.SetMinimization()

class Program_MC1:

    def __init__(self,set:pd.DataFrame):
        self.solver = pywraplp.Solver(
            'MC1',
            pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.vars_object = Program_MC1_Vars
        self.objective_object = Program_MC1_Objective
        self.constraints_object = Program_MC1_Constraints
        self.set = set


    def schematize(self):
        ordered_prefs = [row[0] for idx,row in self.set.iterrows()]
        vars = self.vars_object(self.solver,ordered_prefs)
        constraints = self.constraints_object(
            self.solver,
            vars,
            self.set,
        )
        objective = self.objective_object(
            self.solver,
            vars,
            self.set,
        )
        self.solver.Solve()
        print(vars.Cmin.solution_value())
        for category in ordered_prefs:
            print("{category}".format(category=category))
            print(
                getattr(
                    vars,
                    "{category}".format(category=category)
                ).solution_value()
            )



class Macbeth:
    def __init__(self):
        pass

if __name__ == '__main__':
    frame = pd.read_excel('exemplo MacBeth.xlsx')
    mc1 = Program_MC1(frame)
    mc1.schematize()
