
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Description:
#   A small python program to run Monte Carlo simulation on a portfolio
#
# When -s option is used or "Show plot" in the GUI is selected the
# program will also calculate and display
# - Plot 95% confidence interval within two red lines
# - Plot median as a green line
# "Use log scale" option and "Show plot" option in the GUI are useful
# to show if the can run out in year using the 95% confidence interval
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
# Copyright (c) 2025 pc-scylla and letsrock
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
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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

# -- Both args and kwargs --
def print_args_nicely(*args, **kwargs):
    for arg in args:
        print(f"P:{arg}")
    for kwarg, value in kwargs.items():
        print(f"D:{kwarg}: {value}")

class SimulationApp:
    def __init__(self, **kwargs):
        print("Parameters:")
        print_args_nicely(**kwargs)
        self.initial_investment = kwargs['initial_investment']
        self.mean_return = kwargs['mean_return']
        self.volatility = kwargs['volatility']
        self.years = kwargs['years']
        self.simulations = kwargs['simulations']
        self.plt_show = kwargs['plt_show']
        self.log_show = kwargs['log_show']
        self.withdrawal_rate = kwargs['withdrawal_rate']
        self.inflation_rate = kwargs['inflation_rate']
        self.dynamic_withdraw = kwargs['dynamic_withdraw']

        self.root = tk.Tk()
        self.root.title("Monte Carlo Simulation of Portfolio")

        rowi=0
        # Labels and entries
        tk.Label(self.root, text="Initial Investment:").grid(row=0, column=0, sticky="e")
        self.entry_initial_investment = tk.Entry(self.root)
        self.entry_initial_investment.insert(0, str(self.initial_investment))
        self.entry_initial_investment.grid(row=rowi, column=1)

        rowi+=1
        tk.Label(self.root, text="Mean Return (e.g. 0.07 for 7%):").grid(row=1, column=0, sticky="e")
        self.entry_mean_return = tk.Entry(self.root)
        self.entry_mean_return.insert(0, str(self.mean_return))
        self.entry_mean_return.grid(row=rowi, column=1)

        rowi+=1
        tk.Label(self.root, text="Volatility (e.g. 0.15 for 15%):").grid(row=2, column=0, sticky="e")
        self.entry_volatility = tk.Entry(self.root)
        self.entry_volatility.insert(0, str(self.volatility))
        self.entry_volatility.grid(row=rowi, column=1)

        rowi+=1
        tk.Label(self.root, text="Years:").grid(row=3, column=0, sticky="e")
        self.entry_years = tk.Entry(self.root)
        self.entry_years.insert(0, str(self.years))
        self.entry_years.grid(row=rowi, column=1)

        rowi+=1
        tk.Label(self.root, text="Simulations:").grid(row=4, column=0, sticky="e")
        self.entry_simulations = tk.Entry(self.root)
        self.entry_simulations.insert(0, str(self.simulations))
        self.entry_simulations.grid(row=rowi, column=1)

        rowi+=1
        tk.Label(self.root, text="Inflation Rate (e.g. 0.039 for 3.9%:").grid(row=5, column=0, sticky="e")
        self.entry_inflation_rate = tk.Entry(self.root)
        self.entry_inflation_rate.insert(0, str(self.inflation_rate))
        self.entry_inflation_rate.grid(row=rowi, column=1)

        rowi+=1
        tk.Label(self.root, text="Withdrawal Rate (e.g. 0.03 for 3%):").grid(row=6, column=0, sticky="e")
        self.entry_withdrawal_rate = tk.Entry(self.root)
        self.entry_withdrawal_rate.insert(0, str(self.withdrawal_rate))
        self.entry_withdrawal_rate.grid(row=rowi, column=1)

        # Checkbox for dynamic withdrawal %withdrawal_rate of portfolio
        rowi+=1
        self.dynamic_withdraw_tk = tk.BooleanVar(value=self.dynamic_withdraw)
        self.checkbox_dynamic_withdraw = tk.Checkbutton(self.root, text="Dynamic Withdrawal (Portfolio(Yn)*Withdrawal Rate)", variable=self.dynamic_withdraw_tk)
        self.checkbox_dynamic_withdraw.grid(row=rowi, column=0, columnspan=2)

        # Checkbox for Show plot
        rowi+=1
        self.plt_show_tk = tk.BooleanVar(value=self.plt_show)
        self.checkbox_show_plot = tk.Checkbutton(self.root, text="Show plot", variable=self.plt_show_tk)
        self.checkbox_show_plot.grid(row=rowi, column=0, columnspan=2)

        # Checkbox for Show plot
        rowi+=1
        self.log_show_tk = tk.BooleanVar(value=self.log_show)
        self.checkbox_log_plot = tk.Checkbutton(self.root, text="Use log scale", variable=self.log_show_tk, command=self.on_log_show_tick)
        self.checkbox_log_plot.grid(row=rowi, column=0, columnspan=2)

        # Add my own style for the submit button
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.map("CustomButton.TButton",
                foreground=[('pressed', 'red'), ('active', 'green')],
                # Note that background colour can't be changed in the default Windows theme. It works using "clam"
                background=[('pressed', '!disabled', 'pale green'), ('active', 'snow')],
                font=[("pressed", ("TkDefaultFont", 11)) ]
        )

        # Submit button with separate style
        rowi+=1
        submit_button = ttk.Button(self.root, text="Submit", style="CustomButton.TButton", command=self.on_submit)
        submit_button.grid(row=rowi, column=0, columnspan=2)

        # Add the "Result" label
        rowi+=1
        tk.Label(self.root, text="Results:").grid(row=rowi, column=0, sticky="nw")

        # Read-only text box for results
        rowi+=1
        self.result_box = tk.Text(self.root, height=11, width=60, state='disabled', wrap="word")
        self.result_box.grid(row=rowi, column=0, columnspan=2)
        self.root.bind("<Return>", self.on_submit)
        self.root.bind("<KP_Enter>", self.on_submit)

    def on_log_show_tick(self, *args):
        """when ticked the log scale is selected so lets plot"""
        if  self.log_show_tk.get():
            self.plt_show_tk.set(True)

    def on_submit(self, *args):
        try:
            self.initial_investment = float(self.entry_initial_investment.get())
            self.mean_return = float(self.entry_mean_return.get())
            self.volatility = float(self.entry_volatility.get())
            self.years = int(self.entry_years.get())
            self.simulations = int(self.entry_simulations.get())
            self.inflation_rate = float(self.entry_inflation_rate.get())
            self.withdrawal_rate = float(self.entry_withdrawal_rate.get())

            # Display the values for debugging (you can replace this with your actual processing logic)
            #messagebox.showinfo("Input Values", f"Initial Investment: {self.initial_investment}\n"
            #                                    f"Mean Return: {self.mean_return}\n"
            #                                    f"Volatility: {self.volatility}\n"
            #                                    f"Years: {self.years}\n"
            #                                    f"Simulations: {self.simulations}\n"
            #                                    f"Inflation Rate: {self.inflation_rate}\n"
            #                                    f"Withdrawal Rate: {self.withdrawal_rate}")
            self.monte_carlo_simulation()
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please make sure all inputs are valid.")

    def monte_carlo_simulation(self):
        # Monte Carlo Simulation
        portfolio_values = np.zeros((self.simulations, self.years + 1))  # Matrix to store portfolio values for all simulations
        portfolio_values[:, 0] = self.initial_investment  # Initialize portfolio values for year 0 as the initial investment
        depletion_count = 0  # Counter to track the number of simulations where the portfolio is depleted before self.years

        # Run simulations
        self.dynamic_withdraw = self.dynamic_withdraw_tk.get()
        for i in range(self.simulations):
            withdrawal = self.initial_investment * self.withdrawal_rate  # Constant annual withdrawal (£30,000 for the first year)
            for year in range(1, self.years + 1):
                # Simulate annual market returns using a normal distribution
                random_return = np.random.normal(self.mean_return, self.volatility)
                portfolio_values[i, year] = portfolio_values[i, year - 1] * (1 + random_return)

                # For a dynamic withdrawal takes % of the yearly portfolio
                if self.dynamic_withdraw:
                    withdrawal = portfolio_values[i, year] * self.withdrawal_rate
                    withdrawals_text = "Dynamic Withdrawals ((Yn)*Rate)"
                else:
                    withdrawal *=(1+self.inflation_rate)
                    withdrawals_text = "Constant Withdrawals ((Y1)*Rate)"
                # Subtract annual withdrawal from the portfolio
                portfolio_values[i, year] -= withdrawal

                # Check if the portfolio is depleted (value drops to £0 or below)
                if portfolio_values[i, year] < 0:
                    portfolio_values[i, year] = 0  # Set portfolio value to £0 (no negative values allowed)
                    depletion_count += 1  # Increment the depletion counter
                    break  # End simulation for this portfolio once it's depleted

        # Calculate the probability of portfolio depletion before self.yearss
        depletion_probability = (depletion_count / self.simulations) * 100  # Percentage of simulations with depletion

        # Adjust inflation impact
        inflation_factor = (1 + self.inflation_rate) ** self.years  # Factor to account for self.years of inflation
        inflation_adjusted_mean_final_value = np.mean(portfolio_values[:, -1]) / inflation_factor  # Adjusted portfolio mean

        # Plot portfolio values for all simulations
        self.plt_show = self.plt_show_tk.get()
        self.log_scale = self.log_show_tk.get()
        if self.plt_show:
            plt.figure(figsize=(10, 6))  # Set figure size for the plot
            for i in range(self.simulations):
                plt.plot(portfolio_values[i], alpha=0.1, color='blue')  # Plot portfolio values for each simulation

            # Calculate 95% confidence interval
            portfolio_values_array = np.array(portfolio_values)  # Convert to NumPy array for easier computation
            lower_bound = np.percentile(portfolio_values_array, 2.5, axis=0)  # 2.5th percentile (lower bound)
            upper_bound = np.percentile(portfolio_values_array, 97.5, axis=0)  # 97.5th percentile (upper bound)

            # Calculate median
            median_values = np.median(portfolio_values_array, axis=0)  # Median values across simulations

            # Plot 95% confidence interval as a thick red line
            plt.plot(lower_bound, color='red', linewidth=2, label='95% Confidence Interval (Lower)')
            plt.plot(upper_bound, color='red', linewidth=2, label='95% Confidence Interval (Upper)')

            # Plot median as a green line
            plt.plot(median_values, color='green', linewidth=2, label='Median')

            # Apply logarithmic scaling if enabled
            if self.log_scale:
                plt.yscale('log')  # Set y-axis to logarithmic scale

            plt.title(f'Monte Carlo Simulation of Portfolio Value with {withdrawals_text}')
            plt.xlabel('Years')  # Label for the x-axis (years of simulation)
            plt.ylabel('Portfolio Value (£)')  # Label for the y-axis (portfolio value in £)
            plt.legend()  # Add a legend to the plot
            plt.show()  # Display the plot

        # Summary Statistics
        final_values = portfolio_values[:, -1]  # Extract final portfolio values after 40 years
        mean_final_value = np.mean(final_values)  # Calculate the mean final portfolio value
        std_final_value = np.std(final_values)  # Calculate the standard deviation of final portfolio values
        inflation_adjusted_std_final_val = std_final_value / inflation_factor
        inflation_adjusted_final_withdraw = inflation_adjusted_mean_final_value*self.withdrawal_rate
        if self.dynamic_withdraw:
            inflation_adjusted_final_withdraw = inflation_adjusted_mean_final_value * self.withdrawal_rate
        else:
            inflation_adjusted_final_withdraw = self.initial_investment * self.withdrawal_rate
            if inflation_adjusted_mean_final_value < inflation_adjusted_final_withdraw:
                inflation_adjusted_final_withdraw = inflation_adjusted_final_withdraw

        # Prepare result text
        initial_yearly_withdrawal  = self.withdrawal_rate * self.initial_investment
        result_text = (f"        Portfolio initial value: £{self.initial_investment}\n"
                       f"Withdrawal amount at first year: £{initial_yearly_withdrawal:.0f}\n"
                       f"Without inflation -------------\n"
                       f"     Mean final portfolio value: £{mean_final_value:.2f}\n"
                       f"  Std Dev final portfolio value: £{std_final_value:.2f}\n"
                       f"Inflation adjusted ------------\n"
                       f"     Mean final portfolio value: £{inflation_adjusted_mean_final_value:.2f}\n"
                       f"  Std Dev final portfolio value: £{inflation_adjusted_std_final_val:.2f}\n"
                       f"Withdrawal amount at final year: £{inflation_adjusted_final_withdraw:.0f}\n"
                       f"Probability of depletion ------\n"
                       f" Probability of portfolio depletion before {self.years} years: {depletion_probability:.2f}%")

        # Display results in read-only text box
        self.result_box.config(state='normal')
        self.result_box.delete('1.0', tk.END)
        self.result_box.insert(tk.END, result_text)
        self.result_box.config(state='disabled')
        if inflation_adjusted_mean_final_value>=self.initial_investment:
            self.result_box.config(background="palegreen")
        else:
            self.result_box.config(background="peachpuff")

        # Print results on the console
        print(f"")
        print(f"Initial conditions")
        print(f"==================")
        print(f"        Portfolio initial value: £{self.initial_investment}")
        print(f"                 Inflation rate: {self.inflation_rate*100:.2f}%")
        print(f"      Expected portfolio return: {self.mean_return*100:.2f}%")
        print(f"     Withdrawal amount per year: £{withdrawal:.2f}")
        print(f"         Annual Withdrawal rate: {self.withdrawal_rate}")
        print(f"   Simulation duration in years: {self.years}")
        print("")
        print("Results:")
        print("========")
        print(f"Withdrawal amount at first year: £{initial_yearly_withdrawal:.0f}")
        print(f"Without inflation")
        print(f"     Mean final portfolio value: £{mean_final_value:.2f}")
        print(f"     Mean final portfolio value: £{mean_final_value:.2f}")
        print(f"  Std Dev final portfolio value: £{std_final_value:.2f}")
        print(f"Inflation adjusted")
        print(f"     Mean final portfolio value: £{inflation_adjusted_mean_final_value:.2f}")
        print(f"  Std Dev final portfolio value: £{inflation_adjusted_std_final_val:.2f}")
        print(f"Withdrawal amount at final year: £{inflation_adjusted_final_withdraw:.0f}")
        print(f" Probability of portfolio depletion before {self.years} years: {depletion_probability:.2f}%")

    def run(self):
        self.root.mainloop()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
    description="A small python program to run Monte Carlo simulation on a portfolio e.g. python .\mc_portfolio_simulator.py")

    parser.add_argument(
        "-p", "--portfolio_value",
        type=int,
        default="500000",
        help="Starting amount in the portfolio e.g. 500000 for £500,000")
    parser.add_argument(
        '-m', '--mean_return',
        choices=['0.06', '0.07', '0.08', '0.09'],
        type=float,
        default='0.07',
        help='Average annual return expected from the portfolio e.g. 0.07 for 7 percent')
    parser.add_argument(
         "-v", "--volatility",
        type=float,
        choices=["0.15", "0.16"],
        default="0.15",
        help="Variation in annual returns due to market conditions e.g. 0.015 for 15 percent volatility")
    parser.add_argument(
        '-y', '--years',
        type=int,
        help="Duration of the simulation in years (e.g. 30 for 30 years)",
        default=30)
    parser.add_argument(
        '-n', '--nb_simulations',
        type=int,
        help="Total number of simulations to model potential outcomes (e.g. 1000 for a 1000 simulations)",
        default=3000)
    parser.add_argument(
        '-s', '--show',
        action='store_true',
        help="Display the simulations",
        default=False)
    parser.add_argument(
        "-i", "--inflation_rate",
        type=float,
        default="0.039",
        help="Average history inflation (e.g. 0.039 for 3.9 percent in UK over 20 years)")
    parser.add_argument(
        "-d", '--dynamic_withdraw',
        action='store_true',
        help="Dynamic withdrawal: withdraw a percent of yearly portfolio",
        default=False)
    parser.add_argument(
        "-l", '--log_scale',
        action='store_true',
        help="Display with logarithmic scale",
        default=False)
    parser.add_argument(
        "-w", "--withdrawal_rate",
        type=float,
        default="0.03",
        help="Constant withdrawal rate (e.g. 0.03 for 3 percent of initial investment per year)")

    args = parser.parse_args()

    app = SimulationApp(initial_investment=args.portfolio_value,
                           mean_return=args.mean_return,
                           volatility=args.volatility,
                           years=args.years,
                           simulations=args.nb_simulations,
                           plt_show=args.show,
                           log_show=args.log_scale,
                           inflation_rate=args.inflation_rate,
                           withdrawal_rate=args.withdrawal_rate,
                           dynamic_withdraw=args.dynamic_withdraw)
    app.run()

    # If everything runs successfully
    sys.exit(EXIT_SUCCESS)

if __name__ == "__main__":
    main()