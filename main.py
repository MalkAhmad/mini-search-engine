from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

with open("invertedIndexTFIDF.json", encoding='utf-8') as f:
    inverted_index_json = json.load(f)

with open("BackwardLink.json" , encoding='utf-8') as f:
    BackwardJson = json.load(f)

with open("MetaData.json", "r" , encoding ="utf-8") as file:
    MetaData= json.load(file)

with open("googleRankResult.json", "r" , encoding ="utf-8") as file:
    GooglePageRank_json = json.load(file)
    
def getMetaData(filename):
    MetaDatas = MetaData[filename].split(':$@%:')
    return MetaDatas[1] , MetaDatas[3] , MetaDatas[5]
    
TempDicForGooglePageRank={}

def GetFilesFromInvertedIndex ( key ):
    
    list_files = []
    
    files = inverted_index_json[key] 
    files = files.split(',')

    return files

def ExtractBackward_GetInitialPr(files_list):
    
        
    parents = {}
    FilterBackward = {}
    
    for file in files_list : 
        temp_list = []
        if file in BackwardJson :
            
            back = BackwardJson[file]
            files = back.split(",")
            
            
            for backFile in files : 
                if backFile in files_list :
                    
                    if backFile in parents : 
                        parents [backFile][0] += 1
                    else :
                        parents [backFile] = [1,1/len(files_list)]
                        
                    temp_list .append (backFile)
                    
#             if len(temp_list) :
        FilterBackward [file] = temp_list
    
    for file in files_list : 
        
        if file not in parents :
            parents [file] = [1,1/len(files_list)]
            
    
    return FilterBackward , parents
        
        

def update_PR (filteredBackward , initial_pr_json ):
        
    dictionary_newPr = {}
    
    for key , value in filteredBackward .items():
        
        if len(value) == 0 :
            if key in initial_pr_json :
                dictionary_newPr[key] = initial_pr_json[key]
            continue
        #---------------------------------------------
        
        
        for file in value : 
            
            if file in initial_pr_json : 
                
                count , pr = initial_pr_json[file]
                new_pr = pr/count 
                
                if key in dictionary_newPr :
                    dictionary_newPr[key][1] += new_pr
                
                else :
                    dictionary_newPr[key] = [count , new_pr]
    
    
    
    return dictionary_newPr 
                    
        

def GetPageRank(files_list) : 
    
    FilterBackward , initial_pr = ExtractBackward_GetInitialPr(files_list)
    
    new_pr = update_PR ( FilterBackward , initial_pr )
    
    for i in range(30) : 
        new_pr = update_PR ( FilterBackward , new_pr )
    
    sorted_keys = sorted(new_pr, key=lambda k: new_pr[k][1], reverse=True)
    
    return sorted_keys

app = FastAPI()

# Enable CORS for all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/TFIDF/{word}")
async def getTfidfRank(word: str):
    word = word.lower()
    
    if word not in inverted_index_json:
        return [{"NOT FOUND"}]  # Return a list with a single object

    Files_list_TF_IDF = GetFilesFromInvertedIndex(word)
    
    TF_IDF_Rank = []

    for file in Files_list_TF_IDF:
        URL, title, description = getMetaData(file)
        TF_IDF_Rank.append({"Title": title, "URL": URL, "Description": description})

    return TF_IDF_Rank

@app.get("/googleRank/{word}")
async def getGoogleRank(word: str):
    global GooglePageRank_json
    global TempDicForGooglePageRank
    word = word.lower()
    
    if word in TempDicForGooglePageRank:
        return TempDicForGooglePageRank[word]
    
    if word in GooglePageRank_json:
        return GooglePageRank_json[word]
    
    
    if word not in inverted_index_json:
        return [{"NOT FOUND"}]  # Return a list with a single object

    Files_list_TF_IDF = GetFilesFromInvertedIndex(word)
    Files_list_GR = GetPageRank(Files_list_TF_IDF)
    
    GR_Rank = []

    for file in Files_list_GR:
        URL, title, description = getMetaData(file)
        GR_Rank.append({"Title": title, "URL": URL, "Description": description})
    
    
    TempDicForGooglePageRank[word] = GR_Rank
    
    if len(TempDicForGooglePageRank) > 2:
        New_Dict = {**GooglePageRank_json,**TempDicForGooglePageRank}
        with open('googleRankResult.json', 'w') as file:
            json.dump(New_Dict, file, indent=4)
            
        with open("googleRankResult.json", "r" , encoding ="utf-8") as file:
            GooglePageRank_json = json.load(file)
            
        TempDicForGooglePageRank = {}
    
    
    return GR_Rank