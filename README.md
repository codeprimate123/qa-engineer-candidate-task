# qa-engineer-candidate-task

For convenience, all the tasks are in one repository. The requirements are compatible so everything can be run in one environment (I used conda)

The code was tested on Ubuntu. At the I was short on allowed time, so I didn't refactor the code or use linters and mypy, even though much of the code is typed. It takes some time to review everything for consistency, and if I did, I would want to refactor, but time is running out. As I said, everything runs, but it isn't perfect. Perfection is the enemy of deadlines.

# Selenium for Python for Web Automation Testing
The code was tested with Chrome 130 and the appropriate ChromeDriver. To run the code, you need the appropriate ChromeDriver suited to your OS and Chrome version. The only requirement is Selenium.

I used Selenium as it was preferred. If you left me the choice, I would have used Playwright for Python for convenience and stability, but Selenium also works just fine.

I pretended the code is part of a bigger project, so it is somewhat "overstructured," e.g., classes could fit in just one file, etc.

# API Testing
API tests are by far the shortest test suite. The site to test doesn't really support all that many request types. A report is included. I think spent less then the allocated time and used it to improve other tasks.

# Performance Testing
To be fair, I spent over the allocated time of 2-3 hours as Locust is new to me, but I like it, so I wanted to use at least some of its potential and spent 4 hours, not counting an hour to check the documentation and listen to a video.

It requires Locust and BeautifulSoup. At first, I wanted to use WebDriver to emulate users and extract data from the page, but then I realized I was doing it wrong and revised my approach to use only requests and extracted data with BeautifulSoup. With what I have implemented in the abstract class, many more user behaviors could be implemented, but I was over time as it is, so that is about it.

Report on Performance Testing:
Login and registration are broken.
Response time is slightly longer at the start but later decreases (I assumed there must be some form of caching involved). It isn't lightning fast, but as it is a free test site, I can't really complain.
The site is very stable with 50 users. I tried even a bigger number; I hope the hosts/admins didn't mind.
