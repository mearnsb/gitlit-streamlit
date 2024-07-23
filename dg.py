from fuzzywuzzy import fuzz
import pandas as pd 

def fuzz_run_search(target_text):
    """This method takes in a target text and uses fuzzy matching to find the most similar row in a "faker_name_list.csv" dataframe. It first imports the necessary libraries, including pandas and fuzzywuzzy. Then, it loads a dataframe from a CSV file and creates a copy to work on. Using the target text, it calculates the fuzzy matching scores for each row in the copy and adds them as a new column. It then finds the row with the highest similarity score and prints it as the top match. Additionally, it prints the top 3 matching descriptions and returns them as a dataframe. This method is useful for quickly finding similar data in a large dataset."""    
    df = pd.read_csv('faker_name_list.csv')
    df_copy = df.copy()
    df_copy['similarity_score'] = df_copy['id'].apply(lambda x: fuzz.token_set_ratio(x, target_text))
    most_similar_row = df_copy.loc[df_copy['similarity_score'].idxmax()]
    n = 10
    top_n_matches = df_copy.sort_values(by='similarity_score', ascending=False).head(n)
    return top_n_matches['id'].tolist()
    #return top_n_matches[['id', 'description']]

def fuzz_generate_string(data_elements, name="data"): 
    code_string = 'data = {'
    for l in data_elements: 
    
        if len(l) > 0:
            code_string += f'"{l}" : Faker().{l}() ,'
    code_string += '}'
    code_string = code_string.replace("data", name)
    # This is the data object to use
    print(code_string)
    return code_string


from fuzzywuzzy import fuzz
import pandas as pd 

def fuzz_search(target_text):
    df = pd.read_csv('search_list.csv')
    df_copy = df.copy()
    df_copy['similarity_score'] = df_copy['id'].apply(lambda x: fuzz.token_set_ratio(x, target_text))
    most_similar_row = df_copy.loc[df_copy['similarity_score'].idxmax()]
    n = 3
    top_n_matches = df_copy.sort_values(by='similarity_score', ascending=False).head(n)
    return top_n_matches['id'].tolist()

