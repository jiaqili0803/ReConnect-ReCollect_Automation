#!/usr/bin/env python
# coding: utf-8

# ## Automation Tool for matching terms in local XML files 
# (version 03/10/2023)

# ### Import packages and settings
# 
# * pandas: a library for data manipulation and analysis.
# * numpy: a library for scientific computing with Python.
# * lxml: a library for processing XML and HTML documents.
# * os: a library for operating system-related functions.
# * re: a library for regular expressions, used for pattern matching.
# * warnings: a library for issuing warnings to the user.
# * plotly.express: a library for creating interactive plots and charts.

# In[1]:


import pandas as pd 
import numpy as np
from lxml import etree
import os
import re
import warnings
import plotly.express as px
import plotly.io as pio


# * sets a filter for warnings if needed:

# In[2]:


# warnings.filterwarnings("ignore", category=UserWarning)


# * controls the maximum width of each column in a pandas dataframe. By setting it to -1, pandas will display the full contents of each column, without any truncation:

# In[3]:


pd.set_option('display.max_colwidth', -1)


# * controls the maximum number of rows that pandas will display in the console output. By setting it to None, pandas will display all rows of a dataframe or series, regardless of how many there are:

# In[4]:


# pd.set_option('display.max_rows', None)


# ### Define functions to extract content from xml files
# #### 1. xml files without namespaces
# #### 2. xml files with namespaces

# In[5]:


# function 1 - parse the xml file without namespaces

def parse_xml_to_df(xml_file):
    
    try:
        # Parse the XML file
        tree = etree.parse(xml_file)
        root = tree.getroot()

        # Create a list to store the data
        data = []

        # Iterate over all elements in the XML file
        for element in root:
            # Create a dictionary to store the data for each element
            element_data = {}
            
            ## extract id
            eadid = root.find('.//eadid')
            if eadid is not None:
                element_data['ead_id'] = eadid.text
            
            publicid = eadid.get('publicid')
            if publicid is not None:
                result = re.search(r'::(.*)\.xml', publicid)
                if result:
                    public_id = result.group(1).split('::')[-1]
                    element_data['public_id'] = public_id    
            
            ## EXtract abstract
            abstract = element.find('.//abstract')
            if abstract is not None:
                element_data['abstract'] = abstract.text

            ## Extract language
            language = element.find('.//langmaterial')
            if language is not None:
                element_data['language'] = ''.join(language.itertext())

            ## Extract scopecontent
            scopecontent = element.findall('./scopecontent')
            if scopecontent:
                scopecontent_texts = []
                for sc in scopecontent:
                    paragraphs = sc.findall('./p')
                    if paragraphs:
                        for p in paragraphs:
                            p_text = ""
                            for child in p.itertext():
                                p_text += child
                            scopecontent_texts.append(p_text)
                element_data['scopecontent'] = ', '.join(scopecontent_texts)

            ## Extract controlaccess - e.g., <subject>, <genreform>, <geogname>, <persname>, <corpname>, <famname> etc.
            controlaccess = element.find('.//controlaccess')
            if controlaccess is not None:
                subjects = controlaccess.findall('.//subject')
                if subjects:
                    element_data['subjects'] = ', '.join([subject.text for subject in subjects])
                genreforms = controlaccess.findall('.//genreform')
                if genreforms:
                    element_data['genreforms'] = ', '.join([genreform.text for genreform in genreforms])
                geognames = controlaccess.findall('.//geogname')
                if geognames:
                    element_data['geognames'] = ', '.join([geogname.text for geogname in geognames])
                persnames = controlaccess.findall('.//persname')
                if persnames:
                    element_data['persnames'] = ', '.join([persname.text for persname in persnames])
                corpnames = controlaccess.findall('.//corpname')
                if corpnames:
                    element_data['corpnames'] = ', '.join([corpname.text for corpname in corpnames])
                famnames = controlaccess.findall('.//famname')
                if famnames:
                    element_data['famnames'] = ', '.join([famname.text for famname in famnames])

            ## Extract bioghist    
            bioghist = element.findall('./bioghist')
            if bioghist:
                bioghist_texts = []
                for bio in bioghist:
                    paragraphs = bio.findall('./p')
                    if paragraphs:
                        for p in paragraphs:
                            p_text = ""
                            for child in p.itertext():
                                p_text += child
                            bioghist_texts.append(p_text)
                element_data['bioghist'] = ', '.join(bioghist_texts)

            ## Extract custodhist
            custodhist = element.findall('./custodhist')
            if custodhist:
                custodhist_texts = []
                for cus in custodhist:
                    paragraphs = cus.findall('./p')
                    if paragraphs:
                        for p in paragraphs:
                            p_text = ""
                            for child in p.itertext():
                                p_text += child
                            custodhist_texts.append(p_text)
                element_data['custodhist'] = ', '.join(custodhist_texts)



            # Add the element data to the list of data
            data.append(element_data)

        # print(data)
        
        df = pd.DataFrame([d for d in data if len(d)>2])

    except:
        # If error, print the error message and skip the file
        print("Error parsing file:", xml_file)
        df = None
    
    return df


