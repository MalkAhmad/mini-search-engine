# Project README

## Overview

This project involves building a mini search engine pipeline using various technologies. The main phases include web crawling, inverted index creation, TF-IDF computation, PageRank calculation, and development of an API and a frontend interface using React.

## Phases

### 1. Web Crawling with MapReduce (Multi-Node Cluster)

#### Objective:
Download 112,000 files from the web efficiently using a MapReduce framework in a multi-node cluster environment.

#### Steps:
1. **Setup Hadoop Cluster**: Configure a multi-node Hadoop cluster.
2. **MapReduce Job for Crawling**:
   - **Mapper**: Download content and metadata.
   - **Reducer**: Prepare new input files for the next iteration.

#### Output:
- A directory in HDFS containing 112,000 downloaded files.
- A directory in HDFS containing metadata files in JSON format.
- A directory in HDFS containing neighbors files in text format.
- A directory in HDFS containing a JSON file with all downloaded links in the format <URL, FileName>.

### 2. Inverted Index and TF-IDF with MapReduce

#### Objective:
Create an inverted index and compute TF-IDF scores for the downloaded files, outputting the results in JSON format.

#### Steps:
1. **Count Words in Files MapReduce Job**:
   - **Mapper**: Tokenize text and for each word emit (fileName, one).
   - **Reducer**: Emit (fileName, sum of values) to count words.
2. **Inverted Index & TF-IDF MapReduce Job**:
   - **Mapper**: For each word in each document, emit (word, fileName).
   - **Reducer**: Calculate inverse document frequency (IDF) and combine with term frequency (TF) to produce TF-IDF scores, then emit (word, list of files sorted by TF-IDF value).

#### Output:
TF-IDF JSON Output format: `{'word': 'file1,file2,file5'}`.

### 3. Generate Backward link with (MapReduce) that use in google page rank in runtime

#### Objective:
Calculate the PageRank for each document using Google's PageRank algorithm implemented with MapReduce.

#### Steps:
1. **Backward Link MapReduce**:
   - **mapper input**: file1	url1,url2
   - **Mapper**: emit for url url_filename, filename of original page
				 ex: if url1 = file5   emit file5:file1
   - **Reducer**: emit each filename and its value equal to all backwardlinks
#### Output:
A Json file Containing key : filename and value : Backwardlinks.

### 4. API Development

#### Objective:
Create an API to serve the processed data using FastAPI.

#### Steps:
1. **Setup FastAPI**: Initialize a FastAPI project.
2. **Endpoint Implementation**:
   - `/tfidf`: Query TF-IDF scores.
   - `/Backwardlinks`: Retrieve Backwardlinks
3. **Integration**: Ensure the API can access and serve the processed data.

#### Output:
A functional API serving document data, TF-IDF scores, and google Rank values.

### 5. Frontend Development with React

#### Objective:
Develop a frontend interface to interact with the API and display the processed data.

#### Steps:
1. **Setup React App**: Initialize a React project.
2. **Component Development**:
   - **Document List**: Display a list of documents.
   - **Search Functionality**: Allow users to search based on TF-IDF scores and PageRank values.
   - **PageRank Display**: Show PageRank values.
3. **API Integration**: Connect the frontend components with the API.
4. **Styling**: Apply CSS for a clean and responsive design.

#### Output:
A React-based frontend application to interact with the API and display information to users.

## Conclusion

This project encompasses the entire data processing pipeline, from data collection to user interface. Each phase leverages different technologies and methodologies to build a robust and scalable solution. Follow the steps outlined in each phase to successfully complete the project.
