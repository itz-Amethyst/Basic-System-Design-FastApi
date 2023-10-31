def find_post(id , source):
    for p in source:
        if p['id'] == id:
            return p

def find_index_post(id, source):
    for i,p in enumerate(source):
        if p['id'] == id:
            return i