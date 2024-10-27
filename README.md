# Project 02 Group 15 Wishlist 
<hr>
Turn your dreams into a clickable reality

Video: [youtube url]

## Running the Backend:
#### Installation Directions:
1. Change directories into ../Project02
   ```bash
   cd Project02
   ```
2. Go into a virtual environment

   ```bash
   python -m venv venv 
   .\venv\Scripts\Activate
   ```
3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```
4. Start the server
 ```bash
   python manage.py runserver
 ```
# Project 02 Retrospective 
#### Introduction:
Communication was managed on Slack through a group chat with all four members. We communicated mainly through sending messages on this chat but we also had a few Slack calls to catch up on what needed to be done and if we had any questions.
Originally we had around 20 stories considered for the project that included all the pages we needed to create, all the endpoints we needed, bug fixes, and tests. We ended with more stories than initially considered, with 24 issues completed. 

## Team Retrospective
### Mikaela Charisse Lagumbay
I worked on most of the frontend development, creating and styling the main pages with React and JSX. I designed the Figma mockups that we followed for our website layout and implemented the admin display system for user management. I also made sure our styling was consistent across all pages. I spent about 3-5 hours a week working outside of class, mainly on implementing the designs and making sure all the pages worked together properly. The biggest challenge was discovering we needed additional pages later in the project, like the admin and profiles system. It was challenging because we had to integrate these new features while maintaining consistent styling and functionality with existing pages. We handled this by prioritizing features and making sure to keep consistent styling by reusing components we already had. Even though we were working under time pressure, we made sure everything still looked and worked well together. My favorite part was creating the designs of all the pages and seeing it come to life. It was really rewarding seeing how our whole site came together to create a cohesive and functional web application. I would have gotten a better list of all the pages we needed at the start of the project. Having to add new pages later on, like the admin and profiles system, meant rushing to finish them in a shorter time. Better planning at the beginning would have helped us manage our time better but I think we did good. The most important thing I learned was how important initial planning is for front-end development. Understanding all the required features and pages from the start makes it easier to create a consistent and well-structured application.

### Kyla Usi
My role was a backend developer for the API endpoints. I worked on the Login and Admin stories. I spent about 2 hours every week outside of class to work on the project. The biggest challenge was figuring out how to add permissions on Django for  the endpoints to make sure that the user was an admin and figuring out the sessions at the end was a problem. It turns out that we didn’t need those permissions after all and it would be much easier for frontend to check the boolean if the user is an admin or not. We also ended up getting rid of the sessions since it was not working along with the frontend. The sessions were working on the Django REST framework in the backend but we were running out of time to get the sessions working. Diego helped me out and passed the user_id to those endpoints so we can access the user’s lists, items, and information. My favorite part of the project was finally integrating the frontend with the backend and seeing our hard work, working together. I was really happy with seeing the endpoints work with the really clean designs that the frontend created. It felt like everything was coming together once the login and sign up was integrated. If I could do it over again, I would ask more people about how they connected their Docker image, database, and Heroku all working together. The most valuable thing I learned is that attitude is everything. I noticed that even though we were having problems, we would communicate and we worked really well as a team. We were all there to help each other and I could tell that everyone’s mood was focused and motivated to get everything working. Great team that I would want to work with again. 

### Diego Zavala
As a backend developer, I handled database integration and migration, Docker setup, deploying to Heroku, and creating the item and list API endpoints. I spent around 3-5 hours on average per week with some sessions exceeding that due to recurring issues in the database setup, Docker configuration, and deployment to Heroku. The biggest challenge was definitely connecting the Django code to the JawsDB Maria database and building the image properly so it runs on heroku as well as locally. It was challenging due to the unfamiliarity and limited effective resources on the internet. Through persistent trial and error over a week and a half, I tried a different approach and simplified the configuration which finally worked. Getting all the database, docker, and heroku deployment to work was the biggest victory for me because it was a huge weight taken from my shoulders once it worked. If I could do it over again, I would consider using Spring Boot over Django for potentially a smoother integration and setup as well as getting a different experience. The biggest thing I learned was to expect setbacks and deviations from the original project plan and timetable but to keep trying because eventually you will break through those setbacks and succeed.

### Sumit Sunchu

## Conclusion
We believe that although we had some setbacks and the development process did not go as planned, the overall project was a success. With most of the endpoints working properly with the front end, we were able to knock off those requirements. The frontend design of the website also looks well thought out and professional which only adds to the project’s overall success. The largest victory was getting the frontend to start using the API endpoints and finally being able to use the website as intended. The final assessment of the project is that working with a modern software engineering tech stack of separate frontend, backend, and database all while being hosted live in a docker container comes with learning pains. The setbacks are what caused growth and we feel that we have all grown in our abilities as software engineers by following practices that are used in the industry like agile development. 
