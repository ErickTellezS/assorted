import base64
from os import listdir, remove
from os.path import join

base_path = join('/', 'home', 'erick', 'PycharmProjects', 'Base', 'INEsIFEs', 'sample')
imgs = [f for f in listdir(base_path) if '.b64' in f]
num = 0
for img in imgs:
    num += 1
    print('Voy en archivo: ', num)
    file = join(base_path, img)
    out = join(base_path, img.replace('.b64', '.jpeg'))
    with open(file, 'r') as f:
        code = f.readline()
    imgdata = base64.b64decode(code)
    with open(out, 'wb') as f:
        f.write(imgdata)
    remove(file)
