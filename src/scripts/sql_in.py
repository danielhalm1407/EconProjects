import sys
import os
import logging
import pandas as pd

def get_user_input(prompt):
    return input(prompt).strip().lower().replace(' ','_')
        
#__file__ = "sql_in.py"
def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(filename)s] %(message)s', level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current_dir = os.getcwd()  # __file__ is not defined in interactive mode

        # Print the current directory
        print(f'Current Directory: {current_dir}')

    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
        print(f'Inserting Parent Path: {parent_dir}')

    # Print the updated sys.path
        print(f'Priority System Path: {sys.path[0]}')
    try:
        import econ_utils
        from econ_utils import sql_queries as sqlq
        print('Successfully imported sql_queries as sqlq from econ_utils')
    except ImportError as e:
        print(f'Error importing econ_utils: {e}')
        sys.exit(1)

    # THE MAIN SCRIPT
    logging.info('Retrieving the bloomberg dataframe')
    bloomberg_data = pd.read_excel(os.path.join(sys.path[0],"../data/Bloomberg_Rankings.xlsx"), sheet_name="Mid Cap and Above")
    logging.info('bloomberg dataframe retreived')

    logging.info('Retrieving the Database/Creating if not Existing Already')
    engine = sqlq.get_sql_engine()
    logging.info('Retrieved the Database')

    name = get_user_input("What do you want to call the table?")
    print(f'Your data will be saved to the table name: {name}')
    sqlq.make_table(df = bloomberg_data, engine = engine)
    logging.info('Saved a table to database')

if __name__ == "__main__":
    print("Script is being run directly")
    main()
else:
    print("Script is being imported")