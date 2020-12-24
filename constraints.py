from macbeth_interfaces import *
import logging

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
                    "u(x_{})".format(x)
                )
                uy = getattr(
                    vars,
                    "u(x_{})".format(y+next)
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
                    "u(x_{})".format(x)
                )
                uy = getattr(
                    vars,
                    "u(x_{})".format(y+next)
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

class Constraint_7(Constraint):
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
                value = set[name_y][x]
                if value <= 5:
                    constr = solver.Constraint(
                        0,
                        0
                    )
                    beta_xy = getattr(
                        vars,
                        "beta(x{x}_x{y})".format(
                            x=x,
                            y=(y+next)
                        )
                    )
                    mi_xy = getattr(
                        vars,
                        "mi(x{x}_x{y})".format(
                            x=x,
                            y=(y+next)
                        )
                    )
                    ux = getattr(
                        vars,
                        "u(x_{})".format(x)
                    )
                    uy = getattr(
                        vars,
                        "u(x_{})".format((y+next))
                    )
                    svalue = getattr(
                        vars,
                        's{value}'.format(value=value)
                    )
                    str = "u(x_{x}) - u(x_{y}) - s{value} - beta(x{x}_x{y}) + mi(x{x}_x{y}) = 0".format(
                        x = x,
                        y = (y+next),
                        value = value
                    )
                    logging.debug(str)
                    constr.SetCoefficient(ux,1)
                    constr.SetCoefficient(uy,-1)
                    constr.SetCoefficient(svalue,-1)
                    constr.SetCoefficient(beta_xy,-1)
                    constr.SetCoefficient(mi_xy,1)

class Constraint_8(Constraint):
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
                value = set[name_y][x]
                if value > 1:
                    constr = solver.Constraint(
                        0,
                        0
                    )
                    alfa_xy = getattr(
                        vars,
                        "alfa(x{x}_x{y})".format(
                            x=x,
                            y=(y+next)
                        )
                    )
                    gama_xy = getattr(
                        vars,
                        "gama(x{x}_x{y})".format(
                            x=x,
                            y=(y+next)
                        )
                    )
                    theta = vars.theta
                    ux = getattr(
                        vars,
                        "u(x_{})".format(x)
                    )
                    uy = getattr(
                        vars,
                        "u(x_{})".format((y+next))
                    )
                    svalue = getattr(
                        vars,
                        's{value}'.format(value=(value-1))
                    )
                    str = "u(x_{x}) - u(x_{y}) - s{value} - theta + alfa(x{x}_x{y}) - gama(x{x}_x{y}) = 0".format(
                        x = x,
                        y = (y+next),
                        value = (value-1)
                    )
                    logging.debug(str)
                    constr.SetCoefficient(ux,1)
                    constr.SetCoefficient(uy,-1)
                    constr.SetCoefficient(svalue,-1)
                    constr.SetCoefficient(theta,-1)
                    constr.SetCoefficient(alfa_xy,1)
                    constr.SetCoefficient(gama_xy,-1)

class Constraint_9(Constraint):
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
                value = set[name_y][x]
                if value <= 5:
                    constr = solver.Constraint(
                        0,
                        0
                    )
                    ux = getattr(
                        vars,
                        "u(x_{})".format(x)
                    )
                    uy = getattr(
                        vars,
                        "u(x_{})".format((y+next))
                    )
                    svalue_1 = getattr(
                        vars,
                        's{value}'.format(value=(value-1))
                    )
                    theta = vars.theta
                    svalue = getattr(
                        vars,
                        's{value}'.format(value=(value))
                    )
                    ep_xy = getattr(
                        vars,
                        "ep(x{x}_x{y})".format(
                            x=x,
                            y=(y+next)
                        )
                    )
                    n_xy = getattr(
                        vars,
                        "n(x{x}_x{y})".format(
                            x=x,
                            y=(y+next)
                        )
                    )
                    str = "u(x_{x}) - u(x_{y}) - 0.5*s{value} - 0.5*s{value_1} - 0.5*theta - ep(x{x}_x{y}) + n(x{x}_x{y}) = 0".format(
                        x = x,
                        y = (y+next),
                        value = value,
                        value_1 = (value-1)
                    )
                    logging.debug(str)
                    constr.SetCoefficient(ux,1)
                    constr.SetCoefficient(uy,-1)
                    constr.SetCoefficient(svalue,-0.5)
                    constr.SetCoefficient(svalue_1,-0.5)
                    constr.SetCoefficient(theta,-0.5)
                    constr.SetCoefficient(ep_xy,-1)
                    constr.SetCoefficient(n_xy,1)
