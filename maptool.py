from Helpers import database, mapper, figure
import csv
import sys


if __name__ == '__main__':
    name = None
    for i, arg in enumerate(sys.argv):
        if i == 1:
            name = arg
    
    '''
    error = [[]]
    with open('Data/heatmap/exp2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for row in csv_reader:
            error[0].append(float(row[0]))
    print(error)
    '''

    db = database.db()
    
    if name is None:
        name = input('Enter map name: ')
    #name = 'exp2'
    db.GetCollectionAndWriteDocumentsToFile(name, 100)
    mp = mapper.mapper(name)
    '''
    mop = mp.Map

    counter = 0
    for row in range(len(mop)):
        for col in range(len(mop[0])):
            if mop[row][col] > 0:
                mop[row][col] = error[0][counter]
                counter += 1
            else:
                mop[row][col] = -1

    '''
    mp.buildFigureMap()
    local = mp.getFigureMap()
    #print(mop)
    states = mp.getObservedStates()
    figure.generateHeatMap(local)
    #print(mp.getMap())
    print(local)
    mean, std, minT, maxT = mp.getMeanAndStandardDeviation()
    print('mean: ', mean, 'std: ', std, 'min: ', minT, 'max: ', maxT)
    