# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Problem Set 1
# **Tong Wu**  
# *September 17, 2021*

# ## Question 0 - Markdown warmup

# ***
# This is *quesiton o* for [problem set 1][ps] of [Stats 507][st].  
#
# >Question o is about Markdown.
#
# The next question is about the **Fibonacci Sequence**, $F_{n}=F_{n-2}+
# F_{n-1}$. In part **a** we will define a Python function `fib_rec()`.  
#
# Below is a...
#
# ### Level 3 Header
# Next, we can make a bulleted list:
# - Item 1
#   + detail 1
#   + detail 2
# - Item 2  
#
# Finally, we can make an enumerated list:  
# 1. Item 1  
# 2. Item 2  
# 3. Item 3  
#
# [ps]: https://jbhender.github.io/Stats507/F21/ps/ps1.html
# [st]: https://jbhender.github.io/Stats507/F21/
# ***

# # Correction for this homework
# Comment from GSI: 
# - Q0: -3 for not provide both raw and formatted versions.

# Below is the raw markdown:
    
```
---
This is *quesiton o* for [problem set 1][ps] of [Stats 507][st].  

>Question o is about Markdown.

The next question is about the **Fibonacci Sequence**, $F_{n}=F_{n-2}+
F_{n-1}$. In part **a** we will define a Python function `fib_rec()`.  

Below is a...

### Level 3 Header
Next, we can make a bulleted list:
- Item 1
  + detail 1
  + detail 2
- Item 2  

Finally, we can make an enumerated list:  
1. Item 1  
2. Item 2  
3. Item 3  

[ps]: https://jbhender.github.io/Stats507/F21/ps/ps1.html
[st]: https://jbhender.github.io/Stats507/F21/
---
```

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem set 1 - Question 0 and Question 1.