# <span style="background-color: yellow; font-size: 15px;"> YOUR TODO: If the xml files contain namespaces, you need to define the namespace prefix and URI:</span>
# 

# In[6]:


# TODO: Define the namespace prefix and URI

# e.g., for SCRC:
namespaces = {
    "ead": "urn:isbn:1-931666-22-9",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}


# In[7]:


# Function 2 - parse xml file with namespaces - (FOR SCRC files)

def parse_xml_to_df_ns(xml_file):
    try:
        
        # Parse the XML file
        tree = etree.parse(xml_file)
        root = tree.getroot()

        # Create a list to store the data
        data = []

        # Iterate over all elements in the XML file
        for element in root:
            # Create a dictionary to store the data for each element
            element_data = {}

            ## extract id
            eadid = root.find('.//ead:eadid', namespaces)
            if eadid is not None:
                element_data['ead_id'] = eadid.text

            publicid = eadid.get('publicid')
            if publicid is not None:
                result = re.search(r'::(.*)\.xml', publicid)
                if result:
                    public_id = result.group(1).split('::')[-1]
                    element_data['public_id'] = public_id

            ## extract abstract
            abstract = element.find('.//ead:abstract', namespaces)
            if abstract is not None:
                element_data['abstract'] = abstract.text
             
            ## Extract language
            language = root.findall('.//ead:langmaterial', namespaces)[-1]
            if language is not None:
                element_data['language'] = ''.join(language.itertext())
                
            ## Extract scopecontent
            scopecontent = element.find('.//ead:scopecontent', namespaces)
            if scopecontent is not None:
                scopecontent_texts = []
                p_elements = scopecontent.findall('.//ead:p', namespaces)
                for p in p_elements:
                    p_text = ""
                    for child in p.itertext():
                        p_text += child
                    scopecontent_texts.append(p_text)
                element_data['scopecontent'] = ', '.join(scopecontent_texts)    

            
            ## Extract bioghist    
            bioghist = element.find('.//ead:bioghist', namespaces)
            if bioghist is not None:
                bioghist_texts = []
                p_elements = bioghist.findall('.//ead:p', namespaces)
                
                for p in p_elements:
                    p_text = ""
                    for child in p.itertext():
                        p_text += child
                    bioghist_texts.append(p_text)
                element_data['bioghist'] = ', '.join(bioghist_texts) 
           
            
            ## Extract custodhist    
            custodhist = element.find('.//ead:custodhist', namespaces)
            if custodhist is not None:
                custodhist_texts = []
                p_elements = custodhist.findall('.//ead:p', namespaces)
                
                for p in p_elements:
                    p_text = ""
                    for child in p.itertext():
                        p_text += child
                    custodhist_texts.append(p_text)
                element_data['custodhist'] = ', '.join(custodhist_texts)
            
            
            ## Extract controlaccess - e.g., <subject>, <genreform>, <geogname>, <persname>, <corpname>, <famname> etc.
            controlaccess = element.find('.//ead:controlaccess', namespaces)
            if controlaccess is not None:
                subjects = controlaccess.findall('.//ead:subject', namespaces)
                if subjects:
                    element_data['subjects'] = ', '.join([subject.text for subject in subjects])
                genreforms = controlaccess.findall('.//ead:genreform', namespaces)
                if genreforms:
                    element_data['genreforms'] = ', '.join([genreform.text for genreform in genreforms])
                geognames = controlaccess.findall('.//ead:geogname', namespaces)
                if geognames:
                    element_data['geognames'] = ', '.join([geogname.text for geogname in geognames])
                persnames = controlaccess.findall('.//ead:persname', namespaces)
                if persnames:
                    element_data['persnames'] = ', '.join([persname.text for persname in persnames])
                corpnames = controlaccess.findall('.//ead:corpname', namespaces)
                if corpnames:
                    element_data['corpnames'] = ', '.join([corpname.text for corpname in corpnames])
                famnames = controlaccess.findall('.//ead:famname', namespaces)
                if famnames:
                    element_data['famnames'] = ', '.join([famname.text for famname in famnames])

                    
            # Add the element data to the list of data
            data.append(element_data)

        # Create a DataFrame from the list of data
        df = pd.DataFrame([d for d in data if len(d)>2])
        
    except:
        # If error, print the error message and skip the file
        print("Error parsing file:", xml_file)
        df = None

    return df


# ### An example: Try to get one extracted result

# In[8]:


# try to parse 1 xml file (without namespace)

