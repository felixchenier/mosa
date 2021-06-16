![logo](../logo/logo_standard_light_small.png)

Coding style guidelines
=======================
Félix Chénier

This document defines the coding style to use with Python and Matlab at the *Mobility and Adaptive Sports Research Lab*.

For Python, we try to follow all the following conventions:

- [Style Guide for Python Code (PEP8)](https://pep8.org/)
- [Numpy Docstring](https://numpydoc.readthedocs.io/en/latest/format.html)

For Matlab, we try to follow most of the conventions used by Mathworks themselves. We follow much of this guide by Richard Johnson:

- [MATLAB Guidelines 2.0](http://www.datatool.com/downloads/matlab_style_guidelines.pdf)

The most important rules are described in this document, for both Python and Matlab. You cannot be completely wrong if you follow every rule defined in this document and, for Python coders, if you use the tools mentioned in section [Tools for Python coders](#tools-for-python-coders).


# Contents

<!-- TOC START min:1 max:3 link:true asterisk:false update:true -->
- [Contents](#contents)
- [Why bothering with a coding style?](#why-bothering-with-a-coding-style)
- [Language](#language)
- [Variables](#variables)
  - [Explicit names](#explicit-names)
  - [Passive form](#passive-form)
  - [Temporary variables](#temporary-variables)
  - [Prefixes `i` and `n`](#prefixes-i-and-n)
  - [Plurals](#plurals)
  - [Negated boolean names](#negated-boolean-names)
  - [Reserved names](#reserved-names)
  - [Constants](#constants)
  - [Units](#units)
  - [Dictionaries/Structures](#dictionariesstructures)
- [Functions](#functions)
  - [Explicit names](#explicit-names-1)
  - [Active form](#active-form)
  - [Docstrings](#docstrings)
  - [Symmetry](#symmetry)
- [Classes](#classes)
  - [Passive form](#passive-form-1)
- [Tools for Python coders](#tools-for-python-coders)
- [To be continued](#to-be-continued)
<!-- TOC END -->

# Why bothering with a coding style?

Adopting a coding style is all about understanding this fact: code is more often read than written, and people who read the code are often not the ones who wrote it. By respecting a coding style, the code is clearer, more homogeneous, and easier to understand and reuse.

Both Matlab and Python have general guidelines (although unfortunately different), that we try to follow at the lab. This ensures that the code we produce is coherent with lots of code written by other people.

# Language

Use English. Most programming languages, including Python and Matlab, use English keywords. For coherence, it just makes sense to program in English, including comments. If the code is used explicitly for formation in another language (here it would be French), it is okay to write comments in French. Otherwise, since sharing code is a great way to collaborate, and eventual collaborators may not speak French at all, then code in English.

To be consistent with this convention, this guide is also written in English to avoid the needs for constant translations (e.g., integer/entier, string/chaîne de caractères, etc.).

# Variables

## Explicit names

The names of variables should document their meaning or use and avoid abbreviations or symbols. This works:

    v = p / t

but this will be clearer for the reader:

    velocity = position / time

In Python, variable names are in lower case, separated by underscores:

```python
# python

position
mean_velocity
n_participants
```

In Matlab, variable names are in mixed case, starting with lower case:

```matlab
% matlab

position
meanVelocity
nParticipants
```

## Passive form

Variables should be passive, using nouns (with or without qualifiers). Names that are both nouns and verbs should be avoided.

```python
# python

calculated_forces  # good
calculate_forces   # bad
```

```matlab
% matlab

calculatedForces  % good
calculateForces   % bad
```

## Temporary variables

For temporary variables with a small scope (no more than a few lines), it is correct to use very short names, even one letter long. For example, it is common practise to use `i` and `j` as temporary indexes, `x`, `y`, `z`, `t` as temporary space and time coordinates, and `s` as temporary strings. Still, it is generally a good idea to use meaningful names instead of letters.

```python
# python

for i in range(10):  # ok to use i
    process_recording(i)
```

```matlab
% matlab

for i = 1:10  % ok to use i
    processrecording(i);
end
```

## Prefixes `i` and `n`

Use the prefix `i` for indicating an index, and `n` for indicating a total count:

```python
# python

for i_recording in range(n_recordings):
    process_recording(i_recording)
```

```matlab
% matlab

for i_recording = 1:n_recordings
    processrecording(i_recording);
end
```

## Plurals

Use plural to denote a list (array) of elements, and singular to denote a single element.

```python
# python

participants = ['P01', 'P02', 'P03']

for participant in participants:
    process_participant(participant)
```

```matlab
% matlab

participants = {'P01', 'P02', 'P03'};
for participant = participants
    processparticipant(participant);
end
```

## Negated boolean names

Avoid using negated boolean variable names, such as `is_invalid`, because it creates confusion when used in combination with logic operators. For example, `~is_invalid` is a double negation that means valid, which is confusing.

```python
# python

is_not_found  # bad
is_found      # good

is_invalid    # bad
is_valid      # good
```

```matlab
% matlab

isNotFound  % bad
isFound     % good

isInvalid   % bad
isValid     % good
```

## Reserved names

Avoid using reserved names (names that are part of the language), since it can cause clashes that are difficult to debug. A better way is to suffix the variable name with an underscore, and the best way is to find a synonym.

```python
# python

str = 'test'         # bad
str_ = 'test'        # better
the_string = 'test'  # best
```

```matlab
% matlab

string = 'test'      % bad
string_ = 'test'     % better
theString = 'test'   % best
```

## Constants

Neither Python or Matlab do have true constants. It is therefore a good idea to adopt a practice that makes constants explicit so that someone does not unintentionally redefines its value. In both Python and Matlab, use capital letters separated with underscores to define constants:

```python
SERIAL_NUMBER = '123ABC'
WHEEL_RADIUS = 0.3
```

## Units

In general, use the International System of Units (SI) for values. When SI Units could not or should not be used, consider adding the unit as a suffix.

```python
#python

angle          # good, we assume radians
angle_radians  # good but not required
angle_degrees  # good
angle          # bad if the unit is degrees
```

```matlab
% matlab

angle          % good, we assume radians
angleRadians   % good but not required
angleDegrees   % good
angle          % bad if the unit is degrees
```

## Dictionaries/Structures

The key names of a dictionary (Python), or field names of a structure (Matlab) should be passive, in mixed case starting with a capital.

```python
# python

anthropometrics = {
    'Weight': 75,
    'Height': 170,
    'DateOfBirth': '2000-01-01',
}
```

```matlab
% matlab

anthropometrics = struct( ...
    'Weight', 75, 'Height', 170, 'DateOfBirth', '2000-01-01')
```

Avoid repeating the dictionary/struct name in the key/field names.

```python
# python

segment = {
    'SegmentLength': 0.40,
    'SegmentMass': 2.0,
}  # Bad

segment = {
    'Length': 0.40,
    'Mass': 2.0,
}  # Good
```

```matlab
% matlab

segment = struct('SegmentLength', 0.40, 'SegmentMass', 2.0)  % Bad

segment = struct('Length', 0.40, 'Mass', 2.0)  % Good
```

# Functions

## Explicit names

As for variables, the names of functions should document their use. Avoid using abbreviations.

In Python, function names are in lower case, separated by underscores:

```python
# python

plot
calculate_local_coordinates
```

In Matlab, function names are in lower case, without underscores:

```matlab
% matlab

plot
calculatelocalcoordinates
```

## Active form

Since a function performs an action, it should start with a verb.

```python
# python

calculate_forces   # good
calculated_forces  # bad
```

```matlab
% matlab

calculateforces   % good
calculatedforces  % bad
```

## Docstrings

Every function should have a docstring section to indicate what is the purpose of the function, and how to use it. For Python, we use the numpydoc format. For Matlab, the form is less defined but should match the example provided here.

```python
# python

def calculate_norm(x, y, z):
    """
    Calculate the norm of a vector.

    Parameters
    ----------
    x, y, z: float. The components of the vector.

    Returns
    -------
    float

    """
    return np.sqrt(x ** 2 + y ** 2 + z ** 2)
```

```matlab
% matlab

function norm = calculatenorm(x, y, z)
    % calculate_norm Calculate the norm of a vector.
    %    This function takes as arguments the three components of a vector
    %    (as doubles), and returns the norm of this vector as a new double.
    norm = sqrt(x.^2 + y.^2 + z.^2);
    return
end
```

## Symmetry

Two functions that have opposite actions should have matched names: `add`/`remove`, `start`/`stop`, `begin`/`end`, `insert`/`delete`, `increment`/`decrement`, `open`/`close`, `show`/`hide`, `suspend`/`resume`, etc.


# Classes

## Passive form

As for variables, classes are passive, using nouns. In python, classes and class instances (variables) are differentiated using case. Classes use mixed case starting with a capital letter, while variables use lower cases separated with underscores.

```python
# python

TimeSeries                 # This is the name of the class
timeseries = TimeSeries()  # This is an instance of the TimeSeries class.
```

In Matlab, it is well less defined but we tend to follow the same convention for classes: using mixed case starting with a capital letter.


# Tools for Python coders

For those who are coding in Python in the Spyder environment, you can do the following to ensure that your code complies to other PEP8 specifications that are not covered in this guide, such as the maximal number of blank lines allowed between sections, the number of characters per line, etc.

- In Preferences : Completion in linting : Code style and formatting : Code style, check Enable code style linting to enable PEP8 linting;
- In Preferences : Completion in linting : Code style and formatting : Code formatting, Select autopep8 and check Autoformat files on save to ensure minimal PEP8 compliance at all times;
- In Preferences : Completion in linting : Docstring style, check Enable Docstring style linting and select Numpy to enable Numpy docstring linting.


# To be continued

This is a work in progress, but I'll try to keep the guide short.
