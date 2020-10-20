import KekApi as kek

if __name__ == "__main__":

    a = kek.article(515636)
    
    if a['status'] == 'ok':
        print(a)