xml_file_1 = 'RCRC_Finding_Aid_List_Bentley/Finding_Aids/umich-bhl-0052.xml'
xml_file_2 = 'SCRC_XML/adler_20221006_152012_UTC__ead.xml'
xml_file_3 = 'Clements_Library_Philippine_Islands_EAD/hillardlow_final.xml'

df = parse_xml_to_df(xml_file_1)
df


# In[9]:


# try to parse 1 xml file (with namespace)

df = parse_xml_to_df_ns(xml_file_2)
df


# ### Define functions to extract multiple files (from your local path) at the sametime

# In[10]:


# function 3 - parse multiple xml files at the sametime (without namespace)

def parse_xml_folder_to_df(folder_path):
    # Create a list to store the dataframes for each file
    dfs = []
    
    # Loop over all XML files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            df = parse_xml_to_df(file_path)
            dfs.append(df)
    
    # Concatenate the dataframes into one dataframe
    result_df = pd.concat(dfs, ignore_index=True)
    
    return result_df

# function 4 - parse multiple xml files at the sametime (with namespace)

def parse_xml_folder_to_df_ns(folder_path):
    # Create a list to store the dataframes for each file
    dfs = []
    
    # Loop over all XML files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            df = parse_xml_to_df_ns(file_path)
            dfs.append(df)
    
    # Concatenate the dataframes into one dataframe
    result_df = pd.concat(dfs, ignore_index=True)
    
    return result_df


# #### Parse multiple XML files, get dataframes

# <span style="background-color: yellow; font-size: 15px;"> YOUR TODO: change the path to your local xml files path</span>

# In[11]:


# TODO: select/ change local file path

folder1_path = "RCRC_Finding_Aid_List_Bentley/Finding_Aids"
folder2_path = "Clements_Library_Philippine_Islands_EAD"
folder3_path = "SCRC_XML"


# In[12]:


# Show extracted data - Bentley 

df1_Bentley = parse_xml_folder_to_df(folder1_path)
df1_Bentley


# In[13]:


# Show extracted data - Clements
df2_Clements = parse_xml_folder_to_df(folder2_path)

# df2_Clements


# In[14]:


# Show extracted data - SCRC 

df3_SCRC = parse_xml_folder_to_df_ns(folder3_path)

# df3_SCRC


# ### Export the above dataframes to .csv files (if needed)

# <span style="background-color: yellow; font-size: 15px;"> YOUR TODO: change the name and path of the .csv files you want</span>

# In[15]:


### export

df1_Bentley.to_csv('df1_Bentley.csv', index=True)
df2_Clements.to_csv('df2_Clements.csv', index=True)
df3_SCRC.to_csv('df3_SCRC.csv', index=True)


# ### Match terms 

# <span style="background-color: yellow; font-size: 15px;"> YOUR TODO: here is the place you can change your own defined harmful term set</span>

# In[16]:


# TODO: change term set, this is just an example of our harmful term set (current term list v.2.24)

terms = ['Civilization', 'Civilized', 'Cleanliness', 'Dwelling', 'Enemy', 'Head hunter', 'Head hunters', 'Hygiene', 'Igorot', 
             'Indigenous', 'Insurgency', 'Insurgent', 'Insurgents', 'Insurrection', 'Insurrecto', 'Insurrectos', 'Leper', 'Lepers', 
             'Mestiza', 'Mestizas', 'Mestizo', 'Mestizos', 'Moro', 'Moro Rebellion', 'Moros', 'Native', 'Natives', 'Negrito', 'Negritos', 
             'Non-Christian', 'Non-Christians', 'P.I.', 'Primitive', 'Primitives', 'Tribal', 'Tribe', 'Tribes', 'Trophies', 'Trophy', 
             'Uncivilized', 'Ilustrado', 'slave', 'slavery', 'enslaved', 'Balangiga Massacre', 'Benevolent Assimilation', 'Colonial', 
             'Colonist', 'Colonists', 'Colonization', 'Colony', 'Settler', 'Settlers']



# terms = ['Civilized', 'Civilization', 'Primitive', 'Hygiene', 'Cleanliness', 'Imperial',
#            'Dwelling', 'Native', 'Settler', 'Thomasite', 'Mestizo', 'Tribe', 'Tribal', 'Non-christian', 'Filipino', 
#            'Filipina', 'Philippine ', 'Philippines', 'Manila', 'Philippine Islands', 'Luzon', 'Mindanao', 'Baguio',
#            'Cebu', 'Mindoro', 'Palawan', 'Moro', 'Igorot', 'Indigenous', 'Indigenous Peoples', 'Negrito', 'Bontoc', 
#            'Ilongot', 'Ifugao', 'Bagobo', 'Kalinga', 'Ilocano', 'Mangyan', 'Tinguian', 'Manobo', 'Execution', 'Head hunter',
#            'Human remains', 'Balangiga Massacre', 'Enemy', 'Insurrection', 'Insurgency', 'Insurgent', 'Insurrecto', 
#            'Philippine-American War', 
#            'Philippine Insurrection']


