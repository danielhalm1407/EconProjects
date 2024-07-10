import sys
import os
import pandas as pd
import numpy as np
from scipy.optimize import root
import matplotlib.pyplot as plt
import traceback

__file__ = "nb04.py"

# Debug function to print the call stack
def print_call_stack():
    stack = traceback.format_stack()
    print("Call stack:")
    for line in stack[:-1]:  # exclude the call to this function
        print(line.strip())

def get_user_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print(f"Invalid input: {user_input}. Please enter 'Y' or 'N'.")

def get_custom_values():
    R = float(input("Enter custom value for R: "))
    maturity_g = float(input("Enter custom value for maturity_g: "))
    time_frame = int(input("Enter custom value for time_frame: "))
    return R, maturity_g, time_frame

def main():
    # Get the absolute path of the current script
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current_dir = os.getcwd()  # __file__ is not defined in interactive mode

    # Print the current directory
    print(f'Current Directory: {current_dir}')

    # Insert the parent directory into sys.path
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
        print(f'Inserting Parent Path: {parent_dir}')

    # Print the updated sys.path
    print(f'Priority System Path: {sys.path[0]}')

    # Try to import the custom module
    try:
        import econ_utils
        from econ_utils import inv_theory as inv
        print('Successfully imported inv_theory as inv from econ_utils')
    except ImportError as e:
        print(f'Error importing econ_utils: {e}')
        sys.exit(1)

    # Prompt user for default or custom values
    use_default = get_user_input("Keep default values? [Y/N]: ")
    if use_default == 'n':
        print("You will need to enter custom values")
        R, maturity_g, time_frame = get_custom_values()
    else:
        # Default values
        R = 0.055
        maturity_g = 0.073
        time_frame = 10

    # The MAIN SCRIPT
    asset_df = pd.read_excel(os.path.join(sys.path[0],"../data/Bloomberg_Rankings.xlsx"), sheet_name="Mid Cap and Above")
    asset_df = asset_df.dropna(subset=['5 YR Forecast EPS Growth'])

    # Apply predict_multiple function using user-defined or default values
    asset_df["5Y Multiple"] = asset_df["5 YR Forecast EPS Growth"].apply(lambda x: inv.predict_multiple(x, 5, R=R, maturity_g=maturity_g, time_frame=time_frame))

    # Apply predict_roi function using user-defined or default values
    asset_df["5Y Expected Annualised TR (Change in Multiple)"] = [inv.predict_roi(asset_df["5 YR Forecast EPS Growth"][i], asset_df["Multiple"][i], asset_df["5Y Multiple"][i]) for i in asset_df.index]

    # Save results to Excel
    asset_df.to_excel(os.path.join(sys.path[0],"../data/Top_Stocks.xlsx"))

    print("Total Returns Spat out to Top_Stocks Accordingly")

print("Script is being executed")
print_call_stack()

if __name__ == "__main__":
    print("Script is being run directly")
    main()
else:
    print("Script is being imported")
