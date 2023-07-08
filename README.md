# :sparkles: ReConnect-ReCollect XML Parsing and Term Matching Automation Tool :sparkles:

### Project Website :computer:
Visit us at [Reconnect Recollect](https://www.reconnect-recollect.com/).

### Overview
This repository houses an automation tool designed for parsing local XML files and matching terms within the parsed content. Our tool assists in auditing XML files, extracting valuable insights, and visualizing trends. It is especially useful for researchers dealing with large sets of XML data.

### Key Features
Our tool offers the following key features:

1. **XML File Parsing**: It can parse multiple XML files into dataframes, exporting the parsed data into CSV format. The parsed information includes:
   
   * Filename
   * EAD ID
   * Title
   * Abstract
   * Language
   * Scope Content
   * Control Access
   * Subjects
   * Genre Forms
   * Geo Names
   * Person Names
   * Corporate Names
   * Family Names
   * Respective Sources for Each
   * Biography History
   * Custodian History

2. **Term Matching**: Our tool can match predefined terms (including potentially harmful terms) within the parsed data, exporting these matches into another CSV file. The matched results include:
   * EAD ID
   * Source Filename
   * Title
   * Term
   * Matched Times
   * Matched From
   * Matched Paragraph

3. **Data Visualization**: The tool also provides visualizations for the frequency of matched terms, elements with the highest term occurrences, term frequencies across subsections, and source frequencies.

### Repository Contents

This GitHub repository contains:
* **Automation_tool_(v_07.08.2023).ipynb**: This is the main automation tool. You can download and modify it to apply to your XML files. Note: GitHub might not render Plotly visualizations. To view the full script with all visualizations, see the HTML version.
* **Automation_tool_(v_07.08.2023).html**: This HTML version of the tool includes all visualizations.
* **parsed_dfs**: This folder contains all dataframes parsed from the sample XML files.
* **matched_results**: This folder contains all matching results based on our predefined harmful term list.
* **terms_all.txt; terms_contexual.txt; terms_main.txt**: These files contain different versions of the harmful term list we defined.

:heart: If you have any further questions, encounter issues, or need additional assistance, please don't hesitate to raise an issue in this repository. Your feedback and suggestions for improvements are always appreciated.
