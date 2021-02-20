from os.path import dirname, abspath, join

from .models import Photo, Slide


def read_input_file(key):
    file_path = join(dirname(abspath(__file__)), 'input', f'{key}.txt')
    with open(file_path) as file:
        N = int(file.readline().strip('\n'))
        photos = []
        for i in range(N):
            orientation, num_tags, *tags = file.readline().strip('\n').split()
            photos.append(Photo(orientation, tags, i))

        return photos


def read_output_file(file, photos):
    stream = file.stream
    line = stream.readline().decode().strip('\n')
    N = int(line)
    slides = []
    for i in range(N):
        line = stream.readline().decode().strip('\n')
        indices = [int(x) for x in line.split()]
        slides.append(
            Slide(list(map(lambda index: photos[index], indices)))
        )

    return slides


def get_score(key, file):
    photos = read_input_file(key)
    slides = read_output_file(file, photos)
    n = len(slides)
    score = 0
    for i in range(n-1):
        s1 = slides[i].get_tags()
        s2 = slides[i+1].get_tags()
        score += min(len(s1 & s2), len(s1 - s2), len(s2 - s1))

    return score
