# csc520Assi4

All programs in this assignment require python3 to function correctly.

> ## Question 2
There are two graph plan problems located in this directory named **Q2_problem1.txt**
and **Q2_problem2.txt**.

* **Q2_problem1.txt** contains a problem to make a BLT sandwitch. The graph plan by
  hand is located on page 2 of **Assign4-nnpatel5.pdf**.
* **Q2_problem2.txt** contains a problem to deliver two packages in a specific order.
  The graph plan is located on page 2 of **Assign4-nnpatel5.pdf**.


> ## Question 3
* The start point for the graph plan is in the file **GraphPlanGenerate.py** located
    in the directory **Assign4** along with the secondary file **Planner.py** which contains all the
    classes required by **GraphPlanGenerate.py** to function.

* To program **GraphPlanGenerate.py** takes two command line parameters, an input file containing
    the problem description, and an output file in which to store the results.

* This program keeps generating new layers until it reaches a stale point where the state
  layer is no longer changin. At this point the program terminates and outputs the plan to
  the output file provided.

* Upon execution of the program the contents of the input file is displayed in the terminal
    as shown in the example below.

* The output file will contain the contents of each layer in the graph plan, additionaly
    each layer has a number next to it, this indicates the depth in the graph plan. The action
    layer only lists actions on the 'Actions: ' line of the output of each layer, but the
    mutexes contain relations between persistant literals and actions as well as mutexes
    between two actions. An example is shown below.

* How to use? There are two ways to run the program both are listed below, the second one requires
    a linux terminal to execute.

        ~$ python3 GraphPlanGenerate.py <Infile> <GraphFile>
        ~$ ./GraphPlanGenerate.py <Infile> <GraphFile>


* Example execution with the file **Q2_problem2.txt** and the terminal output is shown below.

        ~$ python3 GraphPlanGenerate.py Q2_problem2.txt Q2_problem2_plan.txt

        The problem in the file Q2_Problem2.txt will be solved with graph planning:

        --------------------------------------------------------------------------------
                                        Q2_Problem2.txt
        --------------------------------------------------------------------------------
        InitialState [+At(A),-Delivered(PA),-Delivered(PB)]

        GoalState [+Delivered(PA),+Delivered(PB)]

        Act [DriveTo(B)]
        Preconditions [+At(A),+Delivered(PA)]
        Effects [+At(B)]

        Act [DeliverPackage(B)]
        Preconditions [+At(B),-Delivered(PB)]
        Effects [+Delivered(PB)]

        Act [DeliverPackage(A)]
        Preconditions [+At(A),-Delivered(PA)]
        Effects [+Delivered(PA)]

* Partial contents of the file **Q2_problem2_plan.txt** is shown below.

        StateLayer: <0>
            Literals: +At(A), -Delivered(PA), -Delivered(PB)
            Negated Literals: 
            Inconsistent Support: 
        ActLayer: <1>
            Actions: DeliverPackage(A)
            Inconsistent Effects: (-Delivered(PA), DeliverPackage(A))
            interference: (-Delivered(PA), DeliverPackage(A))
            Competing Needs: 
        StateLayer: <2>
            Literals: +At(A), -Delivered(PA), -Delivered(PB), +Delivered(PA)
            Negated Literals: (+Delivered(PA), -Delivered(PA))
            Inconsistent Support: (+Delivered(PA), -Delivered(PA))
        .
        .
        .
        
> ## Question 4
* The start point for the graph plan is in the file **GraphPlanExtract.py** located
    in the directory **Assign4** along with the secondary file **Planner.py** which contains
    all the classes required by **GraphPlanExtract.py** to function.

* To program **GraphPlanExtract.py** takes two command line parameters, an input file containing
    the problem description, and an output file in which to store the results.

* Upon execution of the program, the contents of the input file is displayed in the terminal
  and the solition is displayed at the bottom of ther terminal output as shown in the example below.

* Because this program is conserned with extraction the solution and not generating the full planning
  it does not keep generating new layers once the solition has been located. **GraphPlanGenerate.py**
  keeps adding new layers until the graph becomes stale/no longer changing, this solition
  extraction program only expands layers until a solution is found.

* How to use? There are two ways to run the program both are listed below, the second one requires
    a linux terminal to execute.

        ~$ python3 GraphPlanExtract.py <Infile> <GraphFile>
        ~$ ./GraphPlanExtract.py <Infile> <GraphFile>

