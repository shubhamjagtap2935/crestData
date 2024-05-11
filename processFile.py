import os
import pandas as pd


def process_files(input_folder, output_folder):
    # Check if input folder exists
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder '{input_folder}' not found.")

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List to store all dataframes
    dfs = []

    # Iterate through files in input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.dat'):
            file_path = os.path.join(input_folder, file_name)
            df = pd.read_csv(file_path, sep='\t')
            dfs.append(df)
        else:
            raise FileNotFoundError(
                f"File with .dat not found.")

    # Concatenate all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)

    # Calculate gross salary and add a new column for it
    combined_df['Gross Salary'] = combined_df['basic_salary'] + combined_df['allowances']

    # Remove duplicate based on ID
    combined_df.drop_duplicates(subset='id', keep='first', inplace=True)

    # Write processed data to CSV file
    output_file_path = os.path.join(output_folder, 'output2.csv')
    combined_df.to_csv(output_file_path, index=False)

    # Calculate and append footer
    second_highest_salary = combined_df['Gross Salary'].nlargest(2).iloc[-1] if len(
        combined_df) >= 2 else 0
    average_salary = combined_df['Gross Salary'].mean() if len(combined_df) > 0 else 0
    with open(output_file_path, 'a') as file:
        file.write(
            f"SecondHighestSalary={second_highest_salary},average salary={round(average_salary, 1)}")
    print(f"Output file generated at {output_file_path}")

# Execute in try expect block
try:
    dirPathInput = input("Enter input dir path: ")
    dirPathOutput = input("Enter output dir path: ")
    process_files(dirPathInput, dirPathOutput)
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print("An error occurred:", e)
