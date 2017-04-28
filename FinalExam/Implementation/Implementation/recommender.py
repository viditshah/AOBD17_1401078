'''
 Code for  Skill Recommended system in python
 AOBD final paper
 Vidit Shah
 Roll No. 1401078
'''

import codecs 
from math import sqrt


class recommender:
    def __init__(self, data, k=1, metric='pearson', n=5):
        """ initialize recommender
        currently, if data is dictionary the recommender is initialized
        to it.
        For all other data types of data, no initialization occurs
        k is the k value for k nearest neighbor
        metric is which distance formula to use
        n is the maximum number of recommendations to make"""
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        # for some reason I want to save the name of the metric
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        #
        # if data is dictionary set recommender data to it
        #
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):
        """Given product id number return product name"""
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id
    def userfunction(self, id, n):
        """Return n top ratings for user with id"""
        print ("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v)
                   for (k, v) in ratings]
        # finally sort and return
        ratings.sort(key=lambda artistTuple: artistTuple[1],
                     reverse = True)
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator


    def computeNearestNeighbor(self, username):
        """creates a sorted list of users based on their distance to
        username"""
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],
                                   self.data[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        return distances

    def recommend(self, user):
       """Give list of recommendations"""
       recommendations = {}
       # first get list of users  ordered by nearness
       nearest = self.computeNearestNeighbor(user)
       #
       # now get the ratings for the user
       #
       userfunction = self.data[user]
       #
       # determine the total distance
       totalDistance = 0.0
       for i in range(self.k):
          totalDistance += nearest[i][1]
       # now iterate through the k nearest neighbors
       # accumulating their ratings
       for i in range(self.k):
          # compute slice of pie 
          weight = nearest[i][1] / totalDistance
          # get the name of the person
          name = nearest[i][0]
          # get the ratings for this person
          neighborRatings = self.data[name]
          # get the name of the person
          # now find bands neighbor rated that user didn't
          for artist in neighborRatings:
             if not artist in userfunction:
                if artist not in recommendations:
                   recommendations[artist] = (neighborRatings[artist]
                                              * weight)
                else:
                   recommendations[artist] = (recommendations[artist]
                                              + neighborRatings[artist]
                                              * weight)
       # now make list from dictionary
       recommendations = list(recommendations.items())
       recommendations = [(self.convertProductID2name(k), v)
                          for (k, v) in recommendations]
       # finally sort and return
       recommendations.sort(key=lambda artistTuple: artistTuple[1],
                            reverse = True)
       # Return the first n items
       
       return recommendations[:self.n]

	   

users = {"0": {"C#": 2.5,
                      "Office": 3.0, "jboss": 3.0,
                      "C++": 3.5,
                      "C": 2.5 },
         
         "2":{"C#": 2.0, "Matlab": 3.5,
                 "Hadoop": 3.5,
                 "C++": 3.5, "Python": 3.0,"MongoDB": 1.5},

         "4":{"Mapreduce": 2.0, "Bash": 3.5,
                 "Office": 4.0,
                 "Java": 3.5, "jboss": 5.0,"Shell": 4.0},

         "6": {"C#": 1.5,
                      "Hadoop": 3.0, "Ruby": 2.0,
                      "C++":2.5,
                      "C": 2.5,"Scripting": 3.5},
		 "8": {"Mapreduce": 2.0,
                      "Hadoop": 4.0, "Python": 2.0,
                      "C++": 3.5,
                      "C": 2.5,"JIRA": 2.0},
         
         "9":{"C#": 2.0, "Matlab": 3.5,
                 "Office": 3.0,
                 "Java": 3.5, "jboss": 3.0,"MongoDB": 3.5},

         "13":{"Mapreduce": 2.0, "Bash": 3.5,
                 "Hadoop": 1.5,
                 "C++": 3.5, "Python": 5.0,"Shell": 4.0},

         "16": {"C#": 2.0,
                      "Office": 2.0, "Ruby": 3.0,
                      "C++": 2.5,
                      "C": 1.5,"Scripting": 2.0},
		 "19": {"Mapreduce": 2.0,
                      "Office": 4.0, "jboss": 5.0,
                      "Java": 3.5,
                      "C": 2.5,"Git": 3.0},
         
         "21":{"Mapreduce": 2.0, "Matlab": 3.5,
                 "Office": 4.0,
                 "C++": 3.5, "Python": 3.0,"MongoDB": 5.0},

         "24":{"C#": 2.0, "Bash": 3.5,
                 "Hadoop": 2.5,
                 "C++": 3.5, "Python": 5.0,"Shell": 3.0},

         "26": {"Mapreduce": 3.0,
                      "Office": 2.0, "Ruby": 5.0,
                      "Java": 2.5,
                      "C": 1.5,"MongoDB": 2.0},
					  
		 "30": {"C#": 2.0,
                      "Hadoop": 3.5, "Python": 2.0,
                      "C++": 3.5,
                      "C": 2.5,"jboss": 2.0},
         
         "32":{"Mapreduce": 2.0, "Matlab": 3.5,
                 "Hadoop": 4.0,
                 "Java": 3.5, "Python": 3.0,"MongoDB": 5.0},

         "44":{"C#": 2.0, "Bash": 3.5,
                 "Office": 4.0,
                 "C++": 3.5, "Python": 5.0,"Shell": 4.0},
         
        }

