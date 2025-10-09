# autolang v0.1.0

*README last updated 09/10/2025*

*autolang* is a simple Python project based around finite-state automata, formal languages and grammars, and Turing machines. It is intended for educational use, so that students who are studying the theory within this area may supplement their understanding by creating and running their own real automata to see how they work. 

The project is heavily based on the theory from *Introduction to the Theory of Computation* by Michael Sipser.

> [!WARNING]
> A critical memory bug has been discovered in the current version, which can potentially freeze your system.
> Calling the `.L()` method of an automata object, or another method which generates all words over an alphabet, will attempt to allocate memory for the *entire* alphabet simultaneously.
> This can run into several GB of memory for even moderate-length alphabets. There are no safety measures for this at either the *autolang* or Python level.
> To avoid this issue, only use small lengths for alphabet size, e.g. `.L(10)` and **not** `.L(30)`. Safety will vary depending on the number of letters in the alphabet, so always stay under length 10 to be safe and avoid system freezes.
> This bug will be patched within the next 7 days.

- **version** : 0.1.0
- **license** : MIT standard license
- **build status** : prototype/WIP
- **Python version** : 3.12+
- **Python dependencies** : only the standard library
- **official repository** : https://github.com/fawnium/autolang
- **enquiries** : oisinlyons1@gmail.com

