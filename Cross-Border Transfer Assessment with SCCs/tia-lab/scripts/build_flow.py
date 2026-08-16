# scripts/build_flow.py
def load_dataflow(yaml_path: str) -> dict:
    """
    Load and validate the data flow definition.
    Must check required keys: data_categories, subjects, purpose,
    transfer_frequency, locations, sub_processors.
    """
    # TODO: implement
    pass

def classify_sensitivity(fields: list) -> dict:
    """
    Map each field to a sensitivity tier.
    Return dict: {field_name: tier}
    """
    # TODO: implement
    pass

def render_diagram(flow: dict, output_path: str) -> None:
    """
    Generate a Graphviz .dot representation of the flow
    and render to PNG using the `graphviz` CLI or Python bindings.
    """
    # TODO: implement
    pass
