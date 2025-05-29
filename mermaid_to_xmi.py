import re
import uuid
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os

def generate_id():
    """Generate a unique ID for XMI elements."""
    return f"_{uuid.uuid4().hex}"

def parse_mermaid(mermaid_text):
    """Parse Mermaid sequence diagram text to extract lifelines, messages, and fragments."""
    lifelines = []
    messages = []
    fragments = []
    current_fragment = None

    lines = mermaid_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%'):
            continue
        # Parse lifelines (e.g., participant IVI as IVI System)
        if line.startswith("participant"):
            match = re.match(r"participant (\w+) as (.+)", line)
            if match:
                alias, name = match.groups()
                lifelines.append((alias, name))
        # Parse messages (e.g., IVI->>Service: Start service)
        elif "->>" in line:
            match = re.match(r"(\w+)->>(\w+):\s*(.+)", line)
            if match:
                sender, receiver, message = match.groups()
                if current_fragment:
                    current_fragment["messages"].append((sender, receiver, message))
                else:
                    messages.append((sender, receiver, message))
        # Parse fragments (e.g., alt Reboot occurs)
        elif line.startswith("alt"):
            condition = line.split("alt")[1].strip()
            current_fragment = {"type": "alt", "condition": condition, "messages": []}
            fragments.append(current_fragment)
        # Parse loop fragments
        elif line.startswith("loop"):
            condition = line.split("loop")[1].strip()
            current_fragment = {"type": "loop", "condition": condition, "messages": []}
            fragments.append(current_fragment)
        elif line.startswith("end"):
            current_fragment = None
        # Parse notes (e.g., Note over SM: USB mounted with binary)
        elif line.startswith("Note"):
            match = re.match(r"Note over (\w+):\s*(.+)", line)
            if match:
                target, note = match.groups()
                messages.append((target, target, f"Note: {note}"))

    return lifelines, messages, fragments

def generate_xmi(lifelines, messages, fragments, diagram_name):
    """Generate an XMI file for a UML sequence diagram."""
    # Root element with proper namespace declarations
    model = Element('uml:Model', {
        'xmi:version': '2.1',
        'xmlns:xmi': 'http://schema.omg.org/spec/XMI/2.1',
        'xmlns:uml': 'http://schema.omg.org/spec/UML/2.1',
        'xmi:id': generate_id(),
        'name': 'ClusterReflashModel'
    })

    # Interaction
    interaction = SubElement(model, 'uml:packagedElement', {
        'xmi:type': 'uml:Interaction',
        'xmi:id': generate_id(),
        'name': diagram_name
    })

    # Lifelines
    lifeline_dict = {}
    for alias, name in lifelines:
        lifeline_id = generate_id()
        lifeline = SubElement(interaction, 'uml:lifeline', {
            'xmi:id': lifeline_id,
            'name': name,
            'represents': generate_id()
        })
        lifeline_dict[alias] = lifeline_id

    # Messages
    for sender, receiver, message in messages:
        msg_id = generate_id()
        send_event_id = generate_id()
        receive_event_id = generate_id()

        # Message
        SubElement(interaction, 'uml:message', {
            'xmi:id': msg_id,
            'name': message,
            'messageSort': 'synchCall' if not message.startswith("Note:") else 'asynchCall',
            'sendEvent': send_event_id,
            'receiveEvent': receive_event_id
        })

        # Send and receive events
        SubElement(interaction, 'uml:fragment', {
            'xmi:type': 'uml:MessageOccurrenceSpecification',
            'xmi:id': send_event_id,
            'covered': lifeline_dict[sender],
            'message': msg_id
        })
        SubElement(interaction, 'uml:fragment', {
            'xmi:type': 'uml:MessageOccurrenceSpecification',
            'xmi:id': receive_event_id,
            'covered': lifeline_dict[receiver],
            'message': msg_id
        })

    # Fragments
    for fragment in fragments:
        combined_fragment_id = generate_id()
        combined_fragment = SubElement(interaction, 'uml:fragment', {
            'xmi:type': 'uml:CombinedFragment',
            'xmi:id': combined_fragment_id,
            'interactionOperator': fragment['type']
        })

        operand_id = generate_id()
        operand = SubElement(combined_fragment, 'uml:operand', {
            'xmi:id': operand_id
        })

        guard_id = generate_id()
        guard = SubElement(operand, 'uml:guard', {
            'xmi:id': guard_id
        })
        SubElement(guard, 'uml:specification', {'value': fragment['condition']})

        for sender, receiver, message in fragment['messages']:
            msg_id = generate_id()
            send_event_id = generate_id()
            receive_event_id = generate_id()

            SubElement(interaction, 'uml:message', {
                'xmi:id': msg_id,
                'name': message,
                'messageSort': 'synchCall',
                'sendEvent': send_event_id,
                'receiveEvent': receive_event_id
            })

            SubElement(operand, 'uml:fragment', {
                'xmi:type': 'uml:MessageOccurrenceSpecification',
                'xmi:id': send_event_id,
                'covered': lifeline_dict[sender],
                'message': msg_id
            })
            SubElement(operand, 'uml:fragment', {
                'xmi:type': 'uml:MessageOccurrenceSpecification',
                'xmi:id': receive_event_id,
                'covered': lifeline_dict[receiver],
                'message': msg_id
            })

    return model

def convert_mermaid_to_xmi(input_file, output_file, diagram_name):
    """Convert a Mermaid text file to an XMI file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        mermaid_text = f.read()

    lifelines, messages, fragments = parse_mermaid(mermaid_text)
    xmi_content = generate_xmi(lifelines, messages, fragments, diagram_name)

    # Write XMI file with proper XML declaration
    tree = ElementTree(xmi_content)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    # Convert HLD
    convert_mermaid_to_xmi('hld_mermaid.txt', 'hld_sequence.xmi', 'HLD_ClusterReflashSequence')
    # Convert LLD
    convert_mermaid_to_xmi('lld_mermaid.txt', 'lld_sequence.xmi', 'LLD_ClusterReflashSequence')