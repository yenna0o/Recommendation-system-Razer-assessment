# Data Scientist Technical Assessment<br>
This project uses 2 differnt algorithms to recommend a list of 5 products based on a given product ID.<br>
## Installation
Make sure you've already git installed. Then you can run the following commands to get the scripts on your computer:
OS X, Linux and Windows:
```bash
git clone https://github.com/yenna0o/Razer_assignment.git
cd Razer_assignment
```
## Scripts
Please install the required packages before running the scripts.<br>
    ```python
    pip install -r requirements.txt
    ```

* ### hybrid_run.py
    - Algorithm 1.
    - This script outputs a list of 5 product IDs based on an input product ID.
    - The recommendation algorithm is a combine of both user-based and popularity-based.
    - It will be reading data from "Appliances.json" file, hence you need to have the data file downloaded to the same path as this python script.
    - Fetch "reviews" file under Appliances from https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/
    #### Usage Instructions
    ```python
    python hybrid_run.py
    ```
    #### Test example
    ![hybrid_example](https://github.com/yenna0o/Images-in-readme/assets/98952623/f71e66bb-b84d-48c5-a882-6f42e5af9041)

* ### item_based_run.py
    - Algorithm 2.
    - This script outputs a list of 5 product titles based on an input product ID.
    - The recommendation algorithm is item-based.
    - It will be reading data from "meta_Appliances.json" file, hence you need to have the data file downloaded to the same path as this python script.
    - Fetch "metadata" file under Appliances from https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/
    #### Usage Instructions
    ```python
    python item_based_run.py
    ```
    #### Test example
    ![item_based_example](https://github.com/yenna0o/Images-in-readme/assets/98952623/e9703e45-f5a6-42b1-9982-d69b7e9a5e37)
## Algo Explanation:
* ### Algorithm 1 (hybrid): "Users who liked this item also liked…"<br>
Flowchart:<br>
![Screenshot 2023-12-07 021627](https://github.com/yenna0o/Images-in-readme/assets/98952623/9052fc00-6474-4bc1-a420-1a71cf86bc57)<br>
Data file used: Appliances.json<br>
* Algo steps:
    - 1. User input a product id.<br>
    - 2. Based on the product id, find a group of users who liked this product. (An overall of 5 given is deemed as “liked” by the user)<br>
Rationale: The user who wants to buy the product might have similar interest to the users who liked the same product.<br>
    - 3. From the group of users identified, randomly select one user.<br>
Rationale: since there might be too many users, random selection might be a good choice.<br>
    - 4. Find a group of products liked by the selected user.<br>
Rationale: Since the two users might have similar interests, the products liked by one user might also be liked by the other user.<br>
    - 5. Randomly select one product to add to the recommendation list.<br>
Rationale: selecting one product each from different users increases the variety of the products to be recommended.<br>
    - 6. Loop steps 3-5 until a list of 5 products are generated, or the user list is exhausted.<br>
    - 7. If the user list is exhausted but there are less than 5 products, proceed to step 8; If there are already 5 products in the recommendation list, stop the process.<br>
    - 8. Prepare a group of products that are liked by more than 50 times in the most recent year. (2018).<br>
    - 9. Randomly select n products and add to the recommendation list. (n = 5 - len(recommendation)).<br>
    - 10. Stop the process.<br>

* ### Algorithm 2 (item-based): "Similar products you might like..."<br>
Data file used: meta_Appliances.json<br>
* Algo steps:<br>
    - 1. Based on the 'title' of each product, use TF-IDF technique to vectorize them and save as a matrix.<br>
    - 2. Compute consine similarity on the matrix, products are on both row and columns. The resultant consine similarity matrix is stored.<br>
    - 3. Locate the product input from the similarity matrix and get the list of consine similarity values with all other products.<br>
    - 4. Find the 10 most similar products.<br>
    - 5. Randomly generate 5 from the 10 products.<br>
    
### Comparing the 2 algorithms
* When it's better to use algo 1:
The recommendation list may involve a wide range of products. This works better for customers who just want to look around and do not really have a determined shopping goal. They are waiting to be inspired by recommending to them what other buyers liked.
* When it's better to use algo 2:
If the customer is determined to buy a product, it might be better to recommend them based on product features instead of similar user interests.
