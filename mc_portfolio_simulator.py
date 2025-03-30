
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
    print("Parameters:")
    print_args_nicely(**kwargs)
    initial_investment = kwargs['initial_investment']
    mean_return = kwargs['mean_return']
    volatility = kwargs['volatility']
    years = kwargs['years']
    simulations = kwargs['simulations']
    plt_show = kwargs['plt_show']
    withdrawal_rate = kwargs['withdrawal_rate']
    inflation_rate = kwargs['inflation_rate']


    # Monte Carlo Simulation
    portfolio_values = np.zeros((simulations, years + 1))  # Matrix to store portfolio values for all simulations
    portfolio_values[:, 0] = initial_investment  # Initialize portfolio values for year 0 as the initial investment
    depletion_count = 0  # Counter to track the number of simulations where the portfolio is depleted before 40 years

    # Run simulations
    for i in range(simulations):
        withdrawal = initial_investment * withdrawal_rate  # Constant annual withdrawal (£30,000 for the first year)
        for year in range(1, years + 1):
            # Simulate annual market returns using a normal distribution
            random_return = np.random.normal(mean_return, volatility)
            portfolio_values[i, year] = portfolio_values[i, year - 1] * (1 + random_return)

            # Subtract annual withdrawal from the portfolio
            portfolio_values[i, year] -= withdrawal

            # Check if the portfolio is depleted (value drops to £0 or below)
            if portfolio_values[i, year] < 0:
                portfolio_values[i, year] = 0  # Set portfolio value to £0 (no negative values allowed)
                depletion_count += 1  # Increment the depletion counter
                break  # End simulation for this portfolio once it's depleted

    # Calculate the probability of portfolio depletion before 40 years
    depletion_probability = (depletion_count / simulations) * 100  # Percentage of simulations with depletion

    # Adjust inflation impact
    inflation_factor = (1 + inflation_rate) ** years  # Factor to account for 40 years of inflation
    inflation_adjusted_mean_final_value = np.mean(portfolio_values[:, -1]) / inflation_factor  # Adjusted portfolio mean

    # Plot portfolio values for all simulations
    if plt_show:
        plt.figure(figsize=(10, 6))  # Set figure size for the plot
        for i in range(simulations):
            plt.plot(portfolio_values[i], alpha=0.1, color='blue')  # Plot portfolio values for each simulation
        plt.title('Monte Carlo Simulation of Portfolio Value with Constant Withdrawals')
        plt.xlabel('Years')  # Label for the x-axis (years of simulation)
        plt.ylabel('Portfolio Value (£)')  # Label for the y-axis (portfolio value in £)
        plt.show()  # Display the plot

    # Summary Statistics
    final_values = portfolio_values[:, -1]  # Extract final portfolio values after 40 years
    mean_final_value = np.mean(final_values)  # Calculate the mean final portfolio value
    std_final_value = np.std(final_values)  # Calculate the standard deviation of final portfolio values
    inflation_adjusted_std_final_val = std_final_value / inflation_factor
    # Print results
    print(f"\nInitial conditions")
    print(f"==================")
    print(f"     Portfolio initial value: £{initial_investment}")
    print(f"              Inflation rate: {inflation_rate*100:.2f}%")
    print(f"   Expected portfolio return: {mean_return*100:.2f}%")
    print(f"  Withdrawal amount per year: £{withdrawal}")
    print(f"      Annual Withdrawal rate: {withdrawal_rate}")
    print(f"Simulation duration in years: {years}")
    print("")
    print("Results:")
    print("========")
    print(f"Without inflation- Mean final portfolio value: £{mean_final_value:.2f}")
    print(f"Without inflation  - SD final portfolio value: £{std_final_value:.2f}")
    print(f"Inflation-adjusted mean final portfolio value: £{inflation_adjusted_mean_final_value:.2f}")
    print(f"Inflation-adjusted - SD final portfolio value: £{inflation_adjusted_std_final_val:.2f}")
    print(f"Probability of portfolio depletion before {years} years: {depletion_probability:.2f}%")

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
        help="Starting amount in the portfolio (e.g. 500000 for £500,000)")
    parser.add_argument(
        '-m', '--mean_return',
        choices=['0.06', '0.07', '0.08', '0.09'],
        type=float,
        default='0.07',
        help='Average annual return expected from the portfolio (e.g. 0.07 for7%)')
    parser.add_argument(
        "-v", "--volatility",
        type=float,
        choices=["0.15", "0.16"],
        default="0.15",
        help='Variation in annual returns due to market conditions (e.g. 0.015 for 15% volatility)')
    parser.add_argument(
        '-y', '--years',
        type=int,
        help='Duration of the simulation in years (e.g. 30 for 30 years)',
        default=30)
    parser.add_argument(
        '-s', '--simulations',
        type=int,
        help='Total number of simulations to model potential outcomes (e.g. 1000 for a 1000 simulations)',
        default=3000)
    parser.add_argument(
        '-d', '--display',
        action='store_true',
        help='Display the simulations',
        default=False)
    parser.add_argument(
        "-i", "--inflation_rate",
        type=float,
        default="0.039",
        help=r'Average history inflation (e.g. 0.039 for 3.9% in UK over 20years)')
    parser.add_argument(
        "-w", "--withdrawal_rate",
        type=float,
        default="0.03",
        help=r'Constant withdrawal rate (e.g. 0.03 for 3% of initial investment per year')
    args = parser.parse_args()

    monte_carlo_simulation(initial_investment=args.portfolio_value,
                           mean_return=args.mean_return,
                           volatility=args.volatility,
                           years=args.years,
                           simulations=args.simulations,
                           plt_show=args.display,
                           inflation_rate=args.inflation_rate,
                           withdrawal_rate=args.withdrawal_rate)

if __name__ == "__main__":
    main()