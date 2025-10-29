from src.base.base_page import BasePage


class LearnerHomePage(BasePage):
    BROWSE_COURSES="Browse Courses"
    FEATURED_TP_NAME="(//div[@aria-roledescription='carousel'])[2]//h3"
    FEATURED_COURSE_NAME="(//div[@aria-roledescription='carousel'])[1]//h3"
