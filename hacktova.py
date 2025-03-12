import xml.etree.ElementTree as ET

def create_mfd_from_xbrl(xbrl_file, mfd_file):
    """
    Creates an MFD (MapForce Definition) XML file based on an XBRL file structure.

    Args:
        xbrl_file (str): Path to the input XBRL file.
        mfd_file (str): Path to the output MFD file.
    """

    try:
        tree = ET.parse(xbrl_file)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Error: XBRL file '{xbrl_file}' not found.")
        return
    except ET.ParseError as e:
        print(f"Error parsing XBRL file '{xbrl_file}': {e}")
        return

    # Define the MFD root element and attributes
    mapping = ET.Element("mapping", attrib={"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", "version": "22"})

    # Add <resources/> element
    resources = ET.SubElement(mapping, "resources")

    # Create the <component> element
    component = ET.SubElement(mapping, "component", attrib={"name": "defaultmap", "uid": "1", "editable": "1", "blackbox": "0"})
    properties = ET.SubElement(component, "properties", attrib={"SelectedLanguage": "builtin"})
    structure = ET.SubElement(component, "structure")
    children = ET.SubElement(structure, "children")

    # Create input component (similar to your example MFD)
    input_component = ET.SubElement(children, "component", attrib={"name": "input", "library": "core", "uid": "6", "kind": "6"})
    sources = ET.SubElement(input_component, "sources")
    datapoint = ET.SubElement(sources, "datapoint")
    targets = ET.SubElement(input_component, "targets")
    datapoint = ET.SubElement(targets, "datapoint")
    view = ET.SubElement(input_component, "view", attrib={"ltx": "172", "lty": "46", "rbx": "245", "rby": "82"})
    data = ET.SubElement(input_component, "data")
    input_element = ET.SubElement(data, "input", attrib={"datatype": "string"}) # removed preview values for flexibility
    input_element.text = xbrl_file # set the path to the xbrl file
    parameter = ET.SubElement(data, "parameter", attrib={"usageKind": "input", "name": "input"})

    #Create the XBRL component
    xbrl_component = ET.SubElement(children, "component", attrib={"name": "bd-rpt-erf-aangifte-2024", "library": "xbrl", "uid": "7", "kind": "27"})
    properties_xbrl = ET.SubElement(xbrl_component, "properties", attrib={"XSLTTargetEncoding": "UTF-8", "XSLTDefaultOutput": "1", "XBRLShowAllConcepts": "1", "XBRLShowAllConceptsRaw": "1"})
    view_xbrl = ET.SubElement(xbrl_component, "view", attrib={"ltx": "1426", "lty": "74", "rbx": "2075", "rby": "1113"})
    data_xbrl = ET.SubElement(xbrl_component, "data")
    root_xbrl = ET.SubElement(data_xbrl, "root", attrib={"scrollposition": "8472"})
    header_xbrl = ET.SubElement(root_xbrl, "header")
    namespaces_xbrl = ET.SubElement(header_xbrl, "namespaces")

    # Adding some default namespaces
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.xbrl.org/2003/instance"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.altova.com/mapforce"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.xbrl.org/2003/linkbase"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.nltaxonomie.nl/nt18/sbr/20230301/dictionary/nl-common-data"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.nltaxonomie.nl/2013/xbrl/sbr-dimensional-concepts"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.nltaxonomie.nl/nt18/bd/20240221/dictionary/bd-data-ext1"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.nltaxonomie.nl/nt18/bd/20240221/dictionary/bd-tuples-ext1"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.nltaxonomie.nl/nt18/bd/20231213/dictionary/bd-tuples"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "view"})
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.nltaxonomie.nl/nt18/bd/20240221/presentation/bd-abstr-ext1"})
    ET.SubElement(namespaces_xbrl, "namespace")
    ET.SubElement(namespaces_xbrl, "namespace", attrib={"uid": "http://www.nltaxonomie.nl/nt18/bd/20231213/dictionary/bd-data"})

    # Get the schema location from the XBRL file
    schema_ref = root.find('.//{http://www.xbrl.org/2003/linkbase}schemaRef')
    if schema_ref is not None:
        schema_location = schema_ref.get('{http://www.w3.org/1999/xlink}href')
    else:
        schema_location = "http://www.nltaxonomie.nl/nt18/bd/20240221/entrypoints/bd-rpt-erf-aangifte-2024.xsd"
        print("SchemaRef not found, using default.")

    xbrl_element = ET.SubElement(data_xbrl, "xbrl", attrib={"schema": schema_location, "inputinstance": xbrl_file, "outputinstance": "output.xbrl"})

    # Create the graph element
    graph = ET.SubElement(structure, "graph", attrib={"directed": "1"})
    edges = ET.SubElement(graph, "edges")
    vertices = ET.SubElement(graph, "vertices")

    # Create a vertex for the input component
    vertex_input = ET.SubElement(vertices, "vertex", attrib={"vertexkey": "6"})
    edges_input = ET.SubElement(vertex_input, "edges")
    #ET.SubElement(edges_input, "edge", attrib={"vertexkey": "13"}) #Connects to the excel part, which is now the xbrl

    # Create a vertex for the xbrl component
    vertex_xbrl = ET.SubElement(vertices, "vertex", attrib={"vertexkey": "7"})
    edges_xbrl = ET.SubElement(vertex_xbrl, "edges")
    # No edges for now

    # Write the XML tree to a file
    try:
        tree = ET.ElementTree(mapping)
        ET.indent(tree, space="    ", level=0) #for pretty print
        tree.write(mfd_file, encoding="UTF-8", xml_declaration=True)
        print(f"MFD file created successfully: {mfd_file}")
    except Exception as e:
        print(f"Error writing MFD file: {e}")

if __name__ == "__main__":
    xbrl_file = "output.xbrl"  # Replace with your XBRL file path
    mfd_file = "output.mfd"  # Replace with your desired MFD file path
    create_mfd_from_xbrl(xbrl_file, mfd_file)