def normalize(name: str):
    """String normalization is a hairy beast, but we'll make a best effort."""
    name = name.lower()
    tag_index = name.find('|')
    if tag_index >= 0:
        name = name[tag_index+1:]
    name = name.strip()
    name = name.title()
    return name
