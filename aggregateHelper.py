#import pymongo
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import base64
import plotly.graph_objs as go

from blackfynn import Blackfynn
from blackfynn import Dataset
import random

# # constants
# mongohost = "localhost"
# mongoport = 27017
#
# # instantiate the mongo client
# client = pymongo.MongoClient(mongohost, mongoport)
# db = client.UH3mongo
# collection = 'dashDB'


# server = flask.Flask(__name__)
app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True
app.title = 'SPARC-DAT dashboard'


XRANGE = [513, 1293]
YRANGE = [50, 850]

colorOrder = ['rgba(31,119,180,1)', 'rgba(255,127,14,1)', 'rgba(44,160,44,1)', 'rgba(214,30,30,1)', 'rgba(148,103,189,1)','rgba(140,86,75,1)','rgba(227, 119,194,1)', 'rgba(23,190,207,1)', 'rgba(79,221,112,1)']
encodeList = []


perceptDescriptors = ["Vibration", "Flutter", "Buzz", "Urge to move", "Touch", "Pressure", "Sharp","Prick","Tap",
                                "Electric current", "Shock", "Pulsing", "Tickle", "Itch", "Tingle", "Numb", "Warm", "Cool"]

trialTypesOrder = ['Static', 'EMG', 'MagEst', 'Detection', 'Discrimination', 'AM', 'FM', 'PM', 'MultiVE']
trialTypes = {1: 'Static', 2: 'AM', 3: 'FM', 4:'PM', 5: 'MagEst', 6:'Detection', 7:'Discrimination', 15: 'MultiVE', 101: 'EMG'}



# global variables holding the blackfynn
global dcInstance
dcInstance = None
global dcDataset
dcDataset = None
global mmodels
models = {}

