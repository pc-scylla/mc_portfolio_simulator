# Monte Carlo Portfolio Simulator

This Python program allows you to perform Monte Carlo simulations on a portfolio, providing insights into potential outcomes based on user-defined parameters.

---

## Description

The Monte Carlo Portfolio Simulator enables users to analyze portfolio performance over time, taking into account factors such as:
- Portfolio value
- Annual returns
- Volatility
- Inflation rates
- Withdrawal rates

Customize the simulation with flexible options to suit your needs.

---

## How to Run

You can run the simulation in various shell environments. Here are the commands:

### How to run in various shell
- **PowerShell**:
Using PowerShell

python .\mc_portfolio_simulator.py

- **Dos**:
Using DOS shell

python mc_portfolio_simulator.py

- **Bash or Mac Terminal**:
Using bash or mac

python mc_portfolio_simulator.py 

### Script Arguments

Customize the simulation using these arguments:

| Argument            | Description                                                                            | Type      | Choices                        | Default Value |
|---------------------|----------------------------------------------------------------------------------------|-----------|--------------------------------|---------------|
| `-p`, `--portfolio_value` | Starting amount in the portfolio (e.g. `500000` for £500,000).                   | `int`     | N/A                            | `500000`      |
| `-m`, `--mean_return`     | Average annual return expected (choose from `0.06`, `0.07`, `0.08`, `0.09`).     | `float`   | `0.06`, `0.07`, `0.08`, `0.09` | `0.07`        |
| `-v`, `--volatility`      | Variation in annual returns due to market conditions (`0.15` or `0.16`).         | `float`   | `0.15`, `0.16`                 | `0.15`        |
| `-y`, `--years`           | Duration of the simulation in years (e.g. `30` for 30 years).                    | `int`     | N/A                            | `30`          |
| `-n`, `--nb_simulations`  | Total number of simulations to model potential outcomes (e.g. `1000`).           | `int`     | N/A                            | `3000`        |
| `-s`, `--show`            | Display the simulations.                                                         | `bool`    | N/A                            | `False`       |
| `-i`, `--inflation_rate`  | Historical average inflation rate (e.g. `0.039` for 3.9%).                      | `float`   | N/A                            | `0.039`       |
| `-d`, `--dynamic_withdraw`| Dynamic withdrawal: withdraw a percent of yearly portfolio.                      | `bool`    | N/A                            | `False`       |
| `-w`, `--withdrawal_rate` | Constant withdrawal rate (e.g. `0.03` for 3%).                                   | `float`   | N/A                            | `0.03`        |

---

*This README.md was generated with assistance from [Microsoft Copilot](https://www.microsoft.com/en-us/edge/microsoft-copilot).*  

