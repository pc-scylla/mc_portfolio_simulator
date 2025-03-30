
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Description:
#   A small python program to run Monte Carlo simulation on a portfolio
#
# How to run:
#############
# To see the simulation plot and result
# python .\mc_portfolio_simulator.py -d 
# 
# To see the result
# python .\mc_portfolio_simulator.py
#
# Historical data  
# Ref: https://curvo.eu/backtest/en/market-index/sp-500?currency=eur
#   Time period February 1992 to February 2025 for S&P500
#   Average annualised return = 11.21% ----> use 7% to be conservative
#   Annualised standard deviation of the monthly excess returns = 15.20% 
#   Also the Sharpe ratio of 0.69.
#
###############################################################################
# MIT License
#
# Copyright (c) 2025 pc-scylla
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import sys

# Define exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def print_error(msg):
    print(f"ERROR: {msg}\n")

try:
    import numpy as np
except ModuleNotFoundError:
    print_error("'numpy' is missing from the python installation")
    print("Try the following to resolve the problem")
    print("pip install numpy")
    sys.exit(EXIT_FAILURE)  # Exit with FAILURE

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print_error("'matplotlib' is missing from the python installation")
    print("Try the following to resolve the problem")
    print("pip install matplotlib")
    sys.exit(EXIT_FAILURE)  # Exit with FAILURE

def monte_carlo_simulation(**kwargs):
    # Parameters
    print_args_nicely(**kwargs)
    initial_investment = kwargs['initial_investment']
    mean_return = kwargs['mean_return']
    volatility = kwargs['volatility']
    years = kwargs['years']
    simulations = kwargs['simulations']
    plt_show = kwargs['plt_show']
    
    # Monte Carlo Simulation
    portfolio_values = np.zeros((simulations, years + 1))
    portfolio_values[:, 0] = initial_investment

    for i in range(simulations):
        for year in range(1, years + 1):
            random_return = np.random.normal(mean_return, volatility)
            portfolio_values[i, year] = portfolio_values[i, year - 1] * (1 + random_return)

    # Plotting
    if plt_show:
        plt.figure(figsize=(10, 6))
        for i in range(simulations):
            plt.plot(portfolio_values[i], alpha=0.1, color='blue')
        plt.title('Monte Carlo Simulation of Portfolio Value')
        plt.xlabel('Years')
        plt.ylabel('Portfolio Value (£)')
        plt.show()

    # Summary Statistics
    final_values = portfolio_values[:, -1]
    mean_final_value = np.mean(final_values)
    std_final_value = np.std(final_values)

    print(f"Mean final portfolio value: £{mean_final_value:.2f}")
    print(f"Standard deviation of final portfolio value: £{std_final_value:.2f}")

# -- Both args and kwargs --
def print_args_nicely(*args, **kwargs):    
    for arg in args:
        print(f"P:{arg}")
    for kwarg, value in kwargs.items():
        print(f"D:{kwarg}: {value}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
    description="A small python program to run Monte Carlo simulation on a portfolio e.g. python .\mc_portfolio_simulator.py")
    parser.add_argument(
        "-p", "--portfolio_value",
        type=int,
        default="500000",
        help="Initial portfolio value")
    parser.add_argument(
        '-m', '--mean_return',
        choices=['0.06', '0.07', '0.08', '0.09'],
        type=float,
        default='0.07',
        help='Average annual return')
    parser.add_argument(
        "-v", "--volatility",
        type=float,
        choices=["0.15", "0.16"],
        default="0.15",
        help='Annual volatility')
    parser.add_argument(
        '-y', '--years',
        type=int,  
        help='Simulation period',
        default=30)
    parser.add_argument(
        '-s', '--simulations',
        type=int,
        help='Number of Monte Carlo simulations',
        default=1000)
    parser.add_argument(
        '-d', '--display',
        action='store_true',
        help='Display the simulations',
        default=False)
    args = parser.parse_args()
   
    monte_carlo_simulation(initial_investment=args.portfolio_value, mean_return=args.mean_return, volatility=args.volatility, years=args.years, simulations=args.simulations, plt_show=args.display)   

if __name__ == "__main__":
    main()