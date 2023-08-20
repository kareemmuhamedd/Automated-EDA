import os
import pandas as pd
import seaborn 
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import random


######### this function to read data using path of data in your computer ##########
def loadDataFromPC(path):
    try:
        _, file_extension = os.path.splitext(path)
        
        if file_extension == ".csv":
            data = pd.read_csv(path)
        elif file_extension == ".xls":
            data = pd.read_excel(path)
        elif file_extension == ".xlsx":
            data = pd.read_excel(path)
        else:
            raise ValueError("Unsupported file format. Only CSV, XLSX, and XLS are supported.")

        return data
    
    except Exception as e:
        print("An error occurred while loading the data:", str(e))
        return None



######### this function to handeling data and make it able to be readable ##########
def handeling_data(data):
    categoricalColumns = data.select_dtypes(include="object").columns
    numericalColumns = data.select_dtypes(include=["int", "float"]).columns
    data[numericalColumns] = data[numericalColumns].fillna(data[numericalColumns].mean())
    data[categoricalColumns] = data[categoricalColumns].fillna(data[categoricalColumns].mode().iloc[0])
    encoded_data = pd.get_dummies(data, columns=categoricalColumns, drop_first=True)
    scaler = StandardScaler()
    scaledNumerical = scaler.fit_transform(data[numericalColumns])
    encoded_data[numericalColumns] = scaledNumerical
    encoded_data.columns = encoded_data.columns.str.replace("_", "")

    return encoded_data


######### this function to display Histogram  ##########
def displayHistogram(data, colTitleName):
    plt.figure(figsize=(12, 8))

    if colTitleName in data.columns:
        column_data = data[colTitleName]

        if column_data.dtype == "object":
           ## like 'str' data
            value_counts = column_data.value_counts()

            seaborn.barplot(x=value_counts.index, y=value_counts.values)
            plt.xlabel(colTitleName)

            for i, count in enumerate(value_counts.values):
                plt.text(i, count, str(count), ha="center", va="bottom")
            plt.show()
        else:
            seaborn.histplot(
                column_data, kde=True, color=random.choice(list(seaborn.color_palette()))
            )
            plt.xlabel(colTitleName)
            plt.show()
    else:
        print(f"Column '{colTitleName}' does not exist in the data.")
 

######### this function to display Boxplot  ##########
def displayBoxplot(data, posOfxColumn, posOfyColunm):
    name = "myBoxplot"

    if data[posOfxColumn].dtype == "object":
        unique_x = data[posOfxColumn].unique()
        seaborn.boxplot(data=data, x=posOfxColumn, y=posOfyColunm)
        plt.title(f"comparing {posOfxColumn} vs {posOfyColunm} {name}")
        plt.xlabel(posOfxColumn)
        plt.ylabel(posOfyColunm)

    elif data[posOfyColunm].dtype == "object":
        unique_x = data[posOfxColumn].unique()
        colors = random.choices(list(seaborn.color_palette()), k=len(unique_x))
        seaborn.scatterplot(data=data, x=posOfxColumn, y=posOfyColunm, hue=posOfxColumn,palette=colors)
        plt.title(f"comparing {posOfxColumn} vs {posOfyColunm} {name}")
        plt.xlabel(posOfxColumn)
        plt.ylabel(posOfyColunm)

    else:
        seaborn.boxplot(data=data, x=posOfxColumn, y=posOfyColunm)
        plt.title(f"{posOfxColumn} vs {posOfyColunm} {name}")
        plt.xlabel(posOfxColumn)
        plt.ylabel(posOfyColunm)

    plt.tight_layout()
    plt.show()

