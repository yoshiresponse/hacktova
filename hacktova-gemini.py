import pandas as pd
from lxml import etree
from collections import defaultdict

def create_xbrl_from_excel(excel_file, output_file):
    """
    Reads data from an Excel file, transforms it, and writes it to an XBRL file,
    grouping fields by path1 first, then by ID.

    Args:
        excel_file (str): Path to the input Excel file.
        output_file (str): Path to the output XBRL file.
    """

    # Define namespaces
    namespaces = {
        "xbrli": "http://www.xbrl.org/2003/instance",
        "link": "http://www.xbrl.org/2003/linkbase",
        "bd-t": "http://www.nltaxonomie.nl/nt18/bd/20231213/dictionary/bd-tuples",
        "bd-i": "http://www.nltaxonomie.nl/nt18/bd/20231213/dictionary/bd-data",
        "bd-i-ext1": "http://www.nltaxonomie.nl/nt18/bd/20240221/dictionary/bd-data-ext1",
        "nl-cd": "http://www.nltaxonomie.nl/nt18/sbr/20230301/dictionary/nl-common-data",
        "bd-t-ext1": "http://www.nltaxonomie.nl/nt18/bd/20240221/dictionary/bd-tuples-ext1",
        "iso4217": "http://www.xbrl.org/2003/iso4217",
        "xlink": "http://www.w3.org/1999/xlink",
        "sbr": "http://www.nltaxonomie.nl/2011/xbrl/xbrl-syntax-extension",
        "sbr-dim": "http://www.nltaxonomie.nl/2013/xbrl/sbr-dimensional-concepts",
        "bd-codes": "http://www.nltaxonomie.nl/nt18/bd/20231213/dictionary/bd-codes",
        "bd-types": "http://www.nltaxonomie.nl/nt18/bd/20231213/dictionary/bd-types",
        "bd-abstr": "http://www.nltaxonomie.nl/nt18/bd/20231213/presentation/bd-abstracts",
        "bd-codes-ext1": "http://www.nltaxonomie.nl/nt18/bd/20240221/dictionary/bd-codes-ext1",
        "bd-types-ext1": "http://www.nltaxonomie.nl/nt18/bd/20240221/dictionary/bd-types-ext1",
        "bd-rpt-erf": "http://www.nltaxonomie.nl/nt18/bd/20240221/entrypoints/bd-rpt-erf-aangifte-2024",
        "bd-abstr-ext1": "http://www.nltaxonomie.nl/nt18/bd/20240221/presentation/bd-abstr-ext1",
        "bd-lr-pre-ext1": "http://www.nltaxonomie.nl/nt18/bd/20240221/presentation/bd-linkroles-pre-ext1",
        "bd-lr-hd-ext1": "http://www.nltaxonomie.nl/nt18/bd/20240221/validation/bd-linkroles-tables-ext1",
        "iso3166-enum-sbr": "http://www.nltaxonomie.nl/nt18/sbr/20230301/dictionary/iso3166-countrycodes-2022-11-29",
        "iso4217-enum-sbr": "http://www.nltaxonomie.nl/nt18/sbr/20230301/dictionary/iso4217-currencycodes-2023-01-01",
        "nl-codes": "http://www.nltaxonomie.nl/nt18/sbr/20230301/dictionary/nl-codes",
        "nl-types": "http://www.nltaxonomie.nl/nt18/sbr/20230301/dictionary/nl-types",
        "sbi": "http://www.nltaxonomie.nl/nt18/sbr/20230301/dictionary/sbi-businesscodes-2022",
        "xl": "http://www.xbrl.org/2003/XLink",
        "dtr-types": "http://www.xbrl.org/dtr/type/2020-01-21",
        "xbrldt": "http://xbrl.org/2005/xbrldt",
        "gen": "http://xbrl.org/2008/generic",
        "label": "http://xbrl.org/2008/label"
    }

    # Create the root element
    root = etree.Element(f"{{{namespaces['xbrli']}}}xbrl", nsmap=namespaces)

    # Add schemaRef
    schema_ref = etree.SubElement(root, f"{{{namespaces['link']}}}schemaRef")
    schema_ref.set(f"{{{namespaces['xlink']}}}type", "simple")
    schema_ref.set(f"{{{namespaces['xlink']}}}href", "http://www.nltaxonomie.nl/nt18/bd/20240221/entrypoints/bd-rpt-erf-aangifte-2024.xsd")

    # Create a context element
    context = etree.SubElement(root, f"{{{namespaces['xbrli']}}}context", id="ctx1")
    entity = etree.SubElement(context, f"{{{namespaces['xbrli']}}}entity")

    # Read Excel data using pandas
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"Error: Excel file '{excel_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Group by path1 first - all elements with the same path1 will go into the same parent
    # regardless of their ID
    path1_data = defaultdict(list)
    
    for index, row in df.iterrows():
        try:
            id_value = str(row['ID']).strip()
            path1 = str(row['path1']).strip()
            field = str(row['field']).strip()
            value = str(row['value']).strip()
            
            # Add all fields to the path1 group
            path1_data[path1].append((field, value))
            
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue

    # Process each path1 group
    for path1, field_value_pairs in path1_data.items():
        try:
            print(f"Processing Path1: {path1}") # Debugging
            
            # Create one parent element for each path1
            parent_element_name = path1.split(':')[1]
            parent_element = etree.SubElement(root, f"{{{namespaces[path1.split(':')[0]]}}}{parent_element_name}")
            
            # Add all child elements under this parent
            for field, value in field_value_pairs:
                print(f"  Adding Field: {field}, Value: {value}") # Debugging
                element_name = field.split(':')[1]
                element = etree.SubElement(parent_element, f"{{{namespaces[field.split(':')[0]]}}}{element_name}", contextRef="ctx1")
                element.text = value
                
        except Exception as e:
            print(f"Error creating elements for Path1 {path1}: {e}")

    # Write the XML tree to a file
    try:
        tree = etree.ElementTree(root)
        tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"XBRL file created successfully: {output_file}")
    except Exception as e:
        print(f"Error writing XBRL file: {e}")

if __name__ == '__main__':
    create_xbrl_from_excel('test aanmaak xbrl01.xlsx', 'output.xbrl')