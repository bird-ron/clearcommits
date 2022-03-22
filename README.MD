## What is this?
This script purges all commits from a git branch without destroying any work, both locally and remotely.

## How do I use this?
Run it from the command line.

usage: purgecommits.py \[-h\] \[-m MESSAGE\] \[-p\] \[-q\] \[-r REMOTE\] \[-t TEMP\] branch

| positional argument | description     |
|---------------------|-----------------|
| branch              | branch to purge |

| optional argument             | description                                          |
|-------------------------------|------------------------------------------------------|
| -h, --help                    | show this help message and exit                      |
| -m MESSAGE, --message MESSAGE | commit message (defaults to "REDACTED")              |
| -p, --pause                   | pause before exiting                                 |
| -q, --quiet                   | produce no console output                            |
| -r REMOTE, --remote REMOTE    | name of remote repository (defaults to "origin")     |
| -t TEMP, --temp TEMP          | temporary name of orphan branch (defaults to "temp") |

## Can I get some examples?
Sure.
This is the simplest example.
It purges the entire commit history of the main branch:
* **.py**: python purgecommits.py main
* **.exe**: start purgecommits main

Here's a more complicated one:
* **.py**: python purgecommits.py main -m "PURGED COMMIT HISTORY" -p -q -r origin -t jeff
* **.exe**: start purgecommits "main -m ""PURGED COMMIT HISTORY"" -p -q -r origin -t jeff"

The more complicated example does this:
* purges the commit history of main
* commits with the message "PURGED COMMIT HISTORY"
* pauses before exiting
* logs no output to the console
* explicitly specifies the remote as "origin" (despite this being the default)
* uses "jeff" as the temporary name given to the origin branch

## Should I use the .py file or the .exe file?
They do the same thing, so it's completely up to you.
If you're not on Windows or don't like .exe files, use the .py file.
Additionally, you can compile your own executable using compile.py.

## I got an error and I'm upset.
This script checks for two errors:
1. It won't let you purge the commit history unless your local branch is synchronized with the remote branch (no commits 
ahead or behind).
2. It won't let you purge a branch that doesn't exist.

If you're sure that both of these cases are not the issue, then yell at me.
I can probably figure it out. 
Maybe.

## But why?
Haven't you ever made a questionable commit?
Maybe you were just testing out some sort of git command, and now the logs proclaim "sdfgsjlkjwer".
Maybe you were so frustrated you committed something with nasty words and foul language.
Maybe you're working on a software portfolio, and you'd rather nuke your commit history instead of going through it and
making sure it all looks "professional."
Not like any of these things apply to me -- I just decided to make this for **absolutely no reason.** 
Promise.

## But wait -- *should* I use this?
Probably not.
* If you're working solo on a personal project, go ahead.
* If you're working with a buddy or a group of friends, just run it by them first.
* If you're working on a dev team and doing some serious software engineering, the fact that you found this repo is 
somewhat frightening. 
**Do not.**

## I committed secrets, but then I got rid of the offending files and used this script. We cool?
No, we're not cool.
Once you publish private secrets to the public internet, they are no longer secret.
You need to invalidate those secrets and make new ones.

## I miss my old commits. Can I have them back?
No. 
Unless you have a backup somewhere, then yes.
Force push the backup branch, and you're good to go.

## I can still access old commits. Why?
GitHub performs garbage collection once a week.
This is when all the commits that are not part of any repo get deleted.
If you really, really can't wait for garbage collection to kick in, then you need to delete your current repo and make
a new one.

## My antivirus said this code is a trojan and I am scared.
It's not.
I've heard some people get a similar issue when using pyinstaller.
If it really bothers you, just run it as a Python script.
You could also try compiling your own executable.