######### this function to display Scatterplot  ##########        
def displayingScatterplot(data, posOfxColumn, posOfyColunm):
    name = "myScatterplot"


    if data[posOfxColumn].dtype == "object" and data[posOfyColunm].dtype == "object":
        unique_x = data[posOfxColumn].unique()
        colors = random.choices(list(seaborn.color_palette()), k=len(unique_x))
        seaborn.scatterplot(data=data, x=posOfxColumn, y=posOfyColunm, hue=posOfxColumn,palette=colors)

    elif data[posOfxColumn].dtype == "object":
        unique_x = data[posOfxColumn].unique()
        colors = random.choices(list(seaborn.color_palette()), k=len(unique_x))
        seaborn.stripplot(data=data, x=posOfxColumn, y=posOfyColunm, hue=posOfxColumn,palette=colors)

    elif data[posOfyColunm].dtype == "object":
        unique_y = data[posOfyColunm].unique()
        seaborn.stripplot(data=data, x=posOfxColumn, y=posOfyColunm, hue=posOfyColunm,palette=colors)
        colors = random.choices(list(seaborn.color_palette()), k=len(unique_y))
        

    else:
        seaborn.scatterplot(data=data, x=posOfxColumn, y=posOfyColunm)
    plt.title(f"comparing {posOfxColumn} vs {posOfyColunm} {name}")
    plt.xlabel(posOfxColumn)
    plt.ylabel(posOfyColunm)
    plt.tight_layout()
    plt.show()

######### this function to display Piechart  ##########
def displayingPiechart(data, column):
    name = "Piechart"
    value_counts = data[column].value_counts()
    labels = value_counts.index
    counts = value_counts.values

    plt.figure(figsize=(10, 6))
    plt.pie(counts, labels=labels,colors=seaborn.color_palette('Set3'))
    plt.title(f"{column} {name}")
    plt.axis('equal')
    plt.show()

