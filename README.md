# dore
Direct Object Reference Exploitation

#### What's this?

This is a tool used to exploit **IDOR** vulnerability in an automated manner (_This is just a PoC, this tool might be ported to any other language_). Now, what do I mean by automated? It can exploit IDOR vuln. like a boss! Eventhough there are a few limitations with this too.

##### How To

- This section will have an update soon, but anyways this tool requires you to understand python so you can actually start using it right away with the help of `script.py` and Doc-strings.

##### Features

- Uses TOR by default. (local socks5 proxy as a Tor gateway) <!-- There might be a DNS leak, will look after it soon. -->
- Has got a really useful function (**get_max_id**) which basically can obtain max ID from the endpoint. (last/final numerical id) <!-- This is a limitation here. -->
- A cool UI and animations during the exploitation duration. Just try using it!
- Doc-strings to understand what what does the function actually does.
- Can be used to do perform other web explaitation tasks over Tor network, all thanks to awesome functions like `request`, `match`. These functions might look normal, but these are really powerful stuff.

##### Cons

- Currently supports numeric field (animations, and get_max_id)
- Needs refactoring since it does not follow a few good practices.

##### Todo

- Adding binary search method for the function `get_max_id`

_Note: A few functions might not work with OSX directly, working on `get_max_id` and then will start to work to port the code to be usable with OSX._

Will write this soon, but you may try to check by reading `script.py` out. And, peeking at the docstrings.

