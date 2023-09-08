**这一讲主要是介绍了概率论的基础知识以及如何用代码实现。**     
## 概率论    
概率论基础知识之前都学过，所以需要学得也就是概率论中名词的英文：      
- Not (¬)  
- And (∧)
- Or (∨)
- Implication (→) 
- Biconditional (↔) 
- Model
- Knowledge Base (KB)
- Entailment (⊨)蕴涵: If α ⊨ β (α entails β), then in any world where α is true, β is true, too.
- Inference Rules
  - Modus Ponens P → Q,若P则Q
  - And Elimination 若P ∧ Q，则P、Q 
  - Double Negation Elimination ¬¬P => P
  - Implication Elimination ->
  - Biconditional Elimination  <=>
  - De Morgan’s Law
  - Distributive Property        
(P ∨ Q) → R         
¬(P ∨ Q) ∨ R /Eliminate implication         
(¬P ∧ ¬Q) ∨ R /De Morgan’s Law     
(¬P ∨ R) ∧ (¬Q ∨ R) /Distributive Law          
- Resolution
- First Order Logic
  - Universal Quantification任意∀
  - Existential Quantification存在∃
                         
Inference:
- There are multiple ways to infer new knowledge based on existing knowledge. First, we will consider the Model Checking algorithm.         
- To determine if KB ⊨ α (in other words, answering the question: “can we conclude that α is true based on our knowledge base”)            
- Enumerate all possible models.               
- If in every model where KB is true, α is true as well, then KB entails α (KB ⊨ α).       
## 代码实现
```
from logic import *

# Create new classes, each having a name, or a symbol, representing each proposition.
rain = Symbol("rain")  # It is raining.
hagrid = Symbol("hagrid")  # Harry visited Hagrid
dumbledore = Symbol("dumbledore")  # Harry visited Dumbledore

# Save sentences into the KB
knowledge = And(  # Starting from the "And" logical connective, becasue each proposition represents knowledge that we know to be true.

    Implication(Not(rain), hagrid),  # ¬(It is raining) → (Harry visited Hagrid)

    Or(hagrid, dumbledore),  # (Harry visited Hagrid) ∨ (Harry visited Dumbledore).

    Not(And(hagrid, dumbledore)),  # ¬(Harry visited Hagrid ∧ Harry visited Dumbledore) i.e. Harry did not visit both Hagrid and Dumbledore.

    dumbledore  # Harry visited Dumbledore. Note that while previous propositions contained multiple symbols with connectors, this is a proposition consisting of one symbol.             
                # This means that we take as a fact that, in this KB, Harry visited Dumbledore.
    )
```
To run the Model Checking algorithm, the following information is needed:

Knowledge Base, which will be used to draw inferences
A query, or the proposition that we are interested in whether it is entailed by the KB
Symbols, a list of all the symbols (or atomic propositions) used (in our case, these are rain, hagrid, and dumbledore)
Model, an assignment of truth and false values to symbols
The model checking algorithm looks as follows:
```
def check_all(knowledge, query, symbols, model):

    # If model has an assignment for each symbol            
    # (The logic below might be a little confusing: we start with a list of symbols.            
    # The function is recursive, and every time it calls itself it pops one symbol from the symbols list and generates models from it.           
    # Thus, when the symbols list is empty, we know that we finished generating models with every possible truth assignment of symbols.)
    if not symbols:

        # If knowledge base is true in model, then query must also be true
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    else:

        # Choose one of the remaining unused symbols
        remaining = symbols.copy()
        p = remaining.pop()

        # Create a model where the symbol is true
        model_true = model.copy()
        model_true[p] = True

        # Create a model where the symbol is false
        model_false = model.copy()
        model_false[p] = False

        # Ensure entailment holds in both models
        return(check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false))
```
## **总结：**        
首先引入头文件logic(需要自己写这个文件）
```
from logic import *
```
然后定义symbol，
```
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gryffindor"),
        Symbol(f"{person}Hufflepuff"),
        Symbol(f"{person}Ravenclaw"),
        Symbol(f"{person}Slytherin")
    ))
......
mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
......
symbols = characters + rooms + weapons
......
```
再添加knowledge的信息
```
knowledge = And(
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, revolver, wrench)
)
knowledge.add(
                    Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}")))
                )
......
```
最后
```
for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)
```
