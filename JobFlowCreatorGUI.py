import urllib.request
from MyHTMLParser import MyHTMLParser
from TreeBuilder import *
from DictToJson import *
import tkinter
from tkinter import *
from tkinter.messagebox import *


class URLCreator:
    jobName = ''
    prePost = ''
    definedList = []

    def __init__(self, jobname):
        self.jobName = jobname

    def URLAppender(self):
        global jobName
        url='http://nyunix.intranet.csfb.net/db2_group/operation/operation_job_name_dependency.cfm?Job_Name='+self.jobName
        return url

    def loadUrl(self):
        content = str(urllib.request.urlopen(self.URLAppender()).read())
        return content


# End of Class URLCreator###############################################################################################################################################################################################################################################################################################################################################################

# this class creates the tree for the job dpending upon pre or post
class TreeCreator:
    masterDictionary = {}
    masterList = []
    pendingList = []
    jobName =''
    prePost = ''
    definedList=[]

    def __init__(self,jobName,preOrPost):
        self.jobName = jobName
        self.prePost = preOrPost.lower()
        self.pendingList.append(self.jobName)



    def dataFetcher(self,jobname=None):
        global masterList
        global masterDictionary
        global jobName
        global prePost
        # MEATHOD OVERLOAING
        if jobname==None:
            mydatafetcher = URLCreator(jobname=self.jobName)
        else:
            mydatafetcher = URLCreator(jobname=jobname)

        contents = mydatafetcher.loadUrl()
        parser = MyHTMLParser()
        root = parser.feed(contents)
        postdependencyList = list(set(parser.postList))
        predependencyList = list(set(parser.preList))
        # print('pre:',predependencyList)
        return predependencyList, postdependencyList


    def buildBranch(self,jobname=None):
        global masterList
        global masterDictionary
        global jobName
        global prePost
        global pendingList

        # meathod oveloading
        if jobname == None:
            if self.jobName not in self.masterList:
                predependencyList, postdependencyList = self.dataFetcher()
                self.masterList.append(self.jobName)
                if self.prePost == 'pre':
                    self.insertUnique(self.pendingList, predependencyList.copy())
                    self.masterDictionary.update({self.jobName: predependencyList})
                    return predependencyList

                elif self.prePost == 'post':
                    self.insertUnique(self.pendingList, postdependencyList.copy())
                    self.masterDictionary.update({self.jobName: postdependencyList})
                    return postdependencyList
        else:
            if jobname not in self.masterList:
                predependencyList, postdependencyList = self.dataFetcher(jobname)
                self.masterList.append(jobname)
                if self.prePost == 'pre':
                    self.insertUnique(self.pendingList,predependencyList.copy())
                    self.masterDictionary.update({jobname: predependencyList})
                    return predependencyList

                elif self.prePost == 'post':
                    self.insertUnique(self.pendingList, postdependencyList.copy())
                    self.masterDictionary.update({jobname: postdependencyList})
                    return postdependencyList



    def buildTree(self):
        global masterList
        global masterDictionary
        global jobName
        global prePost
        global pendingList
        i=0
        for job in self.pendingList:
            i+=1
            if i%1000 == 0:
                print(i,' Jobs fetched!! Have yourself a coffee! As it may take a while')
            elif i%100 == 0:
                print(i ,"Jobs fetched! please wait it's a huge flow")

            self.buildBranch(job)
            # print('for job:',job)



    def insertUnique(self,parentList,childList):
        childSet = set(childList)
        for child in childSet:
            if child not in parentList:
                parentList.append(child)

def FetchTree():
    job = e1.get().upper().strip()
    preorpost = e2.get().upper().strip()
    print(job,preorpost)
    mytree = TreeCreator(job, preorpost)

    mytree.buildTree()
    data = mytree.masterDictionary
    print(data)

    root = job
    # dictionary to json instance
    DToJ = DictToJson()
    jsonTreeStr = DToJ.jsonFromDict(data, root)
    # tree builder instance
    treeBuilder = TreeBuilder(jsonTreeStr)
    treeBuilder.buildTree()
    showinfo('Done!', 'Job Tree has been made in file JobTree.csv')

fields = ('Annual Rate', 'Number of Payments', 'Loan Principle', 'Monthly Payment', 'Remaining Loan')
master = tkinter.Tk()
master.title("Job Tree Generator")
Label(master, text='Job Name',padx=5,pady=5).grid(row=0)
Label(master, text='Pre/Post',padx=5,pady=5).grid(row=1)
e1 = Entry(master)
e2 = Entry(master)
button = Button(master,padx=5,pady=5, text = 'Create Tree',command=FetchTree )
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
button.grid(row=2,column=1)
master.mainloop()
# another comment added
