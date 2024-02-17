### LEFT JOIN on posts and votes table 
```
>   A LEFT JOIN shows all the data in the left table and whatever matches in the right i.e. "votes"
>   this includes the posts which have no upvotes i.e post_id column is empty for those posts.
>   Whereas a right join will only show us the rows where
>   'votes.posts_id' matches 'posts.id' thus no null entries for the votes table are shown
SELECT * FROM posts LEFT JOIN votes ON posts.id = votes.post_id;
```

### EVERYTHING in posts table and number of votes on each post 

```
    SELECT posts.*, COUNT(votes.post_id) as **votes** FROM posts 
    LEFT JOIN votes ON posts.id = votes.post_id # add WHERE to get specific post
    GROUP By posts.id;
```
```
SELECT users.name,budget.amount FORMAT(amount,2) as forma_val FROM users
JOIN budget ON users.id = budget.cust_id
WHERE budget.amount >= 0 ORDER By budget.amount 
```