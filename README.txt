The program goes through each category in the site and gets links to each offer
then it goes through each offer only if its still valid

Instructions to get final xml file 

1. run helper.py 1st , it will get links to all the categories and save in Cats.txt

2. run getDeals.py , it will take each category link one by one and and get all the 
   info on all the offers in that category while saving it in dealf.txt for time being.
   once its done with one category, it appends all the content of dealf.txt to finaldealf.xml
   and deletes that category link from Cats.txt , and repeats the whole process again till
   Cats.txt is empty.

3. due to category overlapping there may be lot of repetitions, although it is taken care that repeated
   URLs are not processed, by maintaining processedURLS.txt file, if at all there are any repetitions 
   running deleteRepeated.py will delete all the repeated offers from finaldealf.xml


NOTE : I kept dealf.txt as a buffer, as my internet speed is very unstable,
       so its like breaking the whole process into pieces, category wise. 
       i.e. say after running for 10 categories the internet goes down
       so my program crashes, but i have saved all the previous 10 categories data
       in finaldealf.xml, and now when i run the getDeals.py again, it will directly
       start from 11th category.

