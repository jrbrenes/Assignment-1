# Assignment-1
DE 300 HW 1
Juan Brenes

This repository consists of 

To run the files in a container, I inputed the following commands into terminal in the directory that contained my files:

#### To create the container
docker build --no-cache -t assignment-1 .

#### To run the code in the container
docker run -v "$(pwd)/data:/tmp/data" -it assignment-1:latest

### About the script and its outputs
It should outptut a data file with the transformed csv file. The python script 'Assignment 1' was originally a jupyter notebook, as it was a more convenient way of debugging as well as saving the output. The cells were copied and pasted into the current python script, along with the pseudocode for each underlying block of code. The script uses no functions, and it prints the output directly. The script should output charts for all of the required features, as well as save the transformed dataframe into a csv. The output of the cells was saved separately and will be contained in this readme file, as well as the discussion regarding the output.

## Question 1
This part was addressed in the code

## Question 2
Here are the outputs of the graphs from the non-normalized numerical features:

![Figure_1](https://user-images.githubusercontent.com/98558551/233455951-94503904-fc97-4fae-b00d-37593db69b5e.png)
![Figure_2](https://user-images.githubusercontent.com/98558551/233455969-f4d4b1e1-2cee-4c30-938a-cd35572041b4.png)
![Figure_3](https://user-images.githubusercontent.com/98![Figure_4](https://user-
![Figure_4](https://user-images.githubusercontent.com/98558551/233456042-8d64482e-1b44-4522-9192-3ef834f94b70.png)
![Figure_5](https://user-images.githubusercontent.com/98558551/233456053-8c3cd818-1849-4005-b1e4-b12793ef0087.png)
![Figure_6](https://user-images.githubusercontent.com/98558551/233456072-51e9f4f7-750b-4962-b1e5-572fa9a4f4cd.png)
![Figure_7](https://user-images.githubusercontent.com/98558551/233456084-0164c442-a9fe-41fd-a816-f118a9ec143f.png)
![Figure_8](https://user-images.githubusercontent.com/98558551/233456096-8ad3c0d8-2bda-4c2a-b69a-2bc1c971ec88.png)
![Figure_9](https://user-images.githubusercontent.com/98558551/233456144-46e82545-ca08-4ceb-9aed-5f6f0144a3af.png)
![Figure_10](https://user-images.githubusercontent.com/98558551/233456163-73b2a585-9e3a-42e2-ab35-b224d8cdf850.png)

Many of this variables are very skewed, and the code checked for features with a skewness over 1 or lesser than -1. Here is the skewness of the numerical features:


TARGET                        3.078365

CNT_CHILDREN                  2.330726

CNT_FAM_MEMBERS               1.148404

AMT_INCOME_TOTAL              7.245098

AMT_CREDIT                    1.199083

DAYS_EMPLOYED                 2.050958

DAYS_BIRTH                    0.115488

EXT_SOURCE_2                 -0.797461

EXT_SOURCE_3                 -0.465799

AMT_REQ_CREDIT_BUREAU_YEAR    1.354335

The 7 features that failed the skewness check where transformed and stored in the csv file: 'transformed_data.csv'
It is also important that TARGET is a binary feature where a vast majority of rows = 0, hence the skewness. This will matter when filtering for outliers.

## Question 3
Here are the boxplots for the seven features:
![Figure_11](https://user-images.githubusercontent.com/98558551/233457597-c49b08b2-e409-403e-acd4-d6c9501cbd9e.png)
![Figure_13](https://user-images.githubusercontent.com/98558551/233457626-78b16119-6e37-457b-baa0-d99b4a6f1791.png)
![Figure_14](https://user-images.githubusercontent.com/98558551/233457917-f1e00418-62dc-4ce2-a43e-f6755da781cb.png)
![Figure_15](https://user-images.githubusercontent.com/98558551/233457918-b5c5432c-d97e-4051-933c-29725e862b95.png)
![Figure_16](https://user-images.githubusercontent.com/98558551/233457920-532743f7-5fac-4592-bb0b-b5e96f580a2b.png)
![Figure_17](https://user-images.githubusercontent.com/98558551/233457950-ab6ccb18-9285-428c-bc98-c286d2bf2161.png)
![Figure_18](https://user-images.githubusercontent.com/98558551/233457951-265651af-6df1-4555-a782-44b2864082bf.png)

In the code, I tried multiple ways of removing outliers, the first of which was through standard deviations, but that removed way too many rows. I settled with clustering with the DBSCAN algorithm from scikit.learn to do the clustering for each feature. It removed very outliers to a degree I was comfortable with. This is also the longest chunk of code in terms of processng time, clocking at 2m23s in my jupyter notebook, but it did its job well.

Here is the boxplots for both values of TARGET
<img width="1123" alt="Figure19" src="https://user-images.githubusercontent.com/98558551/233461565-14541f98-944f-4c08-be46-261d601a6308.png">


There are not significant differences in children counts and family members.
For amount income total, there are more prevalent outliers in amount total income when TARGET=0 than when TARGET=1
For amount of credit and days employed, the boxplots of TARGET=0 covered a wider range than TARGET=1, as well as having more extreme outliers than TARGET=1.

Now looking at transformed amount of total income by education level:
![Figure_20](https://user-images.githubusercontent.com/98558551/233459642-ee6bc5fe-b20b-43f3-a004-a1cb540e119e.png)
Zoomed out view:
<img width="1027" alt="Screen Shot 2023-04-20 at 2 00 31 PM" src="https://user-images.githubusercontent.com/98558551/233462346-27ae9636-c6e6-4598-b56d-a2b562b69a0e.png">

The percentiles grow wider as the education level rises. All groups have outliers, with secondary and higher education holders havingthe highest concentratons of them. The outliers drift further from the mean for education types that have been completed.

## Question 4
Here are the barplots regarding counts by housing type and of housing type by family status respectively:
![Figure_21](https://user-images.githubusercontent.com/98558551/233462814-96a7727b-6f9d-4240-957a-fee6b54698fa.png)

The overwhelming majority of users own a house or apartment, with very small minorities liviing with their parents or in municipal homes. It is very surprising however, that rented apartments are too low, but the next figure gives us more context on that.

![Figure_22](https://user-images.githubusercontent.com/98558551/233462835-417e73c2-6367-42dd-b4cb-2a1e3c8d47c1.png)

Now that we see the distributions by family status,of those home/apartment owners the vast majority are married, followed by single people and people in civil marriage. As a matter of fact, married people are the largest family status group for each housing type. This dataset is heavliy slanted towards marreid people, and to be able to draw a better insight into the housing types that people with different family statuses have would require more diverse data.

## Question 5
Steps a and b were done in the code, and the output for both target types is the following. The two chunks of code that plot the graphs take a while to run, as the code calculates the proportions as it is plotting.

![Figure_23](https://user-images.githubusercontent.com/98558551/233464120-8b600a8f-51b0-4742-a851-721e474f8a58.png)

When we look at the proportions of target people, the vast majority fall into the young and very young categories (<35), with older people(>35) still being target but to a lesser extent.

When we separate by gender:
![Figure_24](https://user-images.githubusercontent.com/98558551/233464884-d239a12d-4915-4181-9a2d-ec634228dfe3.png)

We see that males are target more than women across every age group, with very young and senior males being significantly more targeted than women when compared to middle age and young men.


