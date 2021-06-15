Coding style – Laboratoire de recherche en mobilité et sport adapté
===================================================================
Félix Chénier

This document defines the coding style to use with Python and Matlab at the Mobility and Adaptive Sports Research Lab. This guide is strongly inspired by the MATLAB Guidelines 2.0 by Richard Johnson, and by Python’s PEP8.
 
# Why bothering with a coding style?

Adopting a coding style is all about understanding this simple fact: code is more often read than written, and people who read the code are often not the ones who wrote it. By respecting a coding style, the code is clearer, more homogeneous, and easier to understand and reuse.

Both Matlab and Python have (unfortunately different) general guidelines, that we try to follow at the lab. This ensures that the code we produce is coherent with most code written by other people.

# Language

Use English. Most programming languages, including Python and Matlab, use English keywords. Therefore, for coherence, it just makes sense to program in English, including comments. If the code is used explicitly for formation in another language (here it would be French), it is okay to write comments in French. Otherwise, keep in mind that sharing code is a great way to collaborate, and eventual code readers may not speak French at all while they are likely to understand English.

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

Variables should be passive (nouns with or without qualifiers). Verbs are reserved for functions.

## Temporary variables

For temporary variables with a small scope (no more than a few lines), it is correct to use very short names (even one letter). For example, it is common practise to use `i` and `j` as temporary indexes, `x`, `y`, `z`, `t` as temporary space and time coordinates, and `s` as temporary strings. Still, it is generally a good idea to stick to meaningful names instead of letters.

```python
# python

for i in range(10):
    process_recording(i)
```

```matlab
% matlab

for i = 1:10
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

participants = {'P01', 'P02', 'P03'}
for participant = participants
    processparticipant(participant);
end
```

## Negated boolean names

Avoid using negated boolean variable names, such as `is_invalid`, because it creates confusion when used in combination with logic operators. For example, `~is_invalid` is a double negation to tell that a value is indeed valid.

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

string = 'test'      # bad
string_ = 'test'     # better
the_string = 'test'  # best
```

## Constants

Neither Python or Matlab do have true constants. It is therefore a good idea to adopt a practice that makes constants explicit so that someone does not unintentionally redefines its value. Use capital letters separated with underscores:

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

angle          # good, we assume radians
angleRadians   # good but not required
angleDegrees   # good
angle          # bad if the unit is degrees
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
plot
calculate_local_coordinates
```

In Matlab, function names are in lower case, without underscores:

```matlab
plot
calculatelocalcoordinates
```

## Active form

Since a function performs an action, it should start with a verb.

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
    %    (as floats), and returns the norm of this vector.
    norm = sqrt(x.^2 + y.^2 + z.^2);
    return
end
```

## Prefixes `get` and `set`

In other programming languages, get and set are often used to get or set the value of class attributes. For example, a class `Participant` could have an attribute `height` with the `get_height()` and `set_height()` methods. However, the recommended strategy in both Python and Matlab is to read or write the attribute directly, and to user dynamic properties in the rarer cases where an operation must be done on reading or assigning. Therefore, using `get` and `set` as getter/setters is not recommended.

## Symmetry

Two functions that have opposite actions should also have an opposite signature: `add`/`remove`, `start`/`stop`, `begin`/`end`, `insert`/`delete`, `increment`/`decrement`, `open`/`close`, `show`/`hide`, `suspend`/`resume`, etc.


# Classes

## Passive form

As for variables, classes are passive, using nouns. To differentiate between a class and a class instance, the casing for classes and variables are different. Classes use mixed case starting with a capital letter.

```python
TimeSeries                 # This is the name of the class
timeseries = TimeSeries()  # This is an instance of the TimeSeries class.
```

# To be continued

This is only the beginning but I will try to keep it short.

# References
