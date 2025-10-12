# autolang v0.1.0

*README last updated 11/10/2025*

*autolang* is a simple Python project based around finite-state automata, formal languages and grammars, and Turing machines. It is intended for educational use, so that students who are studying the theory within this area may supplement their understanding by creating and running their own real automata to see how they work. 

The project is heavily based on the theory from *Introduction to the Theory of Computation* by Michael Sipser.

- **version** : 0.1.0
- **license** : MIT standard license
- **build status** : prototype/WIP
- **Python version** : 3.12+
- **Python dependencies** : only the standard library
- **official repository** : https://github.com/fawnium/autolang
- **enquiries** : oisinlyons1@gmail.com

v0.1.0 is the initial release, which includes creating and simulating various automaton models, printing transition tables, and constructing automata from regular expressions via canonical methods. See [Features](#features) for more details.

Many more features are planned, as outlined in the [Roadmap](#roadmap).

### Example Use

Here is a quick example of how you can use *autolang* to explore automata. See [Usage](#usage) for more examples and more machines!

```python
from autolang import DFA, NFA # Import automata to use
from autolang import regex_to_nfa, nfa_to_dfa # Import functions to construct automata from regex

# Create transition function
tran1 = {
    ('q1', '0'): 'q1',
    ('q1', '1'): 'q2',
    ('q2', '0'): 'q3',
    ('q2', '1'): 'q2',
    ('q3', '0'): 'q2',
    ('q3', '1'): 'q2'
}

# Create DFA
dfa1 = DFA(tran1, 'q1', ['q2']) # Arguments: transition function, start state, list of accept states

# Decide a specific word
dfa1_accepts_1100 = dfa1.accepts('1100') # Will return `True`

# Decide entire language, up to given length
dfa1_language = dfa1.L(4) # Will return all accepted words up to length 4

# Print transition table
dfa1.transition_table() # Prints directly to the terminal

# Create automata from regex
regex = '(0+1)0*'
nfa = regex_to_nfa(regex) # Create NFA that recognises regex
dfa2 = nfa_to_dfa(nfa) # Create corresponding DFA

dfa2_language = dfa2.L(10) # All words should match '(0+1)0*'
```

## Description

This project is intended for educational use while studying automata theory, formal languages, complexity theory, and related areas. While finite-state machines are very well understood and used ubiquitously in compiler toolchains, text processing software, and many other technologies, we thought that it would be helpful to create a framework for students to investigate these machines themselves, to enrich and accelerate their understanding of the theoretical concepts. To justify its existence in such a well-explored area, *autolang* is being developed with the following aims:

- **Accessibility** : The project should be easy to deploy in academic settings, and require minimal technical programming/CS knowledge to interact with. We also aimed to have minimal dependencies to make the installation process easier.

- **Tactile Intuition** : The original motivation of *autolang* was to 'bridge the gap' between the theoretical descriptions of state machines, and how they are practically implemented in code. It is often said that "Turing machines are the basis for all modern computers", which is true, but we wanted interested students to be able to draw a direct line from the abstract models to real practical applications, insofar as that is possible.

While these aims are nowhere near fully-realised in v0.1.0, we expect the project to attain both enhanced features and much better usability in the coming weeks and months. These aims are discussed in more detail under [Design Philosophy](#design-philosophy) below.


## Features

For specific uses of the features below, see the [Usage](#usage) Section.

### Simulating Automata

The following automaton models are currently supported:
- DFA
- NFA
- PDA (nondeterministic only)
- TM (single tape, deterministic, as in *Sipser*)

Each of the above models supports the following methods:
- `.accepts(word: str) -> bool` 
    - Takes a string as input, returns  `True` if the given automaton accepts the string, returns `False` otherwise. If the string contains unrecognised letters, `.accepts()` will always return `False`.
    - **NOTE:** The Turing machine instance of this method (`TM.accepts()`) can also return `None`. This happens when the word is undecidable, or the TM exceeds a certain number of steps.

- `.L(n: int = 5, lazy: bool = False) -> tuple[str, ...] | Generator[str]` 
    - Takes an integer $n$ as input, returns a collection of all words recognised by the given automaton with length $\leq n$, in len-lex order.
    - if `lazy = False` (default), the collection of words is returned as a tuple immediately.
    - if `lazy = True`, the collection is instead returned as a generator, and the words are only evaluated when used in a later iteration. This is useful for saving memory for large languages, but is less intuitive for new users.
    - **WARNING:** Please note that the number of words checked grows exponentially with the length given, and the size of the underlying alphabet. Caution is advised when calling this method with a large integer or an alphabet with more than a handful of letters, as it may take several minutes or hours to terminate.

- `.transition_table()` 
    - Prints the transition table of the given automaton to the terminal.
    - **NOTE:** This feature may change in future versions, i.e. by returning a string instead of printing directly.

For guidance on creating specific automata, see [Usage](#usage) below, and the `examples/` folder inside the repository.

### Constructing Automata

In addition to manually creating and simulating automata, *autolang* has a few functions to construct automata using canonical algorithms. These are listed below:

- `regex_to_nfa(regex: str) -> NFA` 
    - Takes a regular expression string as input, returns an NFA that recognises the corresponding regular language.
    - **NOTE:** The union operator *must* be represented as `+`. The Kleene star operator is `*` as usual. No other operators may be included in the input string.

- `nfa_to_dfa(nfa: NFA) -> DFA` 
    - Takes an `NFA` object as input, returns the corresponding DFA, generated via the standard subset construction.
    - **NOTE:** The subset construction is *lazy*, so only states that are actually reachable from the start state are included in the final DFA.
    - **NOTE:** No further optimisation/minimisation occurs after the initial construction. This is a planned feature.

See the [Usage](#usage) Section for specific explanations of how to construct automata from regex.

For additional planned features, see the [Roadmap](#roadmap) Section.

## Installation

While usability is stated as a priority for *autolang*, please note the installation process is currently a work in progress, and is more 'hands-on' than we would like it to eventually be. 

We recommend using the [Developer](#developer-install) install process if you are interested in testing the code or contributing, and using the [User](#user-install) install process if you just want to use *autolang* in your Python projects.

### Developer Install

Below is a summary of the *autolang* installation process:
- Ensure `git` is installed on your computer and can be run from your terminal.
- Navigate to the folder you want to install autolang into.
- Clone the official GitHub repository. It will be installed as a subfolder within the folder you run the command from.
- Navigate to the new `autolang/` subfolder.
- Create a virtual environment if required.
- Activate the virtual environment, if created. This step is OS-dependent
- `pip` install *autolang* as a local module, so python knows where to find the source code to import.

After doing steps 1 and 2, complete the installation by running the following commands in order:

```bash
# Install from GitHub
git clone https://github.com/fawnium/autolang.git # Clone repository
cd autolang # Navigate to repository subfolder

# Set up virtual environment (optional)
python -m venv .venv # Create virtual environment
# Activate virtual environment (OS-dependent)
source .venv/bin/activate # Linux/MacOS
.venv\Scripts\Activate.ps1 # Windows PowerShell
.venv\Scripts\activate.bat # Windows cmd

# Pip install autolang
pip install -e . 
```

Using `pip install -e .` with the `-e` flag means that Python will import autolang from your local instance inside the `src/` folder. Any changes you make to the source code will immediately apply when you import it, without needing to reinstall.

After doing the above, you should be able to `import` from autolang in a Python file as usual. See [Usage](#usage) and the `examples/` folder for further guidance.

#### Updating autolang

To ensure you have the most up-to-date version from the GitHub repository, simply run:

```bash
git pull
```

Ensure this command is run when your working directory is the `autolang/` folder.


### User Install

Currently, *autolang* cannot be installed from the official python package repository (yet). However, `pip` can still be used to install autolang directly from the GitHub repository. This is very similar to normal `pip` package installs, but **you must ensure you have `git` installed on your computer first**.

#### Setting up a virtual environment (optional, recommended)

You may want to first set up a virtual environment before installing, to prevent cluttering your general system with *autolang*'s files. You can skip this step if you want to install quickly, or you want *autolang* to be importable anywhere on your computer.

For guidance about virtual environments, see:
- https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- https://docs.python.org/3/library/venv.html

If you are using Anaconda, it has its own way of managing virtual environments via `conda`. See:
- https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

The rest of the installation process below is the same regardless of whether you are using Conda.

#### Installing autolang from GitHub

To install autolang in your Python environment, enter the following command in your terminal. 

```bash
pip install git+https://github.com/fawnium/autolang.git
```

Note that this command will fail if you don't have `git` installed on your computer. Ensure you are using the correct terminal, i.e. the one that corresponds to the environment where you will write your Python code.


To check if you have autolang installed and see the version, enter this command:

```bash
pip show autolang
```

#### Updating your installation

To update to the latest version of autolang, enter this command:

```bash
pip install -U git+https://github.com/fawnium/autolang.git
```

Note the presence of the `-U` flag.

The update command above may fail to install the most up-to-date code, because the GitHub repository is regularly being modified without the version changing. If this command fails to update, use the following command instead:

```bash
pip install --force-reinstall --no-cache-dir git+https://github.com/fawnium/autolang.git
```

This will update your installation from GitHub regardless of your current installation. 

## Usage

This section describes how to import and use features once *autolang* has been installed. For installation guidance, see the [Installation](#installation) Section.

Example use cases of all the main *autolang* features are provided in the corresponding files in the `examples/` folder. Please refer to these if you are unsure how to use the features.

In general, automata are created using a specially-formatted dictionary which represents their transition function. They also require additional metadata, such as the start and accept states, which varies slightly by model. Making automaton creation easier is a planned feature.

### Creating a DFA

A DFA is created using this constructor:

```python
DFA(transition: dict[tuple[str, str], str], 
    start: str, 
    accept: Iterable[str])
```

- `transition: dict` is a dict representing the transition function of the DFA.
    - Each entry is of the form `(state, letter): next_state`, and encodes a single transition. All are strings, and `letter` should be a single character.
    - For example if you want the DFA to transition from `q0` to `q1` when reading the letter `a`, include this entry in the dict: `('q0', 'a'): 'q1'`
    - You must ensure you include a transition for every possible state-letter pair, since DFAs are deterministic. If you miss one, an error will be raised.
- `start: str` is the start state of the DFA. Its transitions must be included in the `transition` dict.
- `accept: Iterable[str]` is collection of the DFA accept states. Transitions for all accept states must be included in the `transition` dict.
    - This can be given as a `list`, `set`, or any other valid iterable object.
- You do not need to provide the alphabet or total list of states for the DFA. These are automatically inferred from the `transition` function.
- State names and alphabet letters are *case sensitive*, so ensure all strings are correct.
- States can be given any name, not just `q0, q1, ...`. Certain characters are forbidden from appearing in state names, such as `'+'` or `'_'`, but the number is relatively small. You can stick to letters and numbers to be safe.
- Letters must be single characters, but likewise can be any character other than the small number of forbidden characters.

To see if a DFA accepts a specific word, use the `.accepts()` method:

```python
is_in_language = dfa.accepts('ab') # True or False
```

To get the whole language of a DFA, up to a certain length, use the `.L()` method:

```python
language_of_dfa = dfa.L(4) # Tuple of all accepted words up to length 4, in len-lex order
```

> [!WARNING]
> Be careful using this method with a large length value, as it will take exponential time to compute.

To print the transition table of a DFA for a nice visual, use the `.transition_table()` method:

```python
dfa.transition_table() # Prints to terminal
```

Below is an example of creating a specific DFA. This is the DFA $M_1$ in Sipser, p36.

```python
from autolang import DFA

# Create the transition function dictionary
tran1 = {
    ('q1', '0'): 'q1',
    ('q1', '1'): 'q2',
    ('q2', '0'): 'q3',
    ('q2', '1'): 'q2',
    ('q3', '0'): 'q2',
    ('q3', '1'): 'q2'
}
# Create the DFA itself
M1 = DFA(tran1, 'q1', ['q2']) # The name 'M1' is arbitrary, and any valid variable name can be used

# Check specific words
M1.accepts('000') # Will return `False`
M1.accepts('100') # Will return `True`

# Generate the language of M1 up to length 3
M1.L(3) # Will return `('1', '01', '11', '001', '011', '100', '101', '111')`

# Print M1's transition table
M1.transition_table()
```

### Creating an NFA

An NFA is created using this constructor:

```python
NFA(transition: dict[tuple[str, str], tuple[str, ...]], 
    start: str, 
    accept: Iterable[str])
```

- `transition: dict` is a dict representing the transition function of the NFA.
    - Each entry is of the form `(state, letter): (next_state1, next_state2, ...)`, and encodes *all transitions* from a specific state for a specific letter. Note this differs from the DFA case, and the entry's value must be a *tuple* of strings.
    - If there is only one available transition, **this must still be wrapped in a tuple**, e.g. `('q1',)` and **not** `'q1'` or `('q1')`.
    - For example if you want the NFA to transition from `q0` to `q1` when reading `a`, then include `('q0', 'a'): ('q1',)` in the dict.
    - If you want the NFA to transition to both `q1` or `q2` from the same place, then include `('q0', 'a'): ('q1', 'q2')`.
    - You can omit entries for specific state-letter pairs (unlike with DFAs), and should do so if you want no allowed transitions.
        - If you want to include all possible transition keys for some reason, you can include `('q0', 'a'): tuple()` to indicate an empty set of allowed transitions.
    - ε-transitions are simply encoded using the empty string `''` instead of a letter. For example, an ε-transition from `q0` to `q1` will be `('q0', ''): ('q1',)` in the dict.
- `start: str` is the start state of the NFA. If you don't include any transitions from it in `transition`, the NFA will simply get stuck in the start state.
- `accept: Iterable[str]` is collection of the NFA accept states. 
    - This can be given as a `list`, `set`, or any other valid iterable object.
- The alphabet and total list of states are automatically inferred from the `transition` function.
- The same restrictions on naming states and letters apply here as they do for DFAs.

To see if an NFA accepts a specific word, use the `.accepts()` method:

```python
is_in_language = nfa.accepts('ab') # True or False
```

To get the whole language of an NFA, up to a certain length, use the `.L()` method:

```python
language_of_nfa = nfa.L(4) # Tuple of all accepted words up to length 4, in len-lex order
```

> [!WARNING]
> Be careful using this method with a large length value, as it will take exponential time to compute.

To print the transition table of an NFA for a nice visual, use the `.transition_table()` method:

```python
nfa.transition_table() # Prints to terminal
```

Below is an example of creating a specific NFA. This is the NFA $N_1$ in Sipser, p48.

```python
from autolang import NFA

# Create transition function dict
tran1 = {
    ('q1', '0'): ('q1',),
    ('q1', '1'): ('q1', 'q2'), 
    ('q2', ''): ('q3',),
    ('q2', '0'): ('q3',),
    ('q3', '1'): ('q4',),
    ('q4', '0'): ('q4',),
    ('q4', '1'): ('q4',) 
}
# Create NFA itself
N1 = NFA(tran1, 'q1', ['q4'])

# Check specific words
N1.accepts('010') # False

# Generate the language up to length 3
N1.L(3) # Returns tuple

# Print transition table
N1.transition_table()
```

### Creating a PDA

A PDA is created with this constructor:

```python
PDA(transition: dict[tuple[str, str, str], tuple[tuple[str, str], ...]], 
    start: str, 
    accept: Iterable[str])
```

- `transition: dict` is a dict representing the the PDA transition function.
    - Each entry entry is of the form `(state, letter, stack_top): ((next_state1, stack_push1), (next_state2, stack_push2), ...)`.
    - Each entry encodes all possible transitions (and the corresponding letter pushed to the stack) from a given state, for a given read `letter`, for a given letter read from the stack (`stack_top`)
    - The entry's value **must be wrapped in a tuple**, even if there is only one transition, and each inner tuple must have length 2.
        - If there is only one transition, a comma must still be included after it, inside the parent tuple.
    - As with NFAs, ε-transitions are encoded using the empty string `''`. This applies to both the input letters and the stack.
    - For example, say you want the PDA to have two transitions from `q0` when reading `a` in the input word and reading `$` from the stack: one goes to `q1` and pushes `x` to the stack, and the other goes to `q2` and pushes nothing to the stack. The `transition` entry to encode this is `('q0', 'a', '$'): (('q1', 'x'), ('q2', ''))`
        - **NOTE**: reading a letter from the stack automatically means it gets popped from the stack. If no letter is read, nothing is popped.
    - If you want the PDA to transition without reading the stack, use `''` for `stack_push`, e.g. `('q0', 'a', ''): (('q1', '$'),)`. This will *not* pop the top of the stack.
    - If you want no transitions for a specific state-letter-stack_top triple, then you can omit this entry from the dict, *or* include it with an empty tuple as its value, e.g. `('q0', 'a', '$'): tuple()`.
- `start: str` is the start state of the PDA. If you don't include any transitions from it in `transition`, the NFA will simply get stuck in the start state.
- `accept: Iterable[str]` is collection of the PDA accept states. 
    - This can be given as a `list`, `set`, or any other valid iterable object.
- The alphabets (input and stack) and total list of states are automatically inferred from the `transition` function.
- The same restrictions on naming states and letters apply here as they do for DFAs and NFAs.

To see if a PDA accepts a specific word, use the `.accepts()` method:

```python
is_in_language = pda.accepts('ab') # True or False
```

To get the whole language of a PDA, up to a certain length, use the `.L()` method:

```python
language_of_pda = pda.L(4) # Tuple of all accepted words up to length 4, in len-lex order
```

> [!WARNING]
> Be careful using this method with a large length value, as it will take exponential time to compute.

To print the transition table of a PDA for a nice visual, use the `.transition_table()` method:

```python
pda.transition_table() # Prints to terminal
```

Below is an example of creating a specific PDA. This is PDA $M_1$ in Sipser, p114.

```python
from autolang import PDA
# Create transition function dict
tran1 = {
    ('q1', '', ''): (('q2', '$'),),
    ('q2', '0', ''): (('q2', '0'),),
    ('q2', '1', '0'): (('q3', ''),),
    ('q3', '1', '0'): (('q3', ''),),
    ('q3', '', '$'): (('q4', ''),)
}
# Create PDA itself
M1 = PDA(tran1, 'q1', ['q1', 'q4'])

# Check specific words
M1.accepts('0011') # True
M1.accepts('010') # False

# Generate the language up to length 3
M1.L(8) # Returns ('', '01', '0011', '000111', '00001111')

# Print transition table
M1.transition_table()
```

### Creating a Turing Machine

A Turing machine (TM) is created with this constructor:

```python
TM(transition: dict[tuple[str, str], tuple[str, str, str]], 
   start: str, 
   accept: str, 
   reject: str, 
   reserved_letters: Iterable[str] = set())
```

- `transition: dict` is a dict representing the TM transition function.
    - Each entry encodes a single transition. This includes the next state, letter written to current cell, and move direction. Note the `write` letter is written *before* moving to the next cell.
    - Each entry is of the form `(state, letter): (next_state, write, direction)`. The `direction` *must* be either an uppercase `'L'` or uppercase `'R'`.
    - For example, if you want the TM to transition to state `q1`, write `x` to the current cell, and move right, when in state `q0` and reading `a`, include this entry in the dict: `('q0', 'a'): ('q1', 'x', 'R')`.
    - The special blank-cell letter is the underscore `'_'`, and this cannot be changed.
        - For example if you want the TM to erase its current cell before moving, include `('q0', 'a'): ('q1', '_', 'R')`
    - Note that you *can* omit transitions from a TM transition function, even though they are deterministic. If you do, these transitions will automatically default to the `reject` state. This may lead to unintended behaviour if you forget to add transitions.
        - This choice was made to make creating TMs less tedious, although it does make it easier for mistakes to happen during creation since an error is not raised. We decided defaulting to the reject state was a reasonable compromise in this situation. 
        - Additionally, there are many cases where a specific transition can't actually be reached from any starting configuration, so including it is pointless.
    - If there are *no* transitions to the `accept` state, the TM can still be created, but you will be prompted to continue with the creation, since such a TM will have an empty language.
        - We decided that it should be allowed to create TMs that cannot accept any words for research or investigations. Indeed, for many TMs it doesn't actually matter what they accept, but rather solely what they produce on their tape.
    - Since the TM will immediately halt when it enters the `accept` or `reject` state, you should not include any transitions *from* these states.
- `start: str` is the start state of the TM.
- `accept: str` is the unique accept state of the TM. The default is `'qa'`.
- `reject: str` is the unique reject state of the TM. The default is `'qr'`.
    - **NOTE**: you can use the names `'qa'` and `'qr'` for working states instead, provided you also provide distinct alternatives for the halting states. Sticking with the defaults is recommended.
- `reserved_letters: Iterable[str]` is a list of letters which are intended strictly for use on the tape, and should not be allowed in input words. There is no way to distinguish between the input alphabet and the tape alphabet without you manually stipulating it.
    - The blank letter `'_'` is *always* reserved, and doesn't need to be included in this arg.
- The alphabets (input and tape) and total list of states are automatically inferred from the `transition` function, and `reserved_letters`.
- You cannot use `'_'` as an input letter, since it will just be interpereted as blank. Any other character should be a valid letter for TMs.

To see if a TM accepts a specific word, use the `.accepts()` method:

```python
is_in_language = tm.accepts('ab') # True or False
```

To get the whole language of a TM, up to a certain length, use the `.L()` method:

```python
language_of_tm = tm.L(4) # Tuple of all accepted words up to length 4, in len-lex order
```

> [!WARNING]
> Be careful using this method with a large length value, as it will take exponential time to compute.

To print the transition table of a TM for a nice visual, use the `.transition_table()` method:

```python
tm.transition_table() # Prints to terminal
```

Below is an example of creating a specific TM. This is TM $M_2$ in Sipser, p172.

```python
from autolang import TM

# Create transition function dictionary
tran2 = {
    ('q1', '_'): ('qr', '_', 'R'), # This transition goes to reject, and can be omitted
    ('q1', 'x'): ('qr', 'x', 'R'), # Same with this one
    ('q1', '0'): ('q2', '_', 'R'),

    ('q2', '_'): ('qa', '_', 'R'),
    ('q2', 'x'): ('q2', 'x', 'R'),
    ('q2', '0'): ('q3', 'x', 'R'),

    ('q3', '_'): ('q5', '_', 'L'),
    ('q3', 'x'): ('q3', 'x', 'R'),
    ('q3', '0'): ('q4', '0', 'R'),

    ('q4', '_'): ('qr', '_', 'R'), # Can be omitted
    ('q4', 'x'): ('q4', 'x', 'R'),
    ('q4', '0'): ('q3', 'x', 'R'),

    ('q5', '_'): ('q2', '_', 'R'),
    ('q5', 'x'): ('q5', 'x', 'L'),
    ('q5', '0'): ('q5', '0', 'L')
}
# Create TM itself
M2 = TM(tran2, 'q1', 'qa', 'qr', {'x'})

# Check specific words
M1.accepts('00') # True
M1.accepts('000') # False

# Generate the language up to length 3
M1.L(10) # Returns ('0', '00', '0000', '00000000')

# Print transition table
M1.transition_table()
```

### Creating NFAs/DFAs from Regex

Note that 'regex' in this context refers to *formal* regular expressions, which only support unions (`+`) and Kleene stars (`*`).

Constructing automata that recognise the language of a given regex is quite straightforward, and is achieved by using the functions `regex_to_nfa()` and `nfa_to_dfa()`. You can also chain these functions together to directly create the DFA, without the intermediate NFA. 

```python
from autolang import regex_to_nfa, nfa_to_dfa

R = '(0+1)0*' # define regex - words that start with 0 or 1, followed by zero or more 0s

nfa = regex_to_nfa(R) # Create NFA
dfa = nfa_to_dfa(nfa) # Create corresponding DFA

# Or, create dfa directly
dfa = nfa_to_dfa(regex_to_nfa(R))
```

Note you can also create a DFA *any* existing NFA, not just one that was created from a regex.


## Design Philosophy

Below we discuss the overall aims of the project in more detail.

### Accessibility
Python was chosen as the main language of the project because the language is relatively easy to read and start using, and it is frequently the language of choice in academia for people who must do some coding as part of their study or research, but are not computer scientists. While Python is not the most performant language, its dynamic typing, concise syntax, and other features are amazing for accessibility and fast development, and make it a great language to demonstrate the theory to a more general interested audience. We envisioned the use of autolang to look something like this:
- The student attends a lecture or tutorial, and learns a theoretical concept, or sees a specific example of an automaton.
- The student returns home and wants to solidify their understanding, or the concept didn't quite 'click' with them.
- They open Jupyter notebook (or another Python environment) and import *autolang*
- They run their own code 'experiments' to better understand the automaton behaviour, and they can prepare for the next lecture without worrying about not understanding the previous one.
    - The student could for example create the example machine from the lecture, and pass it specific words that were covered. They could then pass in words that were not covered to see how the behaviour differs.
    - They could also design their own machines that were not seen in lectures at all, for instance if they come up with a language and want to create a machine that recognises it. This could intellectually reward them when they come up with a working machine, and also encourage them to revise the theory if their machine recognises the wrong language or doesn't work at all.
- The student returns to class, more confident that they understand automata and ready to learn more!

### Tactile Intuition
'Tactile intuition' is quite a nebulous term, but is intended to capture the idea that users can 'see the concepts working' themselves, as opposed to simply reading them in a textbook or hearing them in a lecture, and getting the *sense* of understanding without the practical experience of doing exercises, which may reveal that *sense* to actually be false. Of course the textbooks and lectures are essential and are the most important aspect of learning automata theory. Understanding the formal proofs, doing pen-and-paper exercises, and generally using one's mind to think through automata behaviour, can never be substituded for naively entering commands in a Python terminal and trying to reverse-engineer the code's behaviour. Instead, 'tactile intuition' should be interpreted as a way to *supplement* the pen-and-paper work and approach the theory from a different angle. Some students may find that this hands-on approach causes concepts to 'click' with them more easily, whereas others may be more comfortable simply writing proofs and doing exercises with no additional material. In either case we believe that having more tools available will always be beneficial, provided they are used correctly by a motivated student, and are used to enhance theoretical understanding and not to take shortcuts which inhibit real learning.

Tactile intuition firstly covers the idea of *interactability*, which is always present when coding because users must write the function/API calls themselves. Having to manually create automata, including every specific detail of a transition function and other syntax, may make the student feel there is more 'intention' to their learning, and force them to carefully consider the precise components of the theory, rather than convincing themselves that they understand the general idea without catching the inner nuances. 

Tactile intuition is also meant to cover a *visual* aspect to learning the theory, but it felt somewhat dishonest to say this earlier when the main visualisation features have not yet been developed for *autolang*. We plan in future versions to implement a far more interactive graphical way to investigate automata, such as showing step-by-step animations of a machine transitioning between states. We do have a feature for plotting static transition diagrams, but these are not optimised and may produce intractable or 'ugly' visuals for complex unseen automata. Transition diagrams are often thought to be a very intuitive way of understanding the machines, despite being less precise than formal descriptions, and the diagrams that appear in textbooks and teaching materials are of course curated to have a nice clean layout for this purpose. However, these are inherently limited to which specific machines the authors decided to include at the time of publication. We envision the benefit of *autolang*'s visuals to be their *versatility*, i.e. visuals can be generated for an arbitrary machine that the user decides to create, even if their layout may be suboptimal. For more information on planned features, see the [Roadmap](#roadmap) Section. 



## Documentation
This README file serves as the current documentation of autolang. Unfortunately a more comprehensive official documentation does not exist, yet...


## Contributing
Due to how early in development *autolang* is, we are currently **not** looking for any additional contributors, until the project is more robust and its scope has been better defined. You are of course free to fork the project or use any of its constituent code however you wish.

### Issues

*autolang* is a single-person project that is early in development, and therefore there are likely numerous bugs and issues in the current version. If you discover a bug, you are both very welcome and encouraged to notify us about it. You should do this either by raising the issue on the official GitHub repository (https://github.com/fawnium/autolang), or by sending an email directly to the contact address(es) listed in the repository. If you do wish to report an issue, please be as detailed and specific as you can be in your explanation, and if possible, include a minimal code which reproduces the issue.

We are very grateful to receive any comments or constructive criticism about the project!


## Testing
*autolang*'s tests are implemented using the standard Python `unittest` module, and testing requires no additional dependencies. All test files are located flat inside the `tests/` folder in the parent `autolang/` directory. To run all tests, use the following command while your working directory is the parent directory:

```bash
python -m unittest discover tests
```

**NOTE:** Our unit tests are an ongoing work in progress, and may not be particularly robust or compehensive. We are currently working on improving test-case coverage.

## Roadmap

While *autolang* is very early in development, we are excited that it is being actively and rapidly developed. We plan to expand the scope both by implementing more of the canonical algorithms from the theory in Sipser, and enhancing usability by including visualisations and a more comprehensive UI/UX.

Below is the general roadmap for the near future of the project. Please be aware that these features may change in terms of order of implementation and whether they will actually be added.

### v0.2.0

- Transition diagrams for all existing models using `networkx` and `matplotlib`
    - This feature is very close to being in a usable state, and just needs to be integrated with the existing project
    - There will likely be options both to plot diagrams inline (i.e. for jupyter notebooks), and save them as an image for non-graphical/terminal-based environments

- Option to store formatted transition tables (i.e. as a string), in addition to printing them directly to the terminal

- Support accessing TM tape outside of just computing words.

### v0.3.0

- Implement a class to represent context-free grammars (CFGs)

- Convert CFGs to Chomsky normal form and further normalisation

### v0.4.0

- Support generating parse-trees for specific words in a CFG

- Visuals for parse trees

- Construct PDAs directly from CFGs via canonical methods, analagous to NFAs from regular expressions in v0.1.0

### v0.5.0

- Implement different TM models, such as multi-tape and nondeterministic

- Implement other automaton models such as LBA and DPDA

### v0.6.0

- Convert multi-tape TMs to single-tape via canonical construction

### Unspecified/Later Versions

- Support more streamlined ways of initialising automata, in addition to manually typing out Python dicts

- Create a user-friendly GUI to allow visual exploration of all the features in the project, and show animations of the automata computing
    - This could also include step-by-step playback of computing particular words by highlighting active states

- Implement macros which allow running minimal high-level code directly on a Turing machine
    - This is intended as an illustrative/tactile proof-of-concept of the universality of Turing machines


## License
*autolang* has a standard MIT license, and is completely open-source and free to use by anyone for any reason. This project is a single-person hobby project with no commercial parties involved. If the project's status changes in the future, these changes will be broadcast via the official GitHub repository, and other channels if applicable at the time. There are currently **no** plans to change the intellectual property status of *autolang*.

## Credits and Acknowledgements
At the time of writing the only contributor to *autolang* is Lyons / 'fawnium'.

Many thanks are extended to Prof Roney-Dougal and Dr Huczynska at the University of St Andrews, who ran a course on automata theory that inspired and motivated this project to be developed.

Thanks are also extended to Michael Sipser *et al* for writing *Introduction to the Theory of Computation*, a textbook that was invaluable for providing the necessary theory to develop the project.