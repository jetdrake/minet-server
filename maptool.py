from Helpers import database, mapper, figure

if __name__ == '__main__':
    db = database.db()
    
    #name = input('Enter map name: ')
    name = 'line'
    #db.GetCollectionAndWriteDocumentsToFile(name, 100)
    mp = mapper.mapper(name+'.json')
    mp.buildFigureMap()
    local = mp.getFigureMap()
    states = mp.getObservedStates()
    figure.generateHeatMap(local)
    print(local)