v0.1.0 is the initial release, which includes creating and simulating various automaton models, printing transition tables, and constructing automata from regular expressions via canonical methods. See [Features](#features) for more details.

Many more features are planned, as outlined in the [Roadmap](#roadmap)

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
- `.accepts(word: str) -> bool` - Takes a string as input, returns  `True` if the given automaton accepts the string, returns `False` otherwise. If the string contains unrecognised letters, `.accepts()` will always return `False`.
    - **NOTE:** The Turing machine instance of this method (`TM.accepts()`) can also return `None`. This happens when the word is undecidable, or the TM exceeds a certain number of steps.

- `.L(n: int = 5) -> tuple[str, ...]` - Takes an integer $n$ as input, returns a tuple of all words recognised by the given automaton with length $\leq n$, in len-lex order.
    - **NOTE:** There are currently no safety measures for handling very large languages. Be careful running this method with a large alphabet size or input length, as it may take a long time to terminate.

- `.transition_table()` - Prints the transition table of the given automaton to the terminal.
    - **NOTE:** This feature may change in future versions, i.e. by returning a string instead of printing directly.

For guidance on creating specific automata, see [Usage](#usage) below.

### Constructing Automata

In addition to manually creating and simulating automata, *autolang* has a few functions to construct automata using canonical algorithms. These are listed below:

- `regex_to_nfa(regex: str) -> NFA` - Takes a regular expression string as input, returns an NFA that recognises the corresponding regular language.
    - **NOTE:** The union operator *must* be represented as `+`. The Kleene star operator is `*` as usual. No other operators may be included in the input string.

- `nfa_to_dfa(nfa: NFA) -> DFA` - Takes an `NFA` object as input, returns the corresponding DFA, generated via the standard subset construction.
    - **NOTE:** The subset construction is *lazy*, so only states that are actually reachable from the start state are included in the final DFA.
    - **NOTE:** No further optimisation/minimisation occurs after the initial construction. This is a planned feature.


For additional planned features, see the [Roadmap](#roadmap) Section below.
See the [Usage](#usage) Section for specific explanations of how to use the existing features.

## Installation

While usability is stated as a priority for *autolang*, please note the installation process is currently a work-in-progress, and is more 'hands-on' then we would like it to eventually be. We recommend using the [Developer](#developer-install) install process below.

### Developer Install (Recommended)

#### Cloning the Repository

To create a copy of *autolang* on your computer to work with, do the following:

- Ensure `git` is installed on your computer and it can be run from your terminal;
- Navigate to the folder you want to install autolang in;
- Clone the *autolang* repository to your local folder by running the following terminal command:

```bash
git clone https://github.com/fawnium/autolang.git
```

- Then, navigate to the installed folder with this command:

```bash
cd autolang
```

#### Running the code

*autolang* is in standard src layout, and can be installed via pip. Once you have set up a virtual environment if required, run the following command:

```bash
pip install -e .
```

This will tell Python where to find the *autolang* module. After that, you should be able to import as usual:

```python
from autolang import DFA # See examples/ for other features
```

### User Install

User install is currently a work in progress and has not been tested, but you should be able to install directly from the GitHub repository by running the following terminal command:

```bash
pip install git+https://github.com/fawnium/autolang
```


## Usage

This section only describes how to use features once they have been imported. For the correct way to import specific classes and functions, see the [Installation](#installation) Section.

Example use cases of all the main *autolang* features are provided in the corresponding files in the `examples/` folder. Please refer to these if you are unsure how to use the features.

### Creating a DFA

Here we detail how to create and use the DFA $M1$ in Sipser p36, which recognises the language 

$$\{w \in \{0, 1\}^* \mid w \text{ contains at least one `1' and the final `1' is followed by an even number of `0's}\}$$

 Creating other types of automata is similar, but they differ in how specifically to encode the transition function, and other intrinsic differences between the models. See the files in `examples/` for more details. 

A DFA is created by using the constructor `DFA(transition: dict[tuple[str, str], str], start: str, accept: Iterable[str])`. It needs three arguments: the `transition` function; the `start` state; and the `accept` states, which can be given as a `list`, `set` or any other `Iterable` container. You do not need to pass the alphabet or set of states to construct the DFA - these are automatically inferred from the transition function.

The transition function is a dictionary which must be encoded in a specific way. Each key in the dictionary is a pair `(state, letter)` where `state` and `letter` are strings, and the corresponding value is a string `next_state`. Each key-value pair in the dictionary corresponds to a transition in the transition function. For example, if you want the DFA to transition from `q0` to `q1` when reading the letter `a`, include `('q0', 'a'): 'q1'` in the dictionary. You must ensure that you include transitions for every possible letter from every possible states, otherwise an error will be raised. You must also ensure that the additional arguments `start` and `accept` only include valid states that appear in the transition function. Take care to check all strings as they are case-sensitive. Note than some characters are forbidden from appearing in state names, such as `'+'` or `'_'`. To be safe, you can restrict names to numbers and upper- and lower-case Latin letters.

Below is how to create the DFA $M1$ in Sipser, p36. It is worth checking the transition diagram in the textbook to see the correspondence:

```Python
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
```

Now that `M1` has been created, you can give it words to compute or generate its language:

```Python

M1.accepts('000') # Will return `False`
M1.accepts('100') # Will return `True`

# Generate the language of M_1 up to length 3
M1.L(3) # Will return `('1', '01', '11', '001', '011', '100', '101', '111')`
```

You can also print the DFA's transition table for better readability compared to the input dict:

```python
M1.transition_table() # Prints to the terminal when run
```

For further specific DFA constructions see `examples/dfa_examples.py`.

### Creating an NFA

Creating an NFA is similar to a DFA with some nuances. The constructor is `NFA(transition: dict[tuple[str, str], tuple[str, ...]], start: str, accept: Iterable[str])`. Almost everything is the same as the DFA case, except now the values in the transition dictionary must be *tuples* of strings and not a single string, due to nondeterminism. This applies regardless of whether the NFA has zero, one, or many allowed transitions from a given state. If you want the NFA to transition from `q0` to `q1` when reading `a`, include `('q0', 'a'): ('q1',)` in the dictionary. Note that the next state `q1` must be wrapped inside a tuple, and ensure that a comma is inserted so it is recognised as such. If you want the NFA to be able to transition to both `q1` *and* `q2` when in state `q0` and reading `a`, then include `('q0', 'a'): ('q1', 'q2')` in the dictionary. If you want the NFA to have *no* transitions from `q0` when reading `a`, you can simply omit the entry from the dictionary (which is allowed here *unlike* the DFA case), or if you really want you can include the entry `('q0', 'a'): tuple()` which signals an empty tuple of next states. 

Epsilon transitions are simply encoded as the empty string `''` instead of a letter. For example, an epsilon transition from `q0` to `q1` will look like `('q0', ''): ('q1',)` in the dictionary.

For specific NFA constructions see `examples/nfa_examples.py`.

### Creating a PDA

The constructor for creating a PDA is `PDA(transition: dict[tuple[str, str, str], tuple[tuple[str, str], ...]], start: str, accept: Iterable[str])`. The `start` and `accept` arguments are exactly the same as above. 

Now the transition dictionary keys have length $3$ instead of $2$. The order of the key tuple is `state`, `letter`, `stack_top`. The dictionary values are tuples of zero or more transitions, just like with NFAs, except now the entries in the tuples are *themselves* tuples of length $2$, and not strings. Each 2-tuple inside a parent tuple is of the form `(next_state, stack_push)`. 

As an example, suppose you want the PDA have *two* transitions from `q0` when reading `a` in the input word and reading `$` from the stack. The first transition goes to `q1` and pushes `x` to the stack, and the second goes to `q2` and pushes nothing to the stack. The correct dictionary entry to encode this is `('q0', 'a', '$'): (('q1', 'x'), ('q2', ''))`. You must be careful when formatting nested tuples like this, and ensure there is still a comma inside the parent tuple even if there is only one transition, as with the NFA case.

For specific PDA constructions see `examples/pda_examples.py`.

### Creating a TM

TMs are the most complex and unique of the models supported in *autolang*, and hence are the most distinct in their construction, but they are still fairly similar. The constructor is `TM(transition: dict[tuple[str, str], tuple[str, str, str]], start: str, accept: str, reject: str, reserved_letters = set()))`.

The `start` argument is the same as above. For TMs there is no longer a list of accept states. Instead, there is a single unique `accept` state and a single unique `reject` state, and these have the default values `qa` and `qr` respectively. You may use these names for working states instead, provided you also provide distinct alternatives for the accept and reject states. The `reserved_letters` argument is for stipulating letters which are strictly reserved for the tape alphabet, and should *not* be included in the input alphabet. Unfortunately there is no way to automatically distinguish between which letters should and should not be allowed in the input. Note that the special blank letter is represented as an underscore `'_'`. This character can *never* be used in the input alphabet, and does not need to be included with the other reserved letters.

The TM `transition` dictionary entries must all have the form `(state, letter): (next_state, write, direction)`, where all are strings. `state` is the current state, `letter` is the letter in the current cell, `next_state` is the state to transition to, `write` is the letter to write to the current cell, and `direction` *must* either be `'L'` or `'R'`. Recall that DFAs are deterministic and must have a defined transition for every possible state-letter pair. TMs are also deterministic, but we made the decision to allow missing transitions here because many practical examples of TMs display this when a transition could never theoretically be reached for any input. This is of course risky, because you the user may forget necessary transitions, and there is no way to distinguish between mistakes and transitions that were intended to be omitted. It is likely that a future version of *autolang* will automatically add missing transitions, which will default to the reject state.

**NOTE:** You *are* able to create TMs with no transitions to the accept state, even though machines will have an empty language. If you do so, you will be prompted to proceed, in case this omission was a mistake.

For specific TM constructions see `examples/tm_examples.py`.

### Creating NFAs/DFAs from Regex

Constructing machines that recognise the language of a given regex is quite straightforward. Suppose you want an NFA that recognises the regex $(0+1)0*$. To do this, simply write:
```Python
nfa = regex_to_nfa('(0+1)0*') # You can use any name instead of `nfa` 
```
Then, to convert it to a DFA, write:
```Python
dfa = nfa_to_dfa(nfa) # Make sure you pass the correct `NFA` object
```
You can also create the dfa directly by writing:
```Python
dfa = nfa_to_dfa(regex_to_nfa('(0+1)0*'))
```
You can also create a DFA from *any* existing NFA, not just one that was created from a regex.


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
python -m unittest discover
```

**NOTE:** Our unit tests are an ongoing work-in-progress, and may not be particularly robust or compehensive. We are currently working on improving test-case coverage.

## Roadmap

While *autolang* is very early in development, we are excited that it is being actively and rapidly developed. We plan to expand the scope both by implementing more of the canonical algorithms from the theory in Sipser, and enhancing usability by including visualisations and a more comprehensive UI/UX.

Below is the general roadmap for the near future of the project. Please be aware that these features may change in terms of order of implementation and whether they will actually be added.

### v0.2.0

- Transition diagrams for all existing models using `networkx` and `matplotlib`
    - This feature is very close to being in a usable state, and just needs to be integrated with the existing project
    - There will likely be options both to plot diagrams inline (i.e. for jupyter notebooks), and save them as an imagine for non-graphical/terminal-based environments

- Option to store formatted transition tables (i.e. as a string), in addition to printing them directly to the terminal

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