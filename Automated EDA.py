import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import random

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




def handeling_data(data):
    categorical_columns = data.select_dtypes(include="object").columns
    numerical_columns = data.select_dtypes(include=["int", "float"]).columns
    data[numerical_columns] = data[numerical_columns].fillna(data[numerical_columns].mean())
    data[categorical_columns] = data[categorical_columns].fillna(data[categorical_columns].mode().iloc[0])


    encoded_data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)

    scaler = StandardScaler()
    scaled_numerical = scaler.fit_transform(data[numerical_columns])
    encoded_data[numerical_columns] = scaled_numerical

    encoded_data.columns = encoded_data.columns.str.replace("_", "")

    return encoded_data




def displayHistogram(data, colTitleName):
    plt.figure(figsize=(12, 8))

    if colTitleName in data.columns:
        column_data = data[colTitleName]

        if column_data.dtype == "object":
           ## like 'str' data
            value_counts = column_data.value_counts()

            sns.barplot(x=value_counts.index, y=value_counts.values)
            plt.xlabel(colTitleName)

            for i, count in enumerate(value_counts.values):
                plt.text(i, count, str(count), ha="center", va="bottom")

            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.show()
        else:
            sns.histplot(
                column_data, kde=True, color=random.choice(list(sns.color_palette()))
            )
            plt.xlabel(colTitleName)
            plt.tight_layout()
            plt.show()
    else:
        print(f"Column '{colTitleName}' does not exist in the data.")



def displayBoxplot(data, posOfxColumn, posOfyColunm):
    name = "myBoxplot"

    plt.figure(figsize=(8, 6))
    if data[posOfxColumn].dtype == "object":
        unique_x = data[posOfxColumn].unique()
        colors = random.choices(list(sns.color_palette()), k=len(unique_x))

        sns.boxplot(data=data, x=posOfxColumn, y=posOfyColunm, palette=colors)
        plt.title(f"comparing {posOfxColumn} vs {posOfyColunm} {name}")
        plt.xlabel(posOfxColumn)
        plt.ylabel(posOfyColunm)

    elif data[posOfyColunm].dtype == "object":
        unique_y = data[posOfyColunm].unique()
        colors = random.choices(list(sns.color_palette()), k=len(unique_y))

        sns.boxplot(data=data, x=posOfxColumn, y=posOfyColunm, palette=colors)
        plt.title(f"{posOfxColumn} vs {posOfyColunm} {name}")
        plt.xlabel(posOfxColumn)
        plt.ylabel(posOfyColunm)

    else:
        sns.boxplot(data=data, x=posOfxColumn, y=posOfyColunm)
        plt.title(f"{posOfxColumn} vs {posOfyColunm} {name}")
        plt.xlabel(posOfxColumn)
        plt.ylabel(posOfyColunm)

    plt.tight_layout()
    plt.show()

        
def displayingScatterplot(data, posOfxColumn, posOfyColunm):
    name = "myScatterplot"
    plt.figure(figsize=(8, 6))

    if data[posOfxColumn].dtype == "object" and data[posOfyColunm].dtype == "object":
        unique_x = data[posOfxColumn].unique()
        colors = random.choices(list(sns.color_palette()), k=len(unique_x))

        sns.scatterplot(data=data, x=posOfxColumn, y=posOfyColunm, hue=posOfxColumn, palette=colors)

    elif data[posOfxColumn].dtype == "object":
        unique_x = data[posOfxColumn].unique()
        colors = random.choices(list(sns.color_palette()), k=len(unique_x))

        sns.stripplot(data=data, x=posOfxColumn, y=posOfyColunm, hue=posOfxColumn, palette=colors)

    elif data[posOfyColunm].dtype == "object":
        unique_y = data[posOfyColunm].unique()
        colors = random.choices(list(sns.color_palette()), k=len(unique_y))

        sns.stripplot(data=data, x=posOfxColumn, y=posOfyColunm, hue=posOfyColunm, palette=colors)

    else:
        sns.scatterplot(data=data, x=posOfxColumn, y=posOfyColunm)

    plt.title(f"comparing {posOfxColumn} vs {posOfyColunm} {name}")
    plt.xlabel(posOfxColumn)
    plt.ylabel(posOfyColunm)
    plt.tight_layout()
    plt.show()


def displayingPiechart(data, column):
    name = "Piechart"
    value_counts = data[column].value_counts()
    labels = value_counts.index
    counts = value_counts.values

    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=labels,colors=sns.color_palette('Set3'))
    plt.title(f"{column} {name}")
    plt.axis('equal')
    plt.show()

        
def main():
    try:
        file_path = input("Give me your path to display your data: ")
        data1 = loadDataFromPC(file_path)
        data = loadDataFromPC(file_path)
        dataAfterProcessing = handeling_data(data)
        while True:
            print("Press 1. To display Histogram")
            print("Press 2. To display Box Plot")
            print("Press 3. To display Scatter Plot")
            print("Press 4. To display Pie Chart")
            print("Press 5. To Leave")

            userChoice = int(input("Enter your choice (1/2/3/4/5): "))

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
                for i, column in enumerate(data1.columns):
                    print(f"{i}. {column}")

                column_choice = int(input("Enter the number of column you want: "))
                if 0 <= column_choice < len(data.columns):
                    column = data.columns[column_choice]
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
                    displayingPiechart(data, column)
                else:
                    print("Invalid choice. Please try again.")

            elif userChoice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
