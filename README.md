Mermaid to XMI Converter
Overview
This repository contains a Python script (mermaid_to_xmi.py) that converts sequence diagrams written in Mermaid syntax into XMI (XML Metadata Interchange) format. The generated XMI files can be imported into UML modeling tools like IBM Engineering Systems Design Rhapsody to create sequence diagrams. This tool is useful for automating the conversion of text-based sequence diagrams into a format compatible with UML tools, saving time in model-based system design workflows.
Features

Converts Mermaid sequence diagrams to UML 2.x XMI format.
Supports lifelines, messages, and fragments (e.g., alt, loop).
Handles notes and self-messages within the diagram.
Generates XMI files that can be imported into Rhapsody or other UML-compliant tools.

Requirements

Python: Version 3.6 or higher (tested with Python 3.13.3).
Operating System: Compatible with Windows, macOS, and Linux.
Dependencies: Uses Python's standard library (xml.etree.ElementTree, re, uuid). No external packages required.

Installation

Clone the Repository:
git clone https://github.com/<your-username>/mermaid-to-xmi-converter.git
cd mermaid-to-xmi-converter


Ensure Python is Installed:

Verify Python installation:python --version


If Python is not installed, download it from python.org and follow the installation instructions.



Usage

Prepare Input Files:

Create text files containing Mermaid sequence diagrams.
Example: example_diagram.txt:sequenceDiagram
    participant A as ActorA
    participant B as ActorB
    A->>B: Send message
    alt Condition
        B->>A: Reply yes
    else
        B->>A: Reply no
    end
    Note over A: This is a note




Run the Script:

Place your Mermaid text file in the same directory as mermaid_to_xmi.py.
Execute the script with the input file, output file, and diagram name:python mermaid_to_xmi.py


The script is configured to process two files by default:
hld_mermaid.txt → hld_sequence.xmi (named HLD_SequenceDiagram)
lld_mermaid.txt → lld_sequence.xmi (named LLD_SequenceDiagram)


To process a custom file, modify the script’s if __name__ == "__main__": block:convert_mermaid_to_xmi('example_diagram.txt', 'example_sequence.xmi', 'ExampleDiagram')




Import into Rhapsody:

Open IBM Rhapsody.
Create a new project (File > New Project > UML profile).
Import the XMI file:
Tools > Import > From OMG UML/XMI.
Select the generated XMI file (e.g., hld_sequence.xmi).
Import into a package (e.g., HLD).


Verify the sequence diagram in Rhapsody.
Save the project as a .rpy file.



Example Output
The script converts the Mermaid text into a UML 2.x XMI file. Below is a snippet of the generated XMI structure:
<?xml version='1.0' encoding='utf-8'?>
<uml:Model xmi:version="2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1" xmi:id="_..." name="Model">
    <uml:packagedElement xmi:type="uml:Interaction" xmi:id="_..." name="HLD_SequenceDiagram">
        <uml:lifeline xmi:id="_..." name="ActorA" represents="_..."/>
        <uml:lifeline xmi:id="_..." name="ActorB" represents="_..."/>
        <uml:message xmi:id="_..." name="Send message" messageSort="synchCall" sendEvent="_..." receiveEvent="_..."/>
        <!-- Additional elements -->
    </uml:packagedElement>
</uml:Model>

Troubleshooting

Namespace Errors: If Rhapsody reports errors like "The prefix 'uml' is not bound," ensure the xmlns:uml and xmlns:xmi attributes are present in the root <uml:Model> element.
Import Issues: Verify that Rhapsody is using a compatible profile (UML or SysML) and that the XMI version (2.1) matches Rhapsody’s expectations.
Diagram Rendering: After import, you may need to adjust the diagram layout in Rhapsody for better readability.

Contributing
Contributions are welcome! If you encounter issues or have enhancements, please:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add feature").
Push to your branch (git push origin feature/your-feature).
Open a pull request with a description of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or support, feel free to open an issue on this repository or contact the maintainer at <your-email> (optional).
