# solver
Generic solver for deterministic problems coded in python

It's always possible to look at a problem as search process, being the solution a 
sequence of methods applied over the problem instance.

The solver uses python's introspection to serialize the internal state of the 
problem instance, and selecting as valid methods, the list of "public" methods
available in the Problem class.

The problem class must implement an extra method called "error" which tries to 
measure the difference between the current instance and the state "solution".

The solver can receive also optional parameters to specify tolerance for the solution
and maximum time to solve the problem, before giving up.

The solver also supports another parameter to specify maximum branching, to adapt itself
to problems of different nature.
