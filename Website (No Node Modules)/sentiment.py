import numpy as np
def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    return model

def cosine_distance_wordembedding_method(model, s1, s2):
    import scipy
    from scipy.spatial import distance
    vector_1 = np.mean([model[word] for word in s1.split(' ') if word in model],axis=0)
    vector_2 = np.mean([model[word] for word in s2.split(' ') if word in model],axis=0)
    cosine = distance.cosine(vector_1, vector_2)
    return round((1-cosine)*100,2)