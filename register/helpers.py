def handle_uploaded_file(f):
    with open(f'/tmp/', 'x+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)