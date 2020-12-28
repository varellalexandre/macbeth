from .macbeth_interfaces import *
import logging
import pandas as pd

class LPMacbethVars(Vars):
    def __init__(
        self,
        solver:pywraplp.Solver,
        set:list
    ):
        logging.debug("Vars:")
        s1 = solver.NumVar(
            0.5,
            0.5,
            "s_1"
        )
        setattr(
            self,
            "s_1",
            s1
        )
        logging.debug("s_1=0.5")
        for s_value in range(2,7):
            sx = solver.NumVar(
                0,
                solver.infinity(),
                "s_{}".format(s_value)
            )
            setattr(
                self,
                "s_{}".format(s_value),
                sx
            )
            logging.debug("s_{} >= 0".format(s_value))
        for idx,variable in enumerate(set):
            vx = solver.NumVar(
                0,
                solver.infinity(),
                "x_{}".format(idx)
            )
            setattr(
                self,
                "x_{}".format(idx),
                vx
            )
            logging.debug("x_{} >= 0".format(idx))

class LPMacbethConstraints(Constraint):
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Vars,
        set:dict
    ):
        logging.debug("S.t.")
        ordered_prefs = set['ordered_prefs']

        for s_value in range(2,7):
            c0 = solver.Constraint(-solver.infinity(),-1)
            s_1 = getattr(vars,"s_{}".format(s_value - 1))
            s = getattr(vars,"s_{}".format(s_value))
            logging.debug("s_{s_1} + 1 <= s_{s}".format(
                    s = s_value,
                    s_1 = (s_value - 1)
                )
            )
            c0.SetCoefficient(s_1,1)
            c0.SetCoefficient(s,-1)


        c1 = solver.Constraint(0,0)
        min = len(ordered_prefs)-1
        v0 = getattr(vars,"x_{}".format(min))
        logging.debug("x_{} = 0".format(min))
        c1.SetCoefficient(v0,1)
        list_pref = list()

        for x,name_x in enumerate(ordered_prefs):
            next = x+1
            for y,name_y in enumerate(ordered_prefs[next:]):
                lower_bound = set[name_x]['relations'][name_y]['lower']
                upper_bound = set[name_x]['relations'][name_y]['upper']
                s_lower = getattr(
                    vars,
                    "s_{}".format(lower_bound)
                )
                var_x = getattr(
                    vars,
                    "x_{}".format(x)
                )
                var_y = getattr(
                    vars,
                    "x_{}".format(y+next)
                )
                logging.debug("s_{s}+0.5<=x_{x}-x_{y}".format(
                        s = lower_bound,
                        x = x,
                        y = y+next
                    )
                )
                c2 = solver.Constraint(-solver.infinity(),-0.5)
                c2.SetCoefficient(s_lower,1)
                c2.SetCoefficient(var_x,-1)
                c2.SetCoefficient(var_y,1)
                if upper_bound < 6:
                    s_upper = getattr(
                        vars,
                        "s_{}".format(upper_bound+1)
                    )
                    c3 = solver.Constraint(-solver.infinity(),-0.5)
                    c3.SetCoefficient(s_upper,-1)
                    c3.SetCoefficient(var_x,1)
                    c3.SetCoefficient(var_y,-1)
                    logging.debug("x_{x}-x_{y}<=s_{s}-0.5".format(
                            s = upper_bound,
                            x = x,
                            y = y+next
                        )
                    )


class LPMacbethObjective:
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Vars,
        set:dict
    ):
        self.solver = solver
        self.objective = solver.Objective()
        min = len(set['ordered_prefs'])-1
        x_max = getattr(vars,"x_0")
        x_min = getattr(vars,"x_{}".format(min))
        logging.debug(" min : x_0-x_{}".format(min))
        self.objective.SetCoefficient(x_max,1)
        #self.objective.SetCoefficient(x_min,-1)
        self.objective.SetMinimization()


class LPMacbeth(Problem):
    def __init__(self,set:dict):
        super(LPMacbeth,self).__init__(
            'LP-MACBETH'
        )

        self.vars_object = LPMacbethVars
        self.objective_object = LPMacbethObjective
        self.constraints_object = LPMacbethConstraints
        self.set = set

    def calculate(self):
        ordered_prefs = self.set['ordered_prefs']
        vars = self.vars_object(
            self,
            ordered_prefs
        )
        constraints = self.constraints_object(
            self,
            vars,
            self.set,
        )
        objective = self.objective_object(
            self,
            vars,
            self.set,
        )
        self.Solve()
        return_dict = dict()
        for pos,category in enumerate(ordered_prefs):
            logging.debug("{category}".format(category=category))
            return_dict["x_{}".format(pos)] = getattr(
                                                    vars,
                                                    "x_{}".format(pos)
                                                ).solution_value()
            logging.debug(
                return_dict["x_{}".format(pos)]
            )
        return return_dict
