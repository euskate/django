# from django.db import models

# class Reporter(models.Model):
#     full_name = models.CharField(max_length=70)

#     def __str__(self):
#         return self.full_name

# class Article(models.Model):
#     pub_date = models.DateField()
#     headline = models.CharField(max_length=200)
#     content = models.TextField()
#     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.headline


# import random


# a = [[random.randint(0, 100) for j in range(3)] for i in range(5)]
# print(a)
# print(a[0][0])
# print(a[1][0])

import requests as rq

url = "https://pjt3591oo.github.io"

rq.post(url)