@author: Tong Wu
@date: September 10, 2021
"""
import math
import numpy as np
import pandas as pd
import datetime

# ## Question 1 - Display Fibonacci Sequence
# The Fibonacci sequence can be defined as follow:  
# <center>$F_{n} = F_{n-2} + F_{n-1}$, with $F_{0} = 0$ and $F_{1} = 1$.
# </center>

# **a. Write a function `fib_rec` using recursion.**  
# - Note that a **recursive function** is a function that will continue to call 
# itself until certain condition is met.

def check_input(n):
    """
    A function to check whether the input is an non-negative integer or not.

    Parameters
    ----------
    n : int
        The nth number of Fibonacci sequence which starts from 0..

    Returns
    -------
    Raise exception if the input is invalid.

    """
    if isinstance(n, int):
        if n < 0:
            raise Exception("Please enter a non-negative integer.")
    else:
        raise Exception("Please enter a non-negative integer.")


def fib_rec(n):
    """
    A recursive function generating Fibonacci numbers.

    Parameters
    ----------
    n : int
        The nth number of Fibonacci sequence which starts from 0.

    Returns
    -------
    The value of F_n.

    """
    check_input(n)
    if n <= 1:
        return n
    else:
        return(fib_rec(n-2) + fib_rec(n-1))


# **b. Write a function `fib_for` using a `for` loop.**

def fib_for(n):
    """
    A function generating Fibonacci numbers using for loop.

    Parameters
    ----------
    n : int
        The nth number of Fibonacci sequence which starts from 0.

    Returns
    -------
    The value of F_n.

    """
    a = 0
    b = 1
    
    check_input(n)
    if n == 0 or n == 1:
        return n
    else:
        for x in range(1,n):
            temp = a + b
            a = b
            b = temp
        return temp


# **c. Write a function `fib_whl` using a `while` loop.**

def fib_whl(n):
    """
    A function generating Fibonacci numbers using while loop.

    Parameters
    ----------
    n : int
        The nth number of Fibonacci sequence which starts from 0.

    Returns
    -------
    The value of F_n.

    """
    a = 0
    b = 1
    i = 1
    
    check_input(n)
    if n == 0 or n == 1:
        return n
    else:
        while i < n:
            temp = a+b
            a = b
            b = temp
            i += 1
        return temp


# **d. Write a function `fib_rnd` using rounding method.**    
# By using the [rounding method][rm], $F_{n}$ can be found as follows:
# <center>$F_{n}=\left[\frac{\varphi^{n}}{\sqrt{5}}\right], n \geq 0$, where
# $\varphi=\frac{1+\sqrt{5}}{2} \approx 1.6180339887 \ldots$</center>
#
# [rm]: https://en.wikipedia.org/wiki/Fibonacci_number

def fib_rnd(n):
    """
    A function generating Fibonacci numbers using rounding method.

    Parameters
    ----------
    n : int
        The nth number of Fibonacci sequence which starts from 0.

    Returns
    -------
    The nearest integer for the computation result using rounding 
    function, which is the value of F_n.

    """
    check_input(n)
    
    phi = (1 + math.sqrt(5)) / 2
    
    return round(pow(phi, n) / math.sqrt(5))


# **e. Write a function `fib_flr` using truncation method.**  
# By using the [truncation method][tm], $F_{n}$ can be found in terms of the 
# floor function: <center>$F_{n}=\left\lfloor\frac{\varphi^{n}}{\sqrt{5}}+
# \frac{1}{2}\right\rfloor, n \geq 0$, where $\varphi=\frac{1+\sqrt{5}}{2} 
# \approx 1.6180339887 \ldots$</center>
#
# [tm]: https://en.wikipedia.org/wiki/Fibonacci_number

def fib_flr(n):
    """
    A function generating Fibonacci numbers using truncation method.

    Parameters
    ----------
    n : int
        The nth number of Fibonacci sequence which starts from 0.

    Returns
    -------
    The greatest integer less than or equal to the computation result 
    using truncation method, which is the value of F_n.

    """
    check_input(n)
    
    phi = (1 + math.sqrt(5)) / 2
    
    return math.floor((pow(phi, n) / math.sqrt(5) + 1/2))


# **f. Compare the median computation time of each of the functions.**  
# - Use `np.linspace(start, stop, num)` to generate a sequence of evenly 
# spaced increasingly large values of n.  
#   + Note that this generated sequence is a ndarray of float, not integers.
#     Thus, we may need to convert its datatype if necessary.
# - After trying different ranges of ns, the range below is chosen. The
# maximal n we choose is 40, because a larger n consumes a lot of time when 
# we use the recursive function.

ns = np.linspace(10, 40, 7)

def run_time(n, fn):
    """
    Computation time of a given function and a given n.
    We use datetime module to measure the running time in microseconds. 

    Parameters
    ----------
    n : int
        The nth number of Fibonacci sequence which starts from 0.
    fn : function
        This is the function used to generate Fibonacci Sequence.

    Returns
    -------
    The computation time (in microseconds) of certain generating function.

    """  
    t_begin = datetime.datetime.now()
    fn(n)
    t_end = datetime.datetime.now()
    
    return ((t_end - t_begin).seconds * 1e+6 + (t_end - t_begin).microseconds)


def t_ktimes(k, fn):
    """
    A function used to store computation time that a Fibonacci generating 
    function runs k times for each n.
    
    Parameters
    ----------
    k : int
        The number of running times.
    fn : function
         The function used to generate Fibonacci Sequence.
         
    Returns
    -------
    A list to store computation time that a function runs multiple times.

    """
    L = []
    for n in ns:
        L.append([])
        for i in range(1, k+1):
            t = run_time(int(n), fn)
            L[ns.tolist().index(n)].append(t)
    return L

def t_kmedian(fn, k = 5):
    """
    A function used to compute medians for each function after running 
    k times.

    Parameters
    ----------
    k : int
        The number of running times and the default running times is 5.
    fn : function
         The function used to generate Fibonacci Sequence.

    Returns
    -------
    None.

    """
    L1 = t_ktimes(k, fn)
    L2 = []
    for i in range(len(L1)):
        m = np.median(L1[i])
        L2.append(m)
    return L2  


# Construct a `pd.DataFrame` table that shows all medians using all methods 
# above for each n.
# - Note that all medians are measured in microseconds after running 5 times.

index_names = [('n = ' + str(int(n))) for n in ns] 

ml = {
      'Recursion': t_kmedian(fib_rec),
      'For Loop': t_kmedian(fib_for),
      'While Loop': t_kmedian(fib_whl),
      'Rounding': t_kmedian(fib_rnd),
      'Truncation': t_kmedian(fib_flr),
    }

df = pd.DataFrame(ml, index = index_names)

print(df.to_markdown())
print(df)

# From above table, we can find that (running times = 5):
# - The generating funciton using Recursive method has the maximal median 
# computation time for each n.
# - Functions using rounding method and truncation method are more likely take
# less time to generate Fibonacci number even if n becomes larger.
