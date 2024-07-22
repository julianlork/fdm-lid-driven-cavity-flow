# Lid Driven Cavity Flow Simulation
## Overview
Implementation of a lid driven cavity flow simulator using regular finite differences method.

## Example: Periodic drive
The following image shows the simulation results for the following non-default configuration parameters:

- Simulation time:  $160\ sec$
- Reynolds number: $2000$
- Lid velocity   : $v_{top}(t)=sin(t/3)$

![Alt Text](https://github.com/julianlork/fdm-lid-driven-cavity-flow/blob/master/sim_out/periodic_drive/animation.gif)
![Alt Text](https://github.com/julianlork/fdm-lid-driven-cavity-flow/blob/master/sim_out/periodic_drive/velocity_stream.png)

## Example: Constant drive
The following image shows the simulation results for the following (default) configuration parameters:

- Simulation time:  $60\ sec$
- Reynolds number: $500$
- Lid velocity   : $v_{top}(t)=1.0$

![Alt Text](https://github.com/julianlork/fdm-lid-driven-cavity-flow/blob/master/sim_out/constant_drive/animation.gif)
![Alt Text](https://github.com/julianlork/fdm-lid-driven-cavity-flow/blob/master/sim_out/constant_drive/velocity_stream.png)

## Installation
This project uses setuptools for packaging. To install the package simply run the following command in the project directory
```
pip3 install -e .
```

## Execution
The simulation can then be executed by running
```
python3 src/main.py
```

## Governing equations in streamfunction-vorticity formulation
### Streamline function

```math
$$
\frac{\partial^2 \psi}{\partial\ x^2} + \frac{\partial^2 \psi}{\partial\ y^2} = -w 
$$
```

### Vorticity

```math
$$
\frac{\partial w}{\partial t} + \frac{\partial \psi}{\partial y} \frac{\partial w}{\partial x} + \frac{\partial \psi}{\partial x} \frac{\partial w}{\partial y} = \frac{1}{Re} \left( \frac{\partial^2 w}{\partial x^2} + \frac{\partial^2 w}{\partial y^2} \right)
$$
```

### Transport equation

```math
$$
\frac{\partial C}{\partial t} + \frac{\partial \psi}{\partial y} \frac{\partial C}{\partial x} + \frac{\partial \psi}{\partial x} \frac{\partial C}{\partial y} = \frac{1}{Re \cdot Pr} \left( \frac{\partial^2 C}{\partial x^2} + \frac{\partial^2 C}{\partial y^2} \right)
$$
```

For readability we introduce:

```math
$$
\frac{\partial \psi}{\partial x} =: u_x
$$
```

```math
$$
\frac{\partial \psi}{\partial y} =: u_y
$$
```

## Finite Differences Method formulation

### Streamline function update
```math
$$
\psi_{i,j}^{n+1} = \frac{1}{4} \left( \psi_{i+1,j}^n + \psi_{i-1,j}^n + \psi_{i,j+1}^n + \psi_{i,j-1}^n + h^2 w_{i,j}^n \right)
$$
```


### Vorticity update

```math
$$
 \frac{\partial w}{\partial t} = \frac{1}{Re} \left( \frac{w_{i+1, j}^n +w_{i, j+1}^n + w_{i-1, j}^n + w_{i,j-1}^n - 4 w_{i,j}^n }{h^2} \right) - u^n_{x|i,j}\ \left( \frac{w_{i+1,j}^n - w_{i-1,j}^n}{2h}\right) - u^n_{y|i,j}\left(\frac{w_{i,j+1}^n - w_{i,j-1}^n}{2h} \right) := f_{i,j}^n
$$
```

Using Tayler-approximation of $w(t_{n+1})$ we find the update rule

```math
$$
w_{i,j}^{n+1} = w_{i,j}^n + \Delta t\ f_{i,j}^n
$$
```

### Velocity update

```math
$$
u^n_{x|i,j} = \frac{\left( \psi^n_{i,j+1} - \psi^n_{i,j-1}\right)}{2h}
$$
```

```math
$$
u^n_{y|i,j} = \frac{\left( \psi^n_{i+1,j} - \psi^n_{i-1,j}\right)}{2h}
$$
```

### Transport equation update
```math
$$
C_{i,j}^{n+1} = C_{i,j}^n - \hat{Cu}_x - \hat{Cu}_y
$$
```

with the following flow-direction dependent terms to accomodate the upwind-scheme:
```math
$$
\hat{Cu}_x := \left\{ 
    \begin{array}{ll}
        u^n_{x|i,j}\ \frac{\Delta t}{\Delta x}\ \left( C_{i,j}^{n} - C_{i-1,j}^{n} \right) & u^n_{x|i,j} \geq 0 \\ \\
        u^n_{x|i,j}\ \frac{\Delta t}{\Delta x}\ \left( C_{i+1,j}^{n} - C_{i,j}^{n} \right) & u^n_{x|i,j} < 0 \\
    \end{array}
\right.
$$
```

```math
$$
\hat{Cu}_y := \left\{\begin{array}{ll}
        u^n_{y|i,j}\ \frac{\Delta t}{\Delta x}\ \left( C_{i,j}^{n} - C_{i,j-1}^{n} \right) & u^n_{y|i,j} \geq 0 \\ \\
        u^n_{y|i,j}\ \frac{\Delta t}{\Delta x}\ \left( C_{i,j+1}^{n} - C_{i,j}^{n} \right) & u^n_{y|i,j} < 0 \\
    \end{array}
\right.
$$
```