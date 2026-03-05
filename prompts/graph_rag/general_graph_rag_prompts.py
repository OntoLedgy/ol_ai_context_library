# Define the prompt template for entity extraction
prompt_template_entities = """
You are an expert at extracting entities from text.
Please identify all entities in the following query and classify them by type.

Query: {query_str}

Extract entities like people, organizations, locations, products, and events.
"""