# In[ ]:





# In[17]:


# match term function

def match_terms(row, terms):
    results = []
    for term in terms:
        for col in organized_data.columns:
            if not isinstance(row[col], float) and term in row[col]:
                # split the column into paragraphs
                paragraphs = row[col].split('\n')
                # loop through each paragraph
                for paragraph in paragraphs:
                    # check if the term is in the current paragraph
                    if term in paragraph:
                        # bold_paragraph = paragraph.replace(term, '<b>' + term + '</b>')
                        results.append({'ead_id': row['ead_id'], 'Term': term, 'Matched_Times': paragraph.count(term), 'Matched_From': col, 'Matched_Paragraph': paragraph})
    return results


# In[18]:


file_list = [df1_Bentley, df2_Clements, df3_SCRC]


# ### Matched results for - Bentley

# <span style="background-color: yellow; font-size: 15px;"> YOUR TODO: you can choose which of the dataframe/ your xml file source you want to match with the harmful terms</span>

# In[19]:


# TODO: select file pool

organized_data = df1_Bentley


# we can find from the following matched results: we can know which ead file and which section we found that term (ead_id, Matched_From), the matched times, and the Paragraph around that matched term:

# In[20]:


# matched results

results_df = pd.DataFrame([result for index, row in organized_data.iterrows() for result in match_terms(row, terms)])
results_df


# <span style="background-color: yellow; font-size: 15px;"> YOUR TODO: for the frequency and visualization, you can edit/ change the code to create your own frequency table and visualization chart, see below example:</span>

# In[21]:


# frequency of the matched results

term_frequency = results_df.groupby('Term')['Matched_Times'].sum().reset_index()
term_frequency.rename(columns={'Matched_Times': 'Total_Frequency'}, inplace=True)
term_frequency


# In[23]:


# visualization (this will not show in Github, cause GitHub does not render Plotly visualizations in its web interface)

fig = px.bar(term_frequency, x='Term', y='Total_Frequency', text='Total_Frequency')
fig.update_traces(textposition='outside', insidetextanchor='middle')
fig.update_layout(title_text="Term Found in Bentley", xaxis_title_standoff=10, height=600)
fig.show()
pio.write_image(fig, 'term_frequency_Bentley.png')


# <span style="background-color: yellow; font-size: 15px;"> YOUR TODO: use and modify this one line code to export your matched results table to .csv file</span>

# In[24]:


# export match_results to .csv
results_df.to_csv('matched_results_Bentley.csv', index=True)


# In[ ]:





# (the following codes are similar steps for Clements and SCRC xml files)

# ### Matched results for - Clements

# In[25]:


# TODO: select file pool

organized_data = df2_Clements


# In[26]:


# Create a new dataframe with the matched results
results_df = pd.DataFrame([result for index, row in organized_data.iterrows() for result in match_terms(row, terms)])
results_df


# In[27]:


# frequency

term_frequency = results_df.groupby('Term')['Matched_Times'].sum().reset_index()
term_frequency.rename(columns={'Matched_Times': 'Total_Frequency'}, inplace=True)
term_frequency


# In[28]:


# visualization

fig = px.bar(term_frequency, x='Term', y='Total_Frequency', text='Total_Frequency')
fig.update_traces(textposition='outside', insidetextanchor='middle')
fig.update_layout(title_text="Term Found in Clements", xaxis_title_standoff=10, height=600)
fig.update_traces(marker_color='orange')
fig.show()
pio.write_image(fig, 'term_frequency_Clements.png')


# In[29]:


# export match_results
results_df.to_csv('matched_results_Clements.csv', index=True)


# In[ ]:





# ### Matched results for - SCRC

# In[30]:


# TODO: select file pool

organized_data = df3_SCRC


# In[31]:


# Create a new dataframe with the matched results
results_df = pd.DataFrame([result for index, row in organized_data.iterrows() for result in match_terms(row, terms)])
results_df


# In[32]:


# frequency

term_frequency = results_df.groupby('Term')['Matched_Times'].sum().reset_index()
term_frequency.rename(columns={'Matched_Times': 'Total_Frequency'}, inplace=True)
term_frequency


# In[33]:


# visualization

fig = px.bar(term_frequency, x='Term', y='Total_Frequency', text='Total_Frequency')
fig.update_traces(textposition='outside', insidetextanchor='middle')
fig.update_layout(title_text="Term Found in SCRC", xaxis_title_standoff=10, height=600)
fig.update_traces(marker_color='green')
fig.show()
pio.write_image(fig, 'term_frequency_SCRC.png')


# In[34]:


# export match_results
results_df.to_csv('matched_results_SCRC.csv', index=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




