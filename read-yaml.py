from yaml import load, Loader, Dumper

def get_yaml_data(filename):
    yaml_f = open(filename, "r").read()
    data = load(yaml_f, Loader=Loader)
    title = data['title']
    subtitle = data['subtitle']
    abstract = data['abstract']
    authors = []
    for entry in data['author']:
        authors.append( entry['name'] )

    return title, subtitle, abstract, authors

title, subtitle, abstract, authors = get_yaml_data("latex.metadata.yaml")
print (title, subtitle, abstract, authors)