# RF map tab
# def getNumChans(d1, d2):
#     if d1 == 'all':
#         return len(db[collection].distinct('electrodeLabel'))
#     elif d1 == 'day':
#         return len(db[collection].find({"time": {"$regex": d2}}).distinct('electrodeLabel'))
#     # elif d1 == 'week':
#     #     res = db[collection].find({"time": {"$regex": d2}}).distinct('electrodeLabel')
#     elif d1 == 'percept':
#         return len(db[collection].find({d2: {"$exists": 1}}).distinct('electrodeLabel'))
#     elif d1 == 'electrode':
#         return 1
#
# def getNumSensations(d1,d2):
#     if d1 == 'all':
#         return db[collection].find({"numSensations": {"$ne": 0}}).count()
#     elif d1 == 'day':
#         return db[collection].find({"time": {"$regex": d2}, "numSensations": {"$ne": 0}}).count()
#     # elif d1 == 'week':
#     #   return db[collection].find({{"time": {"$regex": d2}, "numSensations": {"$ne": 0}}).count()
#     elif d1 == 'percept':
#         return db[collection].find({d2: {"$exists": 1}, "numSensations": {"$ne": 0}}).count()
#     elif d1 == 'electrode':
#         return db[collection].find({'electrodeLabel': d2}, {"numSensations": {"$ne": 0}}).count()
#
# def getNumTrials(d1,d2):
#     if d1 == 'all':
#         return db[collection].find({'trialType': {'$in':[1, 15]}}).count()
#     elif d1 == 'day':
#         return db[collection].find({'trialType': {'$in':[1, 15]}, "time": {"$regex": d2}}).count()
#     # elif d1 == 'week':
#     #   return db[collection].count()
#     elif d1 == 'percept':
#         return db[collection].find({'trialType': {'$in':[1, 15]}, d2: {"$exists": 1}}).count()
#     elif d1 == 'electrode':
#         return db[collection].find({'trialType': {'$in':[1, 15]}, 'electrodeLabel': d2}).count()
#
# def getPerceptModality(d1,d2):
#     resList = []
#
#     if d1 == 'all':
#         for iMode in perceptDescriptors:
#             resList.append(db[collection].find({"responses." + iMode: {"$exists": 1}}).count())
#     elif d1 == 'day':
#         for iMode in perceptDescriptors:
#             resList.append(db[collection].find({"time": {"$regex": d2}, "responses." + iMode: {"$exists": 1}}).count())
#     # elif d1 == 'week':
#     #   return db[collection].count()
#     elif d1 == 'percept':
#         for iMode in perceptDescriptors:
#             resList.append(db[collection].find({d2: {"$exists": 1}, "responses." + iMode: {"$exists": 1}}).count())
#     elif d1 == 'electrode':
#         for iMode in perceptDescriptors:
#             resList.append(db[collection].find({'electrodeLabel': d2, "responses." + iMode: {"$exists": 1}}).count())
#
#     return resList
#
# def getPerceptLocation(d1,d2):
#     resList = []
#
#     if d1 == 'all':
#         for iLoc in imgName:
#             resList.append(db[collection].find({iLoc: {"$exists": 1}}).count())
#     elif d1 == 'day':
#         for iLoc in imgName:
#             resList.append(db[collection].find({"time": {"$regex": d2}, iLoc: {"$exists": 1}}).count())
#     # elif d1 == 'week':
#     #   return db[collection].count()
#     elif d1 == 'percept':
#         for iLoc in imgName:
#             resList.append(db[collection].find({d2: {"$exists": 1}, iLoc: {"$exists": 1}}).count())
#     elif d1 == 'electrode':
#         for iLoc in imgName:
#             resList.append(db[collection].find({'electrodeLabel': d2, iLoc: {"$exists": 1}}).count())
#
#     return resList
#
# def getPixelCoords(d1,d2, img):
#     resList = {}
#     tmp = []
#     if d1 == 'all':
#         tmp = db[collection].find({img: {"$exists": 1, "$ne": []}}, {img: 1, '_id': 0})
#     elif d1 == 'day':
#         tmp = db[collection].find({"time": {"$regex": d2}, img: {"$exists": 1, "$ne": []}},{img: 1, '_id': 0})
#     # elif d1 == 'week':
#     #   return db[collection].count()
#     elif d1 == 'percept':
#         tmp = db[collection].find({d2: {"$exists": 1}, img: {"$exists": 1, "$ne": []}},{img: 1, '_id': 0})
#     elif d1 == 'electrode':
#         tmp = db[collection].find({'electrodeLabel': d2, img: {"$exists": 1, "$ne": []}},{img: 1, '_id': 0})
#     elif d1 == 'trial':
#         tmp = db[collection].find({'trial': d2, img: {"$exists": 1, "$ne": []}}, {img: 1, '_id': 0})
#
#     # mask = np.zeros([YRANGE[1], XRANGE[1], ])
#     for iLine in tmp:               # trial
#         for ix in iLine[img]:       # lines per trial
#             resList.setdefault(img, []).append(ix)
#     #     imgMask = Image.new('L', (XRANGE[1], YRANGE[1]), 0)
#     #     ImageDraw.Draw(imgMask).polygon(iLine[img][0], outline=1, fill=1)
#     #     mask += np.array(imgMask)
#     # resList[img] = mask
#     return resList
#
# def createDropDownList(inputList):
#     outList = []
#     for x in inputList:
#         outList.append({'label': x, 'value': x})
#
#     if not outList:
#         outList = [{'label':'n/a', 'value':'n/a'}]
#
#     return sorted(outList)
#
# def populateD2(d1):
#     res1 = []
#     if d1 == 'all':
#         res1 = []
#     elif d1 == 'day':
#         tmp = db[collection].distinct('time')
#         res1 = list(set([x.split(' ')[0] for x in tmp]))
#     # elif d1 == 'week':
#     #     res1 = db[collection].distinct('time')
#     elif d1 == 'percept':
#         res1 = imgName
#     elif d1 == 'electrode':
#         res1 = db[collection].distinct('electrodeLabel')
#
#     res = list(reversed(createDropDownList(res1)))
#     return res


