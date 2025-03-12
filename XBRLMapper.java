import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import java.io.StringReader;
import java.io.StringWriter;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import java.io.IOException;

public class XBRLMapper {

    /**
     * Maps values from Excel to XBRL based on pre-split paths and target node names.
     *
     * @param xbrlContent     The XBRL content as a String.
     * @param pathComponents  The pre-split path components (e.g., ["bd:BusinessSpecification", "SubstantialInterestSharesCapitalCommon"]).
     * @param targetNodeName  The target node name (e.g., "SubstantialInterestSharesCapitalCommon").
     * @param value           The value to map (e.g., "1772594").
     * @return The updated XBRL content as a String.
     */
    public static String MapValueToXBRL(String xbrlContent, List<String> pathComponents, String targetNodeName, String value) {
        try {
            // Parse the XBRL content into a DOM Document
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setNamespaceAware(true); // Enable namespace support
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document xbrlDocument = builder.parse(new InputSource(new StringReader(xbrlContent)));

            // Map the value to the XBRL document
            MapValueToXBRL(xbrlDocument, pathComponents, targetNodeName, value);

            // Convert the updated document back to a String
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            DOMSource source = new DOMSource(xbrlDocument);
            StringWriter writer = new StringWriter();
            StreamResult result = new StreamResult(writer);
            transformer.transform(source, result);

            return writer.toString();
        } catch (Exception e) {
            throw new RuntimeException("Error mapping value to XBRL", e);
        }
    }

    /**
     * Internal method to map the value to the XBRL document.
     */
    private static void MapValueToXBRL(Document xbrlDocument, List<String> pathComponents, String targetNodeName, String value) {
        // Start navigation from the root of the XBRL document
        Element currentNode = xbrlDocument.getDocumentElement();

        // Traverse the XBRL structure using the path components
        for (String pathPart : pathComponents) {
            NodeList children = currentNode.getChildNodes();
            boolean found = false;

            // Search for the next node in the path
            for (int i = 0; i < children.getLength(); i++) {
                Node child = children.item(i);
                if (child.getNodeType() == Node.ELEMENT_NODE && MatchesNodeName(child, pathPart)) {
                    currentNode = (Element) child; // Move to the next level
                    found = true;
                    break;
                }
            }

            // If the path part is not found, throw an exception
            if (!found) {
                throw new IllegalArgumentException("Path component not found: " + pathPart);
            }
        }

        // Assign the value to the target node
        NodeList targetNodes = currentNode.getElementsByTagName(targetNodeName);
        if (targetNodes.getLength() == 0) {
            throw new IllegalArgumentException("Target node not found: " + targetNodeName);
        }

        // Update the value of the target node
        Element targetNode = (Element) targetNodes.item(0);
        targetNode.setTextContent(value);
    }

    /**
     * Checks if a node matches the given path part.
     */
    private static boolean MatchesNodeName(Node node, String pathPart) {
        String nodeName = node.getNodeName();
        String localName = node.getLocalName();
        String namespaceURI = node.getNamespaceURI();

        // Handle namespaces (e.g., "bd:BusinessSpecification")
        if (pathPart.contains(":")) {
            String[] parts = pathPart.split(":");
            String prefix = parts[0];
            String name = parts[1];

            // Match namespace and local name
            return nodeName.equals(pathPart) || (namespaceURI != null && localName != null &&
                    localName.equals(name) && namespaceURI.endsWith(prefix));
        } else {
            // Match local name only
            return localName != null && localName.equals(pathPart);
        }
    }
}