######### this function to display PlotingData  ##########
def displayPlotingData(data, h1, h2, h3):
    try:
        if h1 not in data.columns or h2 not in data.columns or h3 not in data.columns:
            raise ValueError("One or more of the specified headers are not present in the data.")

        if data[h1].dtype != 'object' or data[h2].dtype != 'object' or data[h3].dtype != 'object':
            raise ValueError("All three headers must contain categorical data.")

        value_counts_h1 = data[h1].value_counts()
        value_counts_h2 = data[h2].value_counts()
        value_counts_h3 = data[h3].value_counts()

        plt.figure(figsize=(10, 6))

        seaborn.lineplot(data=value_counts_h1, x=value_counts_h1.index, y=value_counts_h1.values, label=h1)
        seaborn.lineplot(data=value_counts_h2, x=value_counts_h2.index, y=value_counts_h2.values, label=h2)
        seaborn.lineplot(data=value_counts_h3, x=value_counts_h3.index, y=value_counts_h3.values, label=h3)

        plt.legend()
        plt.xlabel("Unique Values")
        plt.ylabel("Counts")
        plt.title(f'Value Counts of {h1}, {h2}, and {h3}')
        plt.show()

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    try:
        file_path = input("Give me your path to display your data: ")
        data = loadDataFromPC(file_path)
        dataAfterProcessing = handeling_data(data)
        while True:
            print("Press 1. To display Histogram")
            print("Press 2. To display Box Plot")
            print("Press 3. To display Scatter Plot")
            print("Press 4. To display Pie Chart")
            print("Press 5. To displayPlotingData") 
            print("Press 6. To Leave")
            
            userChoice = int(input("Enter your choice (1/2/3/4/5/6): "))


            if userChoice == 1:
                data = loadDataFromPC(file_path)
                dataAfterProcessing = handeling_data(data)
                try:
                    displayChoice = int(input("\n[1] Display by header\n[2] Display by row\nYour choice is: "))
                    if displayChoice == 2:
                        data = dataAfterProcessing
                    elif displayChoice != 1:
                        raise ValueError
                except ValueError:
                    print("Invalid input. Try again.")
                    userChoice = int(input("Enter [0] to exit or press [1] to try again: "))
                    if userChoice == 0:
                        exit()
                print("\nAvailable Columns:")
                for i, column in enumerate(data.columns):
                    print(f"{i}. {column}")

                column_choice = int(input("Enter the number of column you want: "))
                if 0 <= column_choice < len(data.columns):
                    column = data.columns[column_choice]
                    print('\n\nplease waiting .......\n\n')
                    displayHistogram(data, column)
                else:
                    print("Invalid choice. Please try again.\n")

            elif userChoice == 2:
                data = loadDataFromPC(file_path)
                dataAfterProcessing = handeling_data(data)

                try:
                        displayChoice = int(input("\n[1] Display by header\n[2] Display by row\nYour choice is: "))
                        if displayChoice == 2:
                            data = dataAfterProcessing
                        elif displayChoice != 1:
                            raise ValueError
                except ValueError:
                        print("Invalid input. Try again.")
                        userChoice = int(input("Enter [0] to exit or press [1] to try again: "))
                        if userChoice == 0:
                            exit()
                print("\nAvailable Columns:")
                for i, column in enumerate(data.columns):
                        print(f"{i}. {column}")

                x_column_choice = int(input("Give me the number of X-axis column: "))
                y_column_choice = int(input("Give me the number of Y-axis column: "))

                if 0 <= x_column_choice < len(data.columns) and 0 <= y_column_choice < len(data.columns):
                        posOfxColumn = data.columns[x_column_choice]
                        posOfyColunm = data.columns[y_column_choice]
                        print('\n\nplease waiting .......\n\n')
                        displayBoxplot(data, posOfxColumn, posOfyColunm)
                else:
                        print("Invalid choice. Please try again.")

            elif userChoice == 3:
                data = loadDataFromPC(file_path)
                dataAfterProcessing = handeling_data(data)
                try:
                    displayChoice = int(input("\n[1] Display by header\n[2] Display by row\nYour choice is: "))
                    if displayChoice == 2:
                        data = dataAfterProcessing
                    elif displayChoice != 1:
                        raise ValueError
                except ValueError:
                    print("Invalid input. Try again.")
                print("\nAvailable Columns:")
                for i, column in enumerate(data.columns):
                    print(f"{i}. {column}")

                x_column_choice = int(input("Give me the number of X-axis column: "))
                y_column_choice = int(input("Give me the number of Y-axis column: "))
                if 0 <= x_column_choice < len(data.columns) and 0 <= y_column_choice < len(data.columns):
                    posOfxColumn = data.columns[x_column_choice]
                    posOfyColunm = data.columns[y_column_choice]
                    print('\n\nplease waiting .......\n\n')
                    displayingScatterplot(data, posOfxColumn, posOfyColunm)
                else:
                    print("Invalid choice. Please try again.")

            elif userChoice == 4:
                data = loadDataFromPC(file_path)
                dataAfterProcessing = handeling_data(data)
                try:
                    displayChoice = int(input("\n[1] Display by header\n[2] Display by row\nYour choice is: "))
                    if displayChoice == 2:
                        data = dataAfterProcessing
                    elif displayChoice != 1:
                        raise ValueError
                except ValueError:
                    print("Invalid input. Try again.")
                    userChoice = int(input("Enter [0] to exit or press [1] to try again: "))
                    if userChoice == 0:
                        exit()
                print("\nAvailable Columns:")
                for i, column in enumerate(data.columns):
                    print(f"{i}. {column}")

                column_choice = int(input("Enter the number of column you want: "))
                if 0 <= column_choice < len(data.columns):
                    column = data.columns[column_choice]
                    print('\n\nplease waiting .......\n\n')
                    displayingPiechart(data, column)
                else:
                    print("Invalid choice. Please try again.")

            elif userChoice == 5:
                 data = loadDataFromPC(file_path)
                 dataAfterProcessing = handeling_data(data)
                 header_names = data.columns.tolist()
                 print("Available Headers:")
                 for i, header in enumerate(header_names):
                    print(f"{i}. {header}")

                 hed1 = int(input("Give me the number of header1 column: "))
                 hed2 = int(input("Give me the number of header2 column: "))
                 hed3 = int(input("Give me the number of header3 column: "))
                 if 0 <= hed1 < len(data.columns) and 0 <= hed2 < len(data.columns) and 0 <= hed3 < len(data.columns):
                    headerOneData = data.columns[hed1]
                    headerTwoData = data.columns[hed2]
                    headerThreeData = data.columns[hed3]
                    print('\n\nplease waiting .......\n\n')
                    displayPlotingData(dataAfterProcessing, headerOneData, headerTwoData,headerThreeData)
            elif userChoice == 6:
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