* Example execution with the file **Q2_problem1.txt** and the terminal output is shown below.

        ~$ python3 GraphPlanExtract.py Q2_problem1.txt Q2_problem1_sol.txt

        The problem in the file Q2_Problem1.txt will be solved with graph planning:

        --------------------------------------------------------------------------------
                                        Q2_Problem1.txt
        --------------------------------------------------------------------------------
        InitialState [-ToastedBread,-Lettuce&Tomato,-CookedBacon]

        GoalState [+BLT]

        Act [Toast]
        Preconditions [-ToastedBread]
        Effects [+ToastedBread]

        Act [CutLettuce&Tomato]
        Preconditions [-Lettuce&Tomato]
        Effects [+Lettuce&Tomato]

        Act [CookBacon]
        Preconditions [-CookedBacon]
        Effects [+CookedBacon]

        Act [MakeBLT]
        Preconditions [+ToastedBread,+Lettuce&Tomato,+CookedBacon]
        Effects [+BLT]

        --------------------------------------------------------------------------------
                                        Solution
        --------------------------------------------------------------------------------
        [[Toast, CutLettuce&Tomato, CookBacon], [MakeBLT]]

* The solition is a list which cointains lists, the second level lists represent actions
  which are performed simultaneously.
* The program also produces an output file which also contains the solution at the end of
  the output file as shown in the contents of **Q2_Problem1_sol.txt**.

        StateLayer: <0>
            Literals: -ToastedBread, -Lettuce&Tomato, -CookedBacon
            Negated Literals: 
            Inconsistent Support: 
        ActLayer: <1>
            Actions: Toast, CutLettuce&Tomato, CookBacon
            Inconsistent Effects: (-ToastedBread, Toast), (-Lettuce&Tomato, CutLettuce&Tomato), (-CookedBacon, CookBacon)
            interference: (-ToastedBread, Toast), (-Lettuce&Tomato, CutLettuce&Tomato), (-CookedBacon, CookBacon)
            Competing Needs: 
        StateLayer: <2>
            Literals: -ToastedBread, -Lettuce&Tomato, -CookedBacon, +ToastedBread, +Lettuce&Tomato, +CookedBacon
            Negated Literals: (+ToastedBread, -ToastedBread), (+Lettuce&Tomato, -Lettuce&Tomato), (+CookedBacon, -CookedBacon)
            Inconsistent Support: (+ToastedBread, -ToastedBread), (+Lettuce&Tomato, -Lettuce&Tomato), (+CookedBacon, -CookedBacon)
        ActLayer: <3>
            Actions: Toast, CutLettuce&Tomato, CookBacon, MakeBLT
            Inconsistent Effects: (+ToastedBread, -ToastedBread), (-ToastedBread, Toast), (+Lettuce&Tomato, -Lettuce&Tomato), (-Lettuce&Tomato, CutLettuce&Tomato), (+CookedBacon, -CookedBacon), (-CookedBacon, CookBacon)
            interference: (+ToastedBread, -ToastedBread), (-ToastedBread, Toast), (+Lettuce&Tomato, -Lettuce&Tomato), (-Lettuce&Tomato, CutLettuce&Tomato), (+CookedBacon, -CookedBacon), (-CookedBacon, CookBacon), (-ToastedBread, MakeBLT), (-Lettuce&Tomato, MakeBLT), (-CookedBacon, MakeBLT), (+ToastedBread, Toast), (+Lettuce&Tomato, CutLettuce&Tomato), (+CookedBacon, CookBacon)
            Competing Needs: (+ToastedBread, -ToastedBread), (+Lettuce&Tomato, -Lettuce&Tomato), (+CookedBacon, -CookedBacon), (-ToastedBread, MakeBLT), (-Lettuce&Tomato, MakeBLT), (-CookedBacon, MakeBLT), (+ToastedBread, Toast), (+Lettuce&Tomato, CutLettuce&Tomato), (+CookedBacon, CookBacon), (MakeBLT, Toast), (CutLettuce&Tomato, MakeBLT), (CookBacon, MakeBLT)
        StateLayer: <4>
            Literals: -ToastedBread, -Lettuce&Tomato, -CookedBacon, +ToastedBread, +Lettuce&Tomato, +CookedBacon, +BLT
            Negated Literals: (+ToastedBread, -ToastedBread), (+Lettuce&Tomato, -Lettuce&Tomato), (+CookedBacon, -CookedBacon)
            Inconsistent Support: (+ToastedBread, -ToastedBread), (+Lettuce&Tomato, -Lettuce&Tomato), (+CookedBacon, -CookedBacon), (+BLT, -ToastedBread), (+BLT, -Lettuce&Tomato), (+BLT, -CookedBacon)

        --------------------------------------------------------------------------------
        Solution: [[Toast, CutLettuce&Tomato, CookBacon], [MakeBLT]]