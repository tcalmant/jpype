#!/usr/bin/python3
# *****************************************************************************
# Copyright 2004-2008 Steve Menard
#
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
# 	   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************

from jpype import startJVM, getDefaultJVMPath, JClass

startJVM(getDefaultJVMPath(),
         '-Djava.class.path=c:/tools/lucene-1.4.3/lucene-1.4.3.jar')

QueryParser = JClass("org.apache.lucene.queryParser.QueryParser")
IndexSearcher = JClass("org.apache.lucene.search.IndexSearcher")
IndexReader = JClass("org.apache.lucene.index.IndexReader")
StandardAnalyzer = JClass(
    "org.apache.lucene.analysis.standard.StandardAnalyzer")
FSDirectory = JClass("org.apache.lucene.store.FSDirectory")
IndexWriter = JClass("org.apache.lucene.index.IndexWriter")
SimpleAnalyzer = JClass("org.apache.lucene.analysis.SimpleAnalyzer")

IndexWriter('c:/temp/lucene', SimpleAnalyzer(), True).close()

directory = FSDirectory.getDirectory("c:/temp/lucene", False)
reader = IndexReader.open(directory)
searcher = IndexSearcher(reader)
queryparser = QueryParser.parse("wenger", "contents", StandardAnalyzer())
print(queryparser.rewrite)
print(queryparser.rewrite.matchReport(reader))
qp = queryparser.rewrite(reader)
print(qp)
print(searcher.search.matchReport(qp))
hits = searcher.search(qp)
