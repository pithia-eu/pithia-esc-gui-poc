from ontology.services import (
    get_graph_of_pithia_ontology_component,
    get_parent_node_ids_of_node_id,
)


# Search form setup
def get_parents_of_registered_ontology_terms(ontology_term_ids, ontology_component, parent_node_ids, g=None):
    if g is None:
        g = get_graph_of_pithia_ontology_component(ontology_component)
    for id in ontology_term_ids:
        parent_node_ids_of_id = get_parent_node_ids_of_node_id(id, ontology_component, [], g)
        if len(parent_node_ids_of_id) > 0:
            parent_node_ids.extend(parent_node_ids_of_id)
            parent_node_ids = get_parents_of_registered_ontology_terms(parent_node_ids_of_id, ontology_component, parent_node_ids, g=g)
    return parent_node_ids