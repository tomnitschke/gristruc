# Grist RUC - Reusable User Code
When working with [Grist](https://www.getgrist.com) on an advanced level, there inevitably comes a moment when you find you're repeating yourself. Formulas doing the same kind of thing, or roughly the same thing, start appearing everywhere and you're wondering, couldn't I re-use that stuff I already got working in that other cell?

So, at some point larger Grist projects really benefit from a central code library. Unfortunately, Grist doesn't yet provide an elegant way of creating one, but with a bit of hackery, it can be done. Once set up, you can then stuff your library full of all the code goodness hopefully to be found here once it's all up and running, empower your formulas significantly, and stop doing the same stuff over and over again!

## Great! So how do I use this?
In your Grist document, create a new table. Give it a name like "Lib" or "Code" or something that both makes sense and is fast to type! It might be a good idea to name it in ALL-CAPS to make it stick out against regular tables in your project.

In this table, create just one record and make sure all columns are formula columns. This is where you paste the code from this repo. The trick is to have a formula column spit out something that can be called rather than an actual value. This allows the column to be referenced by Grist's usual means and "called" as if it were a normal Python function. To illustrate, here's an example formula column, let's call it "QuestionBot", as part of a table named "CODE":
```
def solve_meaning_of_life(question):
   return f"You asked '{question}' - to which the answer is, as always it must be, 42."

return solve_meaning_of_life
```
A "QuestionBot" column with this formula in it will get a Python function as its value. This can be called from other places within your Project, like this:
```
# Nota bene: Using lookupOne() without any arguments will just fetch the first record.
return CODE.lookupOne().QuestionBot.solve_meaning_of_life("Pray, what does it all mean?")
```
This will put "You asked..." and so forth into the column with the above formula.

You can also use classes to organize things further:
```
class Solver:
   def solve_meaning_of_life(question):
      ... (see above) ...

return Solver
```
This may be called exactly the same way as before, but allows for having multiple functions in one column.

## Please share!
I cordially invite every seasoned or aspiring Grister to share! Open a pull request and let's add all your little snippets, advanced calculations and all-time greats!
