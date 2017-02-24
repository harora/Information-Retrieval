#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import numpy as np
import pickle
import re

def gettermlist():
	terms=[]
	file_data=open('words.pkl','rb')
	data=pickle.load(file_data)
	for key in data:
		terms.append(key)
	# terms=nltk.corpus.words.words()

	# print(len(terms))
	return terms

def editdistance(query_term,term): #edit distance function
	dp=[[0 for x in range(len(query_term)+1)] for x in range(1+len(term))]
	for i in range(1+len(query_term)):
		dp[0][i]=i
	for i in range(1+len(term)):
		dp[i][0]=i
	for i in range(1,1+len(term)):
		for j in range(1,1+len(query_term)):
			if term[i-1]==query_term[j-1]:
				dp[i][j]=dp[i-1][j-1]
			else:
				dp[i][j]=1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])
			# print(dp[i-1][j-1],i,j)
	return dp[len(term)][len(query_term)]


def spell_check(query_term,terms): #Applying spell check on words individually
	edit_distance=[0 for x in range(0,len(terms))]
	i=0
	for term in terms:
		edit_distance[i]=editdistance(query_term,term)
		# print(edit_distance[i],term)
		i=i+1
		
	index=-1
	min=100000

	for x in range(0,len(edit_distance)):
		word_check=0
		if abs(len(query_term)-len(terms[x]))<3:
			word_check=1
		if edit_distance[x]<min and word_check==1: 
			index=x
			min=edit_distance[x]
	idx=[]


	# print(min,terms[index])
	correct_words=[]
	if min==0:
		correct_words.append(query_term)
	else:
		for x in range(0,len(edit_distance)):
			if edit_distance[x]==min:
				idx.append(x)
		for i in idx:
			correct_words.append(terms[i])
	return correct_words



def query_spell_check(query,terms):
	words=re.compile('\w+').findall(query.lower()) #extracting words
	new_word=[]
	for wrd in words:
		probables=spell_check(wrd,terms)
		# print(probables)
		if len(probables)==1 and probables[0]==wrd:
			new_word.append(wrd)
		else:
			probables.append(wrd)
			print(probables)
			a=input("which one did you mean? \n")
			new_word.append(probables[int(a)-1])
	cquery=' '.join(word for word in new_word)
	return cquery



if __name__ == "__main__":
	terms=gettermlist()
	print(query_spell_check("Wheere is my counr?",terms)) # main function for spell check in queries