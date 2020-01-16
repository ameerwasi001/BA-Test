# Browser Automation-Test
This is an extensible DSL made with selenium and python for browser automation test writing with very simple and elegant syntax.

# Supported Browsers
It supports every browser that selenium supports meaning Firefox, Chrome, Safari, Edge and Internet Explorer 3 and drivers for all of them will be required.

# The knowledge required beforehand
There's very little knowledge required beforehand for starting working with this DSL because the only things you need to know are CSS selectors and xpath which is directly accessible in this language but it's totally not for someone who hasn't done any testing before because it has the exact same workflow of selecting elements in a variable and writing or clicking on them.

# Selectors
There are many methods with which elements can be selected and here are the mthods that are currently supported.\n
```
get_element_by_name
get_element_by_id
get_element_by_xpath
```
In future there are plans for more selectors that just use xpath under the hood.

# Syntax
This language has very few syntax gotcha's but it still has some and here's the basic syntax that you would need to know to start doing browser testing in this language.

## Starting a web browser
```start => chrome, C:/Browserdriver/chromedriver.exe```

So, yeah you say start, then assign arguments using this sign `=>` and the only two arguments seprated by `,` are the browser you are going to use and the path to the driver. 

## Visiting a website
```visit => https://www.google.com/```

Yep, it's that simple you just go ahead and say visit, then assign arguments using this sign `=>` and the only required argument here is the URL of the website you want to visit but make sure to add `http://www.`, because BA-Test at least for now doesn't recognize URLs without this beginning.

## Selecting an element
Similar to what we had done above we will just

```get_element_by_name => q, google_search```

but in this particular instance we assign two arguments seprated by `,` and the first argument asks for the name that you want it to search for, in a page while the second one asks for the name that you want to store it with so that you can use it later in rest of your test.

Other methods can be used in a similar manner, by just providing name, id or xpath respectively.

## Writing on an element
```write => google_search, 'PyCon is big'```

You might write on an element by first calling the name you used to store the found element which may or may not be more than one which in our case it's not so we don't need to pass any optional arguments so, the next argument here is and string because it contains spaces but if it didn't then we could have just typed `PyCon is big` instead of `'PyCon is big'` which requires either double or single quotes.
The write method presses enters unless you pass an optional argument `enter->false` in the same line.

## Wait
In the process of testing you may want to wait for certain things to happen, even though going to website by either clicking or visiting though the methods alredy does so but, you now can wait by sleeping, meaning using sleep method.\n

```sleep => 10```

The above as you might have guessed asks system to wait for 10 seconds before doing anything else.

## Comments
```# Hey, this part finds search results```

Some times you might want to write some arbitrary text for someone reading your code and to do so you can do what's done above and start you line by `#` symbol.

## Indexed elements
If we ask for an element where multiple search results are found this stores them in a list by index starting from 0 so that you can call it with index whenever required. What follows is an example for you to find search results through xpath and store all of them in a list.
```
get_element_by_xpath => //h3[@class='LC20lb'], results
click => results, index->1
```

While the first one is quite self explanatory the second one needs an explanation about the optional argument `index` being passed, it says that click the second index of the found results because results start from 0, so what it'll do is click the second index meaning the index number one which correlates to the second search result.

## Close
`close`

If you decide to close your window after a certain test is done, then you can use the `close` method with no arguments passed whatsoever.

## Variables
This language can help you store, read and re-evaluate certain variables namely strings, floats and integers.
### Setting a variable
Setting a variable is quite simple, you can just state
```
SET => int => wait = 2
```
Setting an integer is as simple as that and we can do the same for setting strings and floats.
### Getting a variable
Getting a variable is just as simple, you can just state
```
GET => wait
```
anywhere in the program so you might be thinking about how you can assign a variables value to an argument.
```
sleep => GET => wait
```
and the same thing can be done with optional arguments.

### Basic math with a variable
All basic math can be done with variables in BA-Test like this,
```
EVALUATE => ((get > wait + 1 - get > wait)*2)/2
```
where `get>` gets the variable and then the next thing is to assign it to a certain method like what follows,
```
sleep => wait -> EVALUATE => ((get > wait + 1 - get > wait)*2)/2
```
thanks, for reading through and we'll hope you'll continue to use BA-Test.

# Development
Wait, were you a developer looking for a test writing DSL for your testers or business people to use and for you to extend we got you. This language has a file named `extensions.py` where you can write methods and the will be directly accessible in this language and what follows is a plethora of things you would need to know before you can start extending this DSL to meet your needs.

## Global variables
There are a few global variables used as memory for BA-Test, the first one is **driver** which is the driver we want to use for browser automation, the second one is **elements** which ofcourse is the memory used to store elements, and the last one is **variables** which is the memory we use to store variables being set by users.

## findElement
You would have to use this function to find an element and whenever you'd have to find an element from global element you must have an element and an index argument which by default should be `None`, and what follows is an example extension of this file where I make a another function to click a button.
```
def testClicker(element, index=None):
  findElement(element, index).click()
```
## listOrNot
This is used to check the given element appropriately and to convert list to an element if nessecary and to raise appropriate errors if required and what follows is an example for a `find_element_by_class` method in extensions.
```
def find_element_by_class(elem_class, index):
  global elements
  elements[index] = driver.find_elements_by_class_name(elem_class)
  listOrNot(index)
```
## str2bool
Everything given by the language is an string with certain exceptions specifically variables inside global variable memory and what follows is an example of where it might be used
```
if str2bool(enter):
  print("we are going to press enter")
```
# What's to come
Some of the examples such as the "class" one will be implemented in core language pretty soon, more optimizations will be done for this language and more functions for developers' convenience will also be avalible.

# Thanks
This time for real, thanks for reading through and we hope to thank you for using this language for test writing purposes.
