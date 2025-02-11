import pygransoOptions

def pygransoOptionsAdvanced(n,options):
    """
    pygransoOptionsAdvanced:
        Process user options struct for pygranso.py.  If user_opts is None or
        not provided, returned opts will be PyGRANSO's default parameters.
        Standard or advanced options may be set.

        Type:
        >> help(pygransoOptionsAdvanced)
        to see documentation for the standard user options.

        USAGE:
        opts = pygransoOptionsAdvanced(n,options)

        INPUT:
        n           Number of variables being optimized.

        user_opts   Struct of settable algorithm parameters.  No fields are
                    required, irrelevant fields are ignored, and user_opts
                    may be given as None.

        OUTPUT:
        opts        Struct of all tunable user parameters for PyGRANSO.
                    If a field is provided in user_opts, then the user's
                    value is checked to whether or not it is a valid value,
                    and if so, it is set in opts.  Otherwise, an error is
                    thrown.  If a field is not provided in user_opts, opts
                    will contain the field with PyGRANSO's default value.

        ADVANCED PARAMETERS

        SEARCH DIRECTION STRATEGIES

        If a step cannot be taken with the current search direction (e.g.
        computed an invalid search direction or the line search failed on a
        valid search direction), PyGRANSO may attempt up to four optional
        fallback strategies to try to continue making progress from the current
        iterate.  The strategies are as follows and are attempted in order:

        0. BFGS-SQP steering
        - default for constrained problems
        - irrelevant for unconstrained problems

        1. BFGS-SQP steering with BFGS's inverse Hessian approximation
        replaced by the identity. If strategy #0 failed because quadprog
        failed on the QPs, this "steepest descent" version of the
        steering QPs may be easier to solve.
        - irrelevant for unconstrained problems

        2. Standard BFGS update on penalty/objective function, no steering
        - default for unconstrained problems

        3. Steepest descent on penalty/objective function, no steering

        4. Randomly generated search direction

        min_fallback_level
        -------------------------------
        Integer in [0,4]. Default value: 0

        Min number of strategy to be employed
        NOTE: fallback levels 0 and 1 are only relevant for constrained problems.

        max_fallback_level
        --------------------------------
        Integer in [0,4]. Default value: 3

        Max number of strategy to be employed (>= min_fallback_level)
        NOTE: fallback levels 0 and 1 are only relevant for constrained problems.

        max_random_attempts
        --------------------------------
        Positive integer. Default value: 5

        If max_fallback_level is 4, this is the number of randomly
        generated directions to attempt if all previous strategies fail on
        any single iteration

        STEERING PARAMETERS (only relevant for constrained problems)

        steering_l1_model
        --------------------------------
        Boolean value. Default value: True

        Determines whether or not the one norm (the standard choice) or the
        infinity norm is used for the total violation measure in steering,
        which in turn affects the predicted violation reduction.

        steering_ineq_margin
        --------------------------------
        Non-negative real value. Default value: 1e-6

        Sets the margin of feasibility for problems that only have
        inequality constraints.  For such problems, steering can be
        adaptively enabled instead of applied at every iteration.  When
        the inequality constraints are all at least steering_ineq_margin
        away from being active, steering will be disabled.  Setting
        steering_ineq_margin to zero means that steering will only be
        applied when one or more inequality constraints are active ( >= 0)
        while setting steering_ineq_margin to inf means that steering will
        be applied on every iteration.
        NOTE: this parameter has no effect if equality constraints are
        present and steering will always be enabled every iteration.

        steering_maxit
        --------------------------------
        Positive integer. Default value: 10

        If the default steering direction is not predicted to adequately
        promote progress towards feasibility, steering_maxit is the max
        number of times to iteratively lower the penalty parameter and
        recompute a hopefully better search direction which does adequately
        promote progress towards feasibility.  Setting this to higher
        values may more aggressively lower the penalty parameter per
        PyGRANSO iteration.

        steering_c_viol
        --------------------------------
        real value in (0,1). Default value: 0.1

        Determines the fraction of predicted violation reduction for a
        search direction to be considered as adequately promoting progress
        towards feasibility.  If a search direction's predicted violation
        reduction does not meet this target, the penalty parameter will be
        lowered and a new search direction will be computed.  Setting this
        to higher values may more aggressively lower the penalty parameter
        per PyGRANSO iteration.

        steering_c_mu
        --------------------------------
        real value in (0,1). Default value: 0.9

        When steering lowers the penalty parameter in order to compute a
        a search direction which promotes progress towards feasibility, it
        does by progessively lowering the penalty parameter by factors of
        steering_c_mu.  For any given PyGRANSO iteration, the penalty
        parameter can be shrunk up to a factor of steering_c_mu to the
        power of steering_maxit.  Setting this to lower values may more
        aggressively lower the penalty parameter per PyGRANSO iteration.

        QP PARAMETERS

        regularize_threshold
        ----------------
        Real value >= 1. Default value: -Inf

        Ill-conditioning of the BFGS inverse Hessian approximations H may
        cause QP solver to have difficulty in solving either the steering or
        termination QPs.  The BFGS inverse Hessian approximations H can be
        optionally regularized by limiting their condition numbers to
        regularize_threshold.  Note that this regularization is only
        applied to the H matrices appearing in the QPs; the evolving BFGS
        inverse Hessian approximation itself is never regularized.
        NOTE: setting opts.regularize_threshold to inf disables any
        regularization (and thus disables even computing the condition
        number of H).

        regularize_max_eigenvalues
        --------------------------------
        Boolean value. Default value: False

        If opts.regularize_threshold < inf, then PyGRANSO's default strategy
        to regularize the BFGS inverse Hessian approximation H is done by
        raising the smallest magnitude eigenvalues such that the condition
        number of the regularized version of H never exceeds
        opts.regularize_threshold.  This default regularization should also
        help ensure that regularized version of H is numerically positive
        definite, since H may have tiny eigenvalues and in practice, these
        may have the wrong sign numerically (negative), particularly on
        nonsmooth problems.  Alternatively, by setting this option to true,
        PyGRANSO will instead apply regularization by lowering the largest
        eigenvalues of H but note that this mode does not attempt to
        maintain numerical positive definiteness.  Also, if an eigenvalue
        of H is exactly zero, this mode will instead resort to raising the
        smallest eigenvalues of H on that particular iteration of PyGRANSO.

        LINE SEARCH PARAMETERS

        wolfe1
        ----------------
        Real value in (0,0.5]. Default value: 1e-4

        First weak Wolfe line search parameter, ensuring sufficient
        decrease of the objective/penalty.

        wolfe2
        ----------------
        Real value in [wolfe1,1). Default value: 0.5

        Second weak Wolfe line search parameter, ensuring algebraic
        increase in projected gradient.

        linesearch_nondescent_maxit
        --------------------------------
        Non-negative integer. Default value: 0

        If the computed direction is not numerically a descent direction,
        the line search can still be optionally attempted to see if it gets
        "lucky", using up to  linesearch_nondescent_maxit evaluations of
        the penalty/objective function (since there may be numerical issues
        in calculating whether it truly is a descent direction or not).

        linesearch_reattempts
        --------------------------------
        Positive integer. Default value: 10

        If the line search fails to bracket a minimizer, this may be an
        indication that the objective function is unbounded below.  For
        constrained problems, it may be that the objective is only unbouded
        below off the feasible set, in which case lower values of
        the penalty parameter mu may be necessary for PyGRANSO to find the
        feasible region.  For constrained problems, if the line search
        fails to bracket a minimizer, PyGRANSO will reattempt the line search
        with progressively lower values of mu, up to linesearch_reattempts
        times.  See opts.linesearch_c_mu, opts.linesearch_reattempts_x0,
        and opts.linesearch_c_mu_x0.
        NOTE: this option is irrelevant for unconstrained problems.

        linesearch_reattempts_x0
        --------------------------------
        Positive integer. Default value: 30

        The same as linesearch_reattempts but applies only to the first
        iteration, where it may beneficial to be more aggressive in
        lowering the penalty parameter for line search reattempts.
        NOTE: this option is irrelevant for unconstrained problems.

        linesearch_c_mu
        --------------------------------
        Real value in (0,1). Default value: 0.5

        If the line search fails to bracket a minimizer for a constrained
        problem, and linesearch_reattempts > 0, each line search reattempt
        will try a progressively smaller penalty parameter, shrinking it by
        another factor of linesearch_c_mu on each reattempt.  See
        opts.linesearch_reattempts, opts.linesearch_reattempts_x0, and
        opts.linesearch_c_mu_x0.
        NOTE: this option is irrelevant for unconstrained problems.

        linesearch_c_mu_x0
        --------------------------------
        Real value in (0,1). Default value: 0.5

        The same as linesearch_c_mu but applies only to the first
        iteration, where it may beneficial to be more aggressive in
        lowering the penalty parameter for line search reattempts.
        NOTE: this option is irrelevant for unconstrained problems.

        EXPERIMENTAL OPTIONS

        NOTE: The following options are still in development and may change or be removed in future releases. We don't recommend users use them in current version.

        init_step_size
        --------------------------------
        Positive real value. Default value: 1

        Initial step size t in line search. Recommend using small value (e.g., 1e-2) for deep learning problems.

        linesearch_maxit
        --------------------------------
        Positive integer. Default value: inf

        Max number of iterations in line search. Recommend using small value (e.g., 25) for deep learning problem.

        is_backtrack_linesearch
        --------------------------------
        Boolean value. Default value: False

        By default, NCVX will use Weak-Wolfe line search. By enabling this method, the curvature condition will be disabled.

        search_direction_rescaling
        --------------------------------
        Boolean value. Default value: False

        Rescale the norm of searching direction to be 1. Recommend setting True in deep learning problem. Used only when backtracking line search is enabled.

        disable_terminationcode_6
        --------------------------------
        Boolean value. Default value: False

        Disable termination code 6 to ensure NCVX can always make a movement even if the line search failed. Recommend setting True in deep learning problem. Used only when backtracking line search is enabled.

        END OF ADVANCED PARAMETERS

        See also pygranso, pygransoOptions.

        If you publish work that uses or refers to PyGRANSO, please cite both
        PyGRANSO and GRANSO paper:

        [1] Buyun Liang, Tim Mitchell, and Ju Sun,
            NCVX: A User-Friendly and Scalable Package for Nonconvex
            Optimization in Machine Learning, arXiv preprint arXiv:2111.13984 (2021).
            Available at https://arxiv.org/abs/2111.13984

        [2] Frank E. Curtis, Tim Mitchell, and Michael L. Overton,
            A BFGS-SQP method for nonsmooth, nonconvex, constrained
            optimization and its evaluation using relative minimization
            profiles, Optimization Methods and Software, 32(1):148-181, 2017.
            Available at https://dx.doi.org/10.1080/10556788.2016.1208749

        pygransoOptionsAdvanced.py (introduced in PyGRANSO v1.0.0)
        Copyright (C) 2016-2021 Tim Mitchell and Buyun Liang

        This file is a MATLAB-to-Python port of gransoOptionsAdvanced.m from
        GRANSO v1.6.4 with the following new functionality and/or changes:
            1. Adding new options: QPsolver, init_step_size, linesearch_maxit,
            is_backtrack_linesearch, search_direction_rescaling,
            disable_terminationcode_6.
            See https://ncvx.org/settings/new_para.html for more details.
        Ported from MATLAB to Python and modified by Buyun Liang, 2021

        For comments/bug reports, please visit the PyGRANSO webpage:
        https://github.com/sun-umn/PyGRANSO

        PyGRANSO Version 1.0.0, 2021, see AGPL license info below.

        =========================================================================
        |  PyGRANSO: A PyTorch-enabled port of GRANSO with auto-differentiation |
        |  Copyright (C) 2021 Tim Mitchell and Buyun Liang                      |
        |                                                                       |
        |  This file is part of PyGRANSO.                                       |
        |                                                                       |
        |  PyGRANSO is free software: you can redistribute it and/or modify     |
        |  it under the terms of the GNU Affero General Public License as       |
        |  published by the Free Software Foundation, either version 3 of       |
        |  the License, or (at your option) any later version.                  |
        |                                                                       |
        |  PyGRANSO is distributed in the hope that it will be useful,          |
        |  but WITHOUT ANY WARRANTY; without even the implied warranty of       |
        |  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        |
        |  GNU Affero General Public License for more details.                  |
        |                                                                       |
        |  You should have received a copy of the GNU Affero General Public     |
        |  License along with this program.  If not, see                        |
        |  <http://www.gnu.org/licenses/agpl.html>.                             |
        =========================================================================

    """
    #  This "advanced" version exists mostly just to break up the help
    #  documentation so the user isn't overwhelmed with details on the more
    #  advanced parameters which they may not immediately (or ever) need.

    #  Just pass all the work to the standard pygransoOptions function.

    opts = pygransoOptions(n,options)

    return opts
