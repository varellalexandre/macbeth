from macbeth_interfaces import *

class Constraint_2(Constraint):
    def __init__(
        self,
        vars:Vars,
        set:pd.DataFrame,
        solver:pywraplp.Solver
    ):
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

class Constraint_3(Constraint):
    def __init__(
        self,
        vars:Vars,
        set:pd.DataFrame,
        solver:pywraplp.Solver
    ):
        ordered_prefs = [row[0] for idx,row in set.iterrows()]
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
                constr = solver.Constraint(
                    0,
                    solver.infinity()
                )
                constr.SetCoefficient(ux,1)
                constr.SetCoefficient(uy,-1)
                constr.SetCoefficient(vars.theta,-1)

class Constraint_5(Constraint):
    def __init__(
        self,
        vars:Vars,
        set:pd.DataFrame,
        solver:pywraplp.Solver
    ):
        ordered_prefs = [row[0] for idx,row in set.iterrows()]
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
