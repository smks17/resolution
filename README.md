# Resolution method
[resolution](https://en.wikipedia.org/wiki/Resolution_(logic)) is a rule of inference leading to a refutation complete theorem-proving technique for sentences in propositional logic and first-order logic.

# Operations are supported

| name        | symbol   | character |
| :-----:     | :----:   | :---: |
| implement   | &#8594;  | ->  |
| equivalence | &#10231; | <-> |
| conjunction | &#8743;  | /\\ |
| disjunction | &#8744;  | \/  |
| negation    | &#172;   | ~   |
| for all     | &#8704;  | FA  |
| there exists| &#8707;  | EX  |

# Format of writing

for parse the clause you should write with following rules:

- your input should have space between each symbols(constant, variable, operation, braces)

example :

❌ incorrect: p->q \
✔️ correct: p -> q

❌ incorrect: p /\\ (q<->r) \
✔️ correct: p /\\ ( q <-> r )

❌ incorrect: (~p) -> q \
✔️ correct: ( ~ p ) -> q

- for each couple variable and a operation put a braces

example :

❌ incorrect: ~p->q \
✔️ correct: ( ~ p ) -> q

❌ incorrect: p /\\ q /\\\ r \
✔️ correct: p /\\ ( q /\\\ r )

❌ incorrect: p \/ q \/ r \
✔️ correct: ( p \/ q ) \/ r

### fisrt order

- don not use space in FA(x), EX(x) and functions like f(x)

❌ incorrect: FA( x ) \
✔️ correct: FA(x)

❌ incorrect: EX (x) \
✔️ correct: EX(x)

❌ incorrect: f ( x ) \
✔️ correct: f(X)

- use bracket with space for using first order opearions

❌ incorrect: FA(x)( ... ) \
✔️ correct: FA(x) ( f(x) )

❌ incorrect: EX(x) (f(x)) \
✔️ correct: EX(x) ( f(x) )

❌ incorrect: FA(x) ( f(x) ) -> EX(x) ( f(x) ) \
✔️ correct: ( FA(x) ( f(x) ) ) -> ( EX(x) ( f(x) ) )

# Usage

## cmd mode
for use from command line you can run resolution.py

type this in your shell

    python resolution.py

then you can write your premise for see result like this:

    Welcome to the resolution shell.   Type help or ? to list commands.

    > ( p /\\ q ) -> ( p \/ q )
    (True, [{'~p'}, {'~q'}, {'p'}, {'q'}])

first thing that print is True or False that means your premise(s) (and conclusion) is provable or not.

another example:

    > p -> q , p , q
    (True, [{'~p'}, {'q'}, {'p'}, {'~q'}])

in this example p -> q and p is the premises and q that clause should be prove.

and second thing that is written is the -----

note: also you can write `> exit` for exit from program 

## as package
you can really easy put ./resolution.py in your folder and import that then for use it try this:

    >>> import resolution
    >>> premises = [' p /\\\ q', 'q']
    >>> conclusion = 'p'
    >>> result = prove(premises, conclusion)
    >>> print(result)
    (True, [{'p'}, {'q'}, {'~p'}])

    >>> premises = [' FA(x) ( f(x) )']
    >>> conclusion = '( EX(y) ( f(x) ) ) -> ( EX(y) ( f(x) ) ) '
    >>> result = prove(premises, conclusion)
    >>> print(result)[0]
    True

----
for more example see ./example.py