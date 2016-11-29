# Report Draft
These all points must be included in ppt/reports

## Initial Approach:

- Started with the classical approach of what all is important
- Data is available
- Interesting piece of information: How we had certain biases like a person's health history or heredity. And location is an important factor.
- How to integrate the different sources of data that we had

## Issues with faceboook and twitter
- Real world approach: you can't use facebook data of profiles to come up with algorithm which impact rates
- Recently a company got in trouble : name of the company /news article link.
- Furthermore, Facebook bans the account, the IP address and reports you to the police.
- Way around: Make the user login and give you permissions to use the posts/etc.
- Twitter: not much of a problem, except getting the user handle

## Classical Approach
- Data from the census data, insurance market place.
- Figuring out how to put it all together and have a weighted order matrix

## Facebook and twitter data Approach
- First task : dictionaries for various approaches
- Second task: Dummy users and data
- Third task: The real action: 
   * Connectivity, fetching posts, fetching tweets
   * Preprocessing: making sure the data we have is ready to be used.
   * Approach: Counting number of occurances of the words created in the various dictionaries and assigning scores based on it. 
     - [ ] I smoke a lot!! was same as I hate smokers!!
     - [ ] Sarcasm
   * Context and specificity were not being taken into consideration, hence change of apporach required. 

## Watson API Approach
   * NLTK and Bluemix API calls.
   * Watson API alone not helpful; it gave a number for relevance and whether it was positive or negative for various words within the posts; it does that even for nouns e.g. "John Doe" 
   * our task to utilize this, and extract only the keywords that were important from the output and then come up with a score using all these keywords are there relevance. Weighted matrix is explained in more detail below. 

## Issues with weighted matrix
- If a person is risky enough for us to increase their insurance rate; but how to make sure we are not surging his insurance rates to a level that he decides not to buy the insurance at all.
that is to make sure the insurance rate are impacted within a given range instead of sky rocketing the rates.
   * setting up limits
   * use average
   * use weighted average?
>> ADD MORE 


## Trivia
- Facebook doesn't allow insurance companies to scrape data and use it without user's permission; that said the above point makes it unsafe to share anything nevertheless.

## Issues with this approach

- user with no FB profiles/ Twitter or relevant data- no impact - can be handled
- Any third party apps you give access to have the access to all your data irrespective of the audience you set or privacy you set i.e. only me option
- user with fake cleaner profile -Error that can't be handled  
- Having the approach where a person with the so called bad posts on facebook would have a  -ve impact (increase in the rates) while the posts where there are +ve impact will have a negative impact (decrease in the rates) . This raises a particular concern where in the user who is a smoker, drinker and occasional drug user who also goes to gym and goes for regular health checkups would netural out the impact and would be given base rate; so to combat this we have decided to give more importance to the negative impact, i.e. the user with "bad posts/tweets" than otherwise.  



## Presentation requirement: 

- question 
- Data collection
- First approach : classical Way - spent most of the time exploring this in detail
- Adding to the classical approach the "Facebook/twitter approach" - the speciality of our app
- Finally Methodology used
- Matrix, weighted order, formulas etc. 
- Problems: interation issues, not sure how to integrate everything, all the data. Facebook data.
- concerns: facebook privacy policy; hidden caveats
- Breaking our own app - we know how to break it; we know where it fails and where it can be handeled: fake users; no data; 
- Conclusion ---> why to use it? why not use it. Moreover, the reasons why it is not being currently used in the mmarket.