# # Static Trial log tab
# def getSurfaceResponses(trialName):
#     return db[collection].find({'trial': trialName},{'responses': 1, '_id': 0})[0]
#
# def getDataTableDictList():
#     res = db.command({
#         'aggregate': collection,
#         'pipeline': [
#             {'$match': {
#                 "trialType": {'$in':[1,15]}
#             }},
#             {"$project": {
#                 "_id": 1,
#                 "trialName": "$trial",
#                 "elec": "$electrodeLabel",
#                 "amp": "$stimParams.cathAmp",
#                 "freq": "$stimParams.freq",
#                 "PW": "$stimParams.width",
#                 "time":"$time",
#             }}]})
#
#     dictList = []
#     for x in res['result']:
#         dictList.append({'Trial': x['trialName'], 'Electrode': x['elec'], 'Amp (uA)': x['amp'], 'PW (usec)': x['PW'], 'Freq (Hz)': x['freq'], 'Timestamp': x['time']})
#
#     return dictList
#
#
# # Psychophysics tab
# def getPsychoElecList():
#     res = db[collection].find({'trialType':{"$in":[5,6,7]}}).distinct('electrodeLabel')
#     return createDropDownList(res)
#
# def getPsychTrialsList(elec, varyingParam, trialType):
#     trialList = db[collection].find({'trialType': trialType, 'electrodeLabel': elec,'varyingParameterType':varyingParam}, {'_id': 0, 'trial': 1})
#     outList = []
#     for i in trialList:
#         outList.append('_'.join(i['trial'].split('_')[1:3]))
#     return list(set(outList))
#
# def getPsychoData(elec, trialtype, param, setNum):
#     res2 = db.command({
#         'aggregate': collection,
#         'pipeline': [
#             {"$match":{
#                 "trialType":trialtype,
#                 "trial":{"$regex":setNum},
#                 'varyingParameterType':param,
#                 "electrodeLabel":elec
#             }},
#             {"$group": {
#                 "_id": {"elec": "$electrodeLabel","param": {"$abs":{"$subtract":['$val_interval1','$val_interval2']}}},     # , "userAnswer": "$userAnswer", "correctAnswer":"$correctAnswer",
#                 "numCorrect": {"$sum": {"$cond":[{"$eq":['$userAnswer','$correctAnswer']},1,0]}},
#                 "count": {"$sum":1}
#             }},
#             {"$project": {
#                 "_id": 0,
#                 'absDiff': '$_id.param',
#                 "percentCorrect": {"$divide":["$numCorrect", "$count"]}
#             }}
#     ]})
#     return res2['result']
#
# def getDiscrimReferenceVal(setNum):
#     res = db[collection].find({'trialType':7,'trial': {"$regex": setNum}},{'_id':0,'val_interval1':1,'val_interval2':1})
#     if res.count():
#         res1 = [res[0][i] for i in res[0].keys()]
#         if res.count() > 2:
#             res2 = [res[2][i] for i in res[2].keys()]
#         else:
#             res2 = [res[1][i] for i in res[1].keys()]
#         refVal = (res[1][j] for j in res[1].keys() if res[1][j] in res1 and res[1][j] in res2).next()
#         return refVal
#
# def getMagEstTrialsList(elec, varyingParam):
#     trialList = db[collection].find({'trialType': 5, 'electrodeLabel': elec, 'varyingParameterType':varyingParam}, {'_id': 0, 'trial': 1})
#     outList = []
#     for i in trialList:
#         outList.append('_'.join(i['trial'].split('_')[1:3]))
#     return list(set(outList))
#
# def getMagEstData(elec, setNum, varyingParam):
#     res2 = db.command({
#         'aggregate': collection,
#         'pipeline': [
#             {"$match": {
#                 "trialType": 5,
#                 "trial": {"$regex": setNum},
#                 "electrodeLabel": elec,
#                 'varyingParameterType': varyingParam,
#             }},
#             {"$project": {
#                 "_id": 0,
#                 'probeVal': '$varyingParameterVal',
#                 "response": '$reportedMag'
#             }}
#         ]})
#     return res2['result']
#
#
# # Trial counts tab
# def getNumTrialTypesPerElec():
#     res2 = db.command({
#         'aggregate': collection,
#         'pipeline': [
#             {"$group": {
#                 "_id": {"elec": "$electrodeLabel", "type": "$trialType"},
#                 "count": {"$sum": 1}
#             }},
#             {"$project": {
#                 "_id": 0,
#                 'trialtype': '$_id.type',
#                 'elec': '$_id.elec',
#                 "count": "$count"
#             }}]})
#
#     resultDict = {}
#     for iRes in res2['result']:
#         resultDict.setdefault(iRes['elec'],{})
#         resultDict[iRes['elec']][iRes['trialtype']] = iRes['count']
#
#     return resultDict
#
# def trialTypeCountTemplate(imgIdx):
#
#     return html.Div(
#         [
#             dcc.Graph(
#                 id=str(imgIdx),
#                 style={"height": "60%", "width": "98%"},
#                 config= dict(displayModeBar=False),
#                 figure={
#                     'data': [go.Bar(x=[1,2,3,4,5], y = [9,4,5,6,7],showlegend=False)],
#                     'layout': {
#                         'xaxis': {
#                             'fixedrange': True,
#                     #         # 'range': XRANGE,
#                     #         # 'ticklen': 0,
#                     #         # 'showgrid': False,
#                     #         # 'zeroline': False,
#                     #         # 'showline': False,
#                     #         # 'ticks': '',
#                     #         # 'showticklabels': False
#                         },
#                         'yaxis': {
#                             'fixedrange':True,
#                             # 'range': YRANGE,
#                     #         # 'ticklen': 0,
#                     #         # 'showgrid': False,
#                     #         # 'zeroline': False,
#                     #         # 'showline': False,
#                     #         # 'ticks': '',
#                     #         # 'showticklabels': False
#                         },
#                         'showlegend': False,
#                         'margin':{'t':0,'b': 0, 'l':0, 'r':0},
#                     }
#                 },
#             ),
#         ],
#         style={'width': '12.0625%','marginBottom':'1%'},
#         className="eight columns chart_div"
#
#     )
#
#
# # P-space tab
# def loadAllParams(electrode):
#     res1 = db.command({
#             'aggregate' : collection,
#             'pipeline' : [
#               {'$match' : {
#                  "trialType":1,
#                   "electrodeLabel": electrode
#                   }},
#               {"$project": {
#                       "_id": 0,
#                       "amp": "$stimParams.cathAmp",
#                       "freq": "$stimParams.freq",
#                       "PW": "$stimParams.width",
#                     }}]})
#
#     return res1['result']
#
#
# # misc helpers
# def getAllChans():
#     return db[collection].distinct('electrodeLabel')
#
def indicator(color, text, id_value, val):
    return html.Div(
        [

            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id=id_value,
                children = val,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
    )
#
def getRFtemplate(imgIdx,appendStr=''):
    return html.Div(
        [
#             dcc.Graph(
#                 id=imgName[imgIdx]+'_'+appendStr,
#                 style={"height": "90%", "width": "98%"},
#                 config= dict(displayModeBar=False),
#                 figure= {'data': [go.Scatter(x=[], y=[])],
#             'layout': {
#                 'xaxis': {
#                     'fixedrange': True,
#                     'range': XRANGE,
#                     'ticklen': 0,
#                     'showgrid': False,
#                     'zeroline': False,
#                     'showline': False,
#                     'ticks': '',
#                     'showticklabels': False
#                 },
#                 'yaxis': {
#                     'fixedrange':True,
#                     'range': YRANGE,
#                     'ticklen': 0,
#                     'showgrid': False,
#                     'zeroline': False,
#                     'showline': False,
#                     'ticks': '',
#                     'showticklabels': False
#                 },
#                 'showlegend': False,
#                 'margin':{'t':0,'b': 0, 'l':0, 'r':0},
#                 'images': [{
#                     'xref': 'x',
#                     'yref': 'y',
#                     'x': XRANGE[0],
#                     'y': YRANGE[0],
#                     'yanchor': 'bottom',
#                     'sizex': XRANGE[1] - XRANGE[0],
#                     'sizey': YRANGE[1] - YRANGE[0],
#                     'sizing': 'stretch',
#                     'layer': 'above',
#                     'source': 'data:image/png;base64,{}'.format(encodeList[imgIdx])
#                 }],
#             }
#         },
#             ),
        ],
        style={'width': '16.25%','marginBottom':'1%'},
        className="six columns chart_div"

    )




def instantiateDatCore():
    '''
    instantiate a dat core object if not already done
    :return: handle to the dat core object
    '''
    # we are going to store the instance as a global
    # so we can access it from everywhere
    global dcInstance
    # check if we already have the dat core instance or not
    if not isinstance(dcInstance,Blackfynn):
        dcInstance = Blackfynn()
    # return the dcInstance
    return dcInstance
instantiateDatCore()

def getDatasets():
    '''
    return a list of the datasets on dat core
    :return: dictionary with datasets info
        key   = dat core id
        value = dataset name
    '''
    global dcInstance
    # get all the datasets from dat core
    lDatasets = dcInstance.datasets()
    # refactor them in jason
    dDatasets = [{"label": item.name, 'value':item.id}  for item in lDatasets]
    # for item in lDatasets:
    #     datasetList.append({"label":iKey, 'value':bfDatasetDict[iKey]})

    return dDatasets

def getDataset(id_or_name):
    '''
    retrieve the dat core object for the selected dataset
    :param id_or_name: dat core id or name of the dataset
    :return: data core dataset object
    '''
    global dcInstance
    global dcDataset
    if id_or_name:
        # set relaod flag to true
        reload = True
        # check if we need to reload
        if isinstance(dcDataset,Dataset) and \
            ( dcDataset.id == id_or_name or \
              dcDataset.name == id_or_name ):
            reload = False
        # reload if it needs to
        if reload:
            dcDataset = dcInstance.get_dataset(id_or_name)
        # return dataset object

    return dcDataset


def getModelsNames():
    '''
    return the models present in the dataset
    :return: dictionary with dat core id and name of the models
        key = dat core id
        value = model name
    '''
    global dcDataset
    # retrieve models from dat core
    hModels = dcDataset.models()
    # re arrange in the format that we need
    jsonModelNames = [{'label': key + "(" + str(item.count) +")", 'value': "M:model:"+item.id } for key, item in hModels.items()]
    return jsonModelNames

def getModelsInfo():
    '''
    return the models present in the dataset with all their properties
    :return: dictionary with dat core id and name of the models
        key = dat core id
        value = model name and properties
    '''
    global dcDataset
    # retrieve models from dat core
    hModels = dcDataset.models()
    # loop on models and builds a dictioknary with model name, id and properties
    jsonModelsInfo = {}
    for mName, mObject in hModels.items():
        jsonModelsInfo[mObject.id] = {
            'name': mName,
            'properties': {
                'P:' + mName + ':' + pObject.id: {
                    'name': pObject.name,
                    'type': pObject.type}
                for pName, pObject
                in mObject.schema.items()}
        }
    return jsonModelsInfo

def getModel(id_or_name):
    '''
    return the dat core model object
    :param id_or_name: dat core id or model name
    :return: model object
    '''
    global dcDataset
    global models
    # check if we need to load the model or not
    if id_or_name in models.keys():
        # model already loaded
        mObject = models[id_or_name]
    else:
        # simplify id is it is a composite one
        id_or_name = id_or_name.split(':')[-1]
        # get tobject model
        mObject = dcDataset.get_model(id_or_name)
        # save model in cache
        models[mObject.display_name] = mObject
        models['M:model:' + mObject.id] = mObject
    return mObject


def getRecord(recordId):
    '''

    :param recordId:
    :return:
    '''
    # I assume that the record is in the following format M:<model_name>:<dat_cor_id>
    [temp1,modelName,recId] = recordId.split(':')
    # get model
    mObject = getModel(modelName)
    # retrieve record
    record = mObject.get(recId)
    return record

def getDcId(record):
    '''

    :param record:
    :return:
    '''
    return 'R:'+record.type+':'+record.id


def getObjectNeighbours(centerObjectIdName,numberOfObjects=100,numberOfLevels=2):
    '''
    this function retrieves the list of objects that are in the neighbour of the requested object
    :param centerObjectIdName: name or id of the central object
    :return: dictionary with list of nodes and relationships
    '''
    # retrieve record for center object
    record = getRecord(centerObjectIdName)
    # initialize counter and output structure
    recCounter = 1
    visStruct = {
        'nodes' : {},
        'links' : []
    }
    # build the list
    [visStruct,temp1,temp2] = _buildNeighbourhood(visStruct,record,numberOfObjects,numberOfLevels)
    # repackage for iGraph
    recordToIndex = {}
    outVisStruct = {
        'nodes' : [],
        'links' : []
    }
    counter = 0
    for key, item in visStruct['nodes'].items():
        outVisStruct['nodes'].append(item)
        recordToIndex[key] = counter
        counter += 1
    for item in visStruct['links']:
        outVisStruct['links'].append({
            'source' : recordToIndex[item['source']],
            'target' : recordToIndex[item['target']]
        })

    return visStruct


def _buildNeighbourhood(visStruct,sRec,oCounter,lCounter):
    '''

    :param sRec:
    :param oCounter:
    :return:
    '''
    global dcDataset
    # full record id
    sDcId = getDcId(sRec)
    visStruct = {}
    visStruct['nodes'] = []
    visStruct['links'] = []
    # add this record to the visualization list
    visStruct['nodes']{sDcId} = {
        'dcId': sDcId,
        'Name': sRec.type + ' ' + sRec.id,
        'type': sRec.type
    }
    # get all the related nodes through a relationship
    linkedRecords = sRec.get_related()
    # se if we need to select a subset
    linkedRecordsToBeShown = linkedRecords
    if oCounter < len(linkedRecords):
        linkedRecordsToBeShown = random.sample(linkedRecords, oCounter)

    # add related record to list
    for dRec in linkedRecordsToBeShown:
        dDcId = getDcId(dRec)
        visStruct['nodes'][dDcId] = {
            'dcId': dDcId,
            'Name': dRec.type + ' ' + dRec.id,
            'type': dRec.type
        }
        visStruct['links'].append(
            {
                'source': sDcId,
                'target': dDcId
            }
        )

    # update counter
    oCounter -= len(linkedRecordsToBeShown)
    lCounter -= 1
    if oCounter > 0 and lCounter > 1:
        # add related record to list
        for dRec in linkedRecordsToBeShown:
            [visStruct,oCounter,lCounter] = _buildNeighbourhood(visStruct,dRec,oCounter,lCounter)

    return visStruct,oCounter,lCounter

