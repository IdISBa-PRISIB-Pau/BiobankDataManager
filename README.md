# Biobank Data Manager

## Overview
The Biobank Data Manager is a Python application designed for data entry and exploration of biobank data. It provides a graphical user interface (GUI) for managing data related to MIABIS, SPREC, OMOP Person, Condition Occurrence, and Procedure Occurrence.

## Features
- Tabbed interface for different data categories
- Form fields for data entry
- Save data to CSV
- Load data from CSV
- Dynamic table creation with scrollbars

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/BiobankDataManager.git
    ```
2. Navigate to the project directory:
    ```sh
    cd BiobankDataManager
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
Run the application:
```sh
python Main.py
```

## Current Issues
. Horizontal Scrollbar Not Working Properly: The horizontal scrollbar does not function correctly after adjusting the column width.
. Table Height Issue: The table height is too small, making it difficult to view the content.
. Dynamic Width Adjustment: The total width of the Treeview should adjust dynamically when any column width is changed, but it is not working as expected.

## Contributing
Fork the repository.  
Create a new branch (git checkout -b feature-branch).  
Make your changes.  
Commit your changes (git commit -m 'Add some feature').  
Push to the branch (git push origin feature-branch).  
Open a pull request.  
