# Celmo

Common envelope light module.

## Synopsis

Celmo  computes   the  light   curve  emitted  from   common  envelope
hydrodynamic  simulations carried  out with  the 3D  hydrodynamic code
Enzo used in unigrid mode.


## Installation

To install celmo in your standar python directorie run the command:

`sudo pip install /path/to/celmo/source`

## Examples

### command line

Assuming that the data is in `/path/to/data`

1. Create a new project directory `mkdir /path/to/root/project`
2. Create a new parameter file some_params.par (see below)
3. Run celmo `nohup celmo_cmd.py some_params.par > output.log &`


### interactive notebook

Follow the example in celmo/notebooks/Example.ipynb

### parameter file

The parameter file has the following format:

>[output]

>directory=/path/to/root/project

>datafiles=/path/to/data

>overwrite=no

>[model]

>effective_temperature=3500

>mol_weight=1.2

>floor_density=1e-9

