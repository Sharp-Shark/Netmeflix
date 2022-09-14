import os

try :
    datas = {}
    movies = os.listdir('movies/')
    moviePaths = movies.copy()
    for movieIndex, movie in enumerate(movies) :
        with open('movies/'+movie, 'r') as file :
            movies[movieIndex] = file.read()
        data = {}
        name = ''
        build = ''
        state = 'name'
        for char in movies[movieIndex] :
            if char == '{' :
                name = build
                data[name] = ''
                state = 'property'
                build = ''
            elif char == '}' :
                data[name] = build
                state = 'name'
                build = ''
                name = ''
            else :
                if state == 'property' or char != '\n' :
                    build = build + char
        datas[moviePaths[movieIndex]] = data
        with open(data['template'], 'r') as template :
            movieHTML = movie.split('.')[0]+'.html'
            with open('website/'+movieHTML, 'w') as file :
                finished = template.read()
                for name in list(data.keys()) :
                    finished = finished.replace('{'+name+'}', data[name])
                print(finished)
                file.write(finished)

    #templateLink = '<a href="{path}" target="_blank"><img src="{img}" height="400px"/></a>'
    templateLink = '''
    <a href="{path}">
        <img src="{img}" height="400px" width="300px" style="margin: 8px;" />
    </a>
    '''
    movieDisplay = ''
    for pathIndex, path in enumerate(moviePaths) :
        if datas[path]['template'] == 'sourceTemplate.html' :
            continue
        movieLink = templateLink
        movieLink = movieLink.replace('{path}', path.split('.')[0]+'.html')
        for name in list(datas[path].keys()) :
            movieLink = movieLink.replace('{'+name+'}', datas[path][name])
        movieDisplay = movieDisplay + movieLink
    with open('mainTemplate.html', 'r') as templateMain :
        with open('website/main.html', 'w') as websiteMain :
            websiteMain.write(templateMain.read().replace('{movies}', movieDisplay))

    os.system('start website/main.html')
except Exception as error :
    input(error)