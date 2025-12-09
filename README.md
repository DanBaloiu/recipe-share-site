# 🧑‍🍳 Recipe Share Site

**Live Site:**  
[https://recipe-share-site-new-919ac18d9f8e.herokuapp.com/](https://recipe-share-site-new-919ac18d9f8e.herokuapp.com/)

**GitHub Repository:**  
[https://github.com/DanBaloiu/recipe-share-site](https://github.com/DanBaloiu/recipe-share-site)

A modern, mobile-friendly recipe sharing platform where users can browse, post, comment on, and rate recipes.  
Built with Django 4.2, Bootstrap 5, Cloudinary, and PostgreSQL, and deployed on Heroku.

---

## 🧭 1. Purpose & UX Strategy

The goal of **Recipe Share Site** is to provide a clean, accessible environment for cooking enthusiasts to:

- Discover easy and delicious recipes.  
- Share their own recipes with others.  
- Interact through comments and ratings.

### 🎯 Target Audience

- Food lovers looking for inspiration.  
- Home cooks wanting to document and share creations.  
- Users seeking social engagement through recipe discussion.

### 🎨 Design Choices

- Simple, clear Bootstrap layout.  
- Bright imagery to highlight food visuals.  
- **Primary colour:** Bootstrap blue  
- **Secondary:** Neutral grey and white  
- **Font:** Bootstrap default (`system-ui, sans-serif`)

---

## 🚀 2. Agile Methodology & User Stories

Agile development was used throughout, with incremental commits on GitHub representing small deliverables.

### User Stories

| ID | As a... | I want to... | So that I can... | Status |
|----|-----------|---------------|------------------|---------|
| 1 | admin | Manage content | keep the site high quality | ✅ |
| 2 | User | Register / log in | I can interact with the site | ✅ |
| 3 | User | Add a recipe with an image | Share my own dish | ✅ |
| 4 | User | Comment on recipes | Share feedback or tips | ✅ |
| 5 | User | Rate recipes (1–5 stars) | Express my opinion | ✅ |
| 6 | Admin | Moderate content | Maintain quality and respectfulness | ✅ |
| 7 | Visitor | View recipe details | See ingredients and steps clearly | ✅ |
| 8 | Visitor | Paginate through recipes | Browse easily | ✅ |
| 9 | Visitor | See average ratings | Gauge popularity of recipes | ✅ |
| 10 | User | Edit my recipe | Improve it | ✅ |
| 11 | User | Delete my recipe | Remove unwanted content | ✅ |

- User stories also available in the [Project Board](https://github.com/users/DanBaloiu/projects/9)

---

## ⚙️ 3. Features

### Implemented Features

| Feature | Description |
|----------|--------------|
| **Recipe Listing** | Displays all published recipes in a Bootstrap card grid with pagination and average rating. |
| **Recipe Detail Page** | Shows full details, ingredients, steps, author, date, comments, and rating form. |
| **User Authentication** | Signup, login, and logout handled via Django AllAuth. |
| **Add / Edit Recipes** | Authenticated users can submit new recipes with images (Cloudinary). |
| **Comment System** | Logged-in users can post and view comments under each recipe. |
| **Ratings System** | Users can leave one 1–5 star rating per recipe; average displayed. |
| **Admin Dashboard** | Full CRUD control over recipes, comments, and ratings. |
| **Responsive Design** | Layout adapts seamlessly to mobile, tablet, and desktop. |
| **Cloudinary Media** | Recipe images stored externally for persistence across deployments. |

### Future Enhancements
 
- Tag-based filters  
- Email notifications for replies  
- Rich-text formatting for ingredients and steps

---

## 🧩 4. Information Architecture

### Navigation Map

- `/` → Recipe List (pagination)  
- `/recipe/<slug>/` → Detail (comments, rating)  
- `/accounts/` → AllAuth authentication routes  
- `/admin/` → Admin dashboard

### Database Schema

![ERD Schema](staticfiles/images/ERD.png)

---

## 🎨 5. Design & Branding

### Typography & Colour Palette

- **Font:** Bootstrap default system font stack  
- **Primary colour:** `#0d6efd` (Bootstrap blue)  
- **Accent:** `#6c757d` (grey)  
- **Background:** `#ffffff`  
- **Contrast:** Dark text on light background for accessibility

### Wireframes & Mockups

![Desktop Wireframe](staticfiles/images/Wireframe_desktop.png)  
![Mobile Wireframe](staticfiles/images/Wireframe_mobile.png)

---

## 🧰 6. Technologies Used

| Category | Technology |
|-----------|-------------|
| **Languages** | Python 3, HTML5, CSS3, JavaScript |
| **Frameworks** | Django 4.2, Bootstrap 5 |
| **Database** | PostgreSQL (Heroku) |
| **Storage** | Cloudinary |
| **Hosting** | Heroku |
| **Libraries** | dj-database-url, psycopg, django-allauth, gunicorn, whitenoise |
| **Version Control** | Git & GitHub |
| **Deployment** | GitHub → Heroku CI/CD pipeline |

---

## 🚀 7. Deployment

This website is deployed to Heroku from a GitHub repository, the following steps were taken:

### Creating Repository on GitHub
- First make sure you are signed into [Github](https://github.com/) and go to the repository, which can be found [here](https://github.com/Code-Institute-Org/ci-full-template).
- Then click on use this template and select Create a new repository from the drop-down. Enter the name for the repository and click Create repository from template.
- Once the repository was created, I clicked the green gitpod button to create a workspace in gitpod so that I could write the code for the site.
Creating an app on Heroku
- After creating the repository on GitHub, head over to [heroku](https://www.heroku.com/) and sign in.
- On the home page, click New and Create new app from the drop down.
- Give the app a name(this must be unique) and select a region I chose Europe as I am in Europe, Then click **Create app**.
### Create a database
- Log into [CIdatabase maker](https://www.heroku.com/%5D(https://dbs.ci-dbs.net/))
- add your email address in input field and submit the form
open database link in your email
- paste dabase URL in your DATABASE_URL variable in env.py file and in Heroku config vars
### Deploying to Heroku.
- Head back over to heroku and click on your app and then go to the Settings tab
- On the settings page scroll down to the config vars section and enter the DATABASE_URL which you will set equal to the elephantSQL URL, create - Secret key this can be anything, CLOUDINARY_URL this will be set to your cloudinary url and finally Port which will be set to 8000.
- Then scroll to the top and go to the deploy tab and go down to the Deployment method section and select Github and then sign into your account.
- Below that in the search for a repository to connect to search box enter the name of your repository that you created on GitHub and click connect
- Once it has been connected scroll down to the Manual Deploy and click Deploy branch when it has deployed you will see a view app button below and this will bring you to your newly deployed app.
- Please note that when deploying manually you will have to deploy after each change you make to your repository.

## 🧪 8. Testing

### ✅ Code Validation

| Tool | Status | Screenshot |
|------|---------|-------------|
| **HTML (W3C Validator) - Homepage** | ✅ Passed | ![HTML Validator](staticfiles/images/HTML_Homepage_Validation.jpg) |
| **HTML (W3C Validator) - Post** | ✅ Passed | ![HTML Validator](staticfiles/images/HTML_After_2.png) |
| **HTML (W3C Validator) - Submit Post** | ✅ Passed | ![HTML Validator](staticfiles/images/HTML_Submit_Recipe_Validation.jpg) |
| **HTML (W3C Validator) - Sign up** | ✅ Passed | ![HTML Validator](staticfiles/images/HTML_Signup_Validation.jpg) |
| **CSS (W3C Validator) - Homepage** | ✅ Passed | ![CSS Validator](staticfiles/images/CSS_Validation.png) |
| **CSS (W3C Validator) - Post** | ✅ Passed | ![CSS Validator](staticfiles/images/CSS_Post_Validation.jpg) |
| **CSS (W3C Validator) - Submit Recipe** | ✅ Passed | ![CSS Validator](staticfiles/images/CSS_SubmitRecipe_Validation.jpg) |
| **CSS (W3C Validator) - Sign Up** | ✅ Passed | ![CSS Validator](staticfiles/images/CSS_SignUp_Validation.jpg) |
---

### ⚡ Performance (Lighthouse)

| Metric | Score |
|--------|--------|
| **Performance** | 78 |
| **Accessibility** | 97 |
| **Best Practices** | 78 |
| **SEO** | 91 |

![Lighthouse Report](staticfiles/images/Lighthouse_results.png)

---

---

### ▶ Running tests locally


Test run (project `recipes` app)

The following is an example run of the test suite for the `recipes` app (this project). It shows the test database creation, the discovered tests, and the final OK status indicating all tests passed.

```
$ C:/Users/Dan/recipe-share-site/.venv/Scripts/python.exe manage.py test recipes
Found 10 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 10.885s

OK
Destroying test database for alias 'default'...
```

Which tests were added

- `recipes/test_forms.py`
	- `TestCommentForm.test_form_is_valid` — verifies `CommentForm` valid when `body` provided.
	- `TestCommentForm.test_form_is_invalid_when_body_missing` — verifies `CommentForm` invalid when `body` is empty.
	- `TestRecipeForm.*` — verifies `RecipeForm` validates required fields (title, description, ingredients, steps, and numeric fields `prep_minutes`, `cook_minutes`, `servings`).

- `recipes/test_views.py`
	- `TestRecipeViews.test_recipe_detail_get_contains_form_and_content` — recipe detail page loads and includes `comment_form` in context.
	- `TestRecipeViews.test_comment_post_requires_login` — POSTing a comment when not authenticated redirects to login.
	- `TestRecipeViews.test_comment_post_creates_unapproved_comment` — authenticated comment submissions create `Comment` with `approved=False`.
	- `TestRecipeViews.test_rating_post_creates_rating` — authenticated rating POST creates a `Rating` record.
	- `TestRecipeViews.test_invalid_empty_rating_does_not_create_and_no_500` — submitting an empty rating is handled gracefully and does not crash.
	- `TestRecipeViews.test_pending_recipes_access_control` — `pending_recipes` is blocked for non-staff and accessible to staff users.

How these tests map to the assessment

- LO4.1: The tests exercise functionality and data management for comments, ratings and recipe forms, demonstrating automated checks for correctness and basic access control.
- LO4.3: This README documents the tests, their purpose, and the exact test output shown above (single-source documentation as required).

![Test run screenshot](staticfiles/images/Testing_1.jpg)
*Figure: Project test run showing all `recipes` tests passing.*

### 🧭 Manual Testing

| Action | Expected Result | Outcome |
|--------|-----------------|----------|
| Load homepage | Recipes displayed, responsive layout | ![Load homepage](staticfiles/images/Load_Homepage.jpg) |
| Login Confirmation | Hello, Username displayed on the navbar | ![Login Confirmation](staticfiles/images/Loin_Confirmation.jpg) |
| View recipe detail | Ingredients, steps, and comments visible | ![Login Confirmation](staticfiles/images/View_recipe_detail.jpg) |
| Post a comment | Recive notification awaiting admin aproval | ![Post a comment](staticfiles/images/Comment_Notification.jpg) |
| Rate recipe | Rating saved and average updates | ![Rate recipe](staticfiles/images/Submit_rating.jpg) |
| Update rating | Updates the rating and shows confirmation | ![Update rating](staticfiles/images/Update_Rating.jpg) |
| Log out | Logout user and redirects to homepage | ![Log out](staticfiles/images/Confirm_Logout.jpg) |
| Update a comment | Asks for confirmation and send to admin for validation | ![Update a comment](staticfiles/images/Update_Comment.jpg) |
| Delete a comment | Asks for confirmation and deletes from database | ![Delete a comment](staticfiles/images/Delete_Comment.jpg) |
| Staff: Pending recipes | Shows draft recipes with Approve / Reject buttons | ![Staff: Pending recipes](staticfiles/images/Pending_Admin.jpg) |
| Staff: Approve recipe | Recipe published and removed from pending list | ✅ |
| Staff: Reject recipe | Recipe removed from pending list (not public) | ✅ |
| Staff: Pending comments | Shows unapproved comments with Approve / Reject buttons | ![Staff: Pending comments](staticfiles/images/Pending_Comments.jpg) |
| Staff: Approve comment | Comment appears under the recipe | ✅ |
| Non-staff access to staff pages | Redirected or blocked (no access) | ✅ |

---

## 🐛 9. Bugs & Fixes

| Issue | Description | Fix |
|--------|--------------|-----|
| **TemplateDoesNotExist** | Template paths missing | Added `TEMPLATES[0]["DIRS"]` |
| **DATABASES Improperly Configured** | Missing ENGINE | Added SQLite fallback & `dj-database-url` |
| **Cloudinary errors** | Missing `CLOUDINARY_URL` | Added env var + `cloudinary_storage` |
| **STATICFILES_STORAGE/STORAGES conflict** | Django 4.2 change | Removed legacy setting |
| **CSRF_TRUSTED_ORIGINS** | Missing HTTPS scheme | Fixed with `https://...` |
| **Heroku 503 (H14)** | No web dyno running | Added `Procfile` |
| **Collectstatic errors** | Missing CSS references | Corrected file paths |
| **Images missing on Heroku** | Ephemeral filesystem | Configured Cloudinary storage |
| **Comments not visible** | Missing model/form context | Fixed logic in views |
| **Rating submission (no star)** | Submitting the rating form without selecting a star caused an HTTP 500 server error (UnboundLocalError / unexpected POST handling). | Added a client-side guard + modal to prevent empty submissions and updated server-side view logic to handle unexpected POSTs gracefully. |
| **Ratings admin-only** | UI integration missing | Added frontend star-rating + average logic |


---

## 📷 11. Screenshots

![Homepage Screenshot](staticfiles/images/Desktop_Screen.png)  
![Recipe Detail Screenshot](staticfiles/images/Screenshot_Detail.png)  
![Admin Dashboard Screenshot](staticfiles/images/Screenshot_Admin.png)

### Responsiveness Testing
1 Desktop
![Desktop](staticfiles/images/Desktop_Screen.png)
2 Tablet
![Tablet](staticfiles/images/Tablet_View.png)
3 Mobile
![Mobile](staticfiles/images/Mobile_Screen.png)

### Different Browser Testing
![Chrome](staticfiles/images/Chrome.jpg)
![Safari](staticfiles/images/Safari.jpg)
![Microsoft Edge](staticfiles/images/Edge.jpg)
![Opera](staticfiles/images/Opera.jpg)
![Firefox](staticfiles/images/Firefox.jpg)

---

## 💡 12. Lessons Learned

- Always set `CSRF_TRUSTED_ORIGINS` with `https://` in Django 4+.  
- Use Cloudinary from the start to avoid Heroku media loss.  
- Django 4.2 uses `STORAGES` instead of `STATICFILES_STORAGE`.  
- Never skip migrations during deployment.  
- Keep commits small and descriptive.

---

## 🤖 14. AI Usage (Reflection)

This project made strategic use of AI-assisted developer tools during implementation, debugging, and design. The purpose of this section is to document where AI was used, what outcomes it produced, and how those contributions were validated.

Summary of AI tools used:
- **ChatGPT (OpenAI)** — used for higher-level design suggestions, refactoring guidance, and to draft small code changes and documentation snippets.
- **GitHub Copilot** — used while coding to suggest function and test scaffolding, form/widget attributes, and small template snippets.

Key outcomes (mapped to LO8 assessment criteria):

- **1 — AI-assisted code creation**: AI was used to help generate and refine code for several front-end and back-end improvements, including:
	- Adding Bootstrap-compatible widgets and classes to `recipes/forms.py` so forms render with consistent styling.
	- Implementing staff approval views and templates (`recipes/views.py`, `recipes/urls.py`, `recipes/templates/recipes/pending_*.html`).
	- Creating a small context processor (`recipes/context_processors.py`) to provide pending counts to templates.
	These changes were reviewed and adjusted manually to ensure they fit the project's architecture and coding style.

- **2 — AI-assisted debugging**: AI helped diagnose and fix a Django template error caused by attempting to pass keyword args into `label_tag` from templates (Django templates do not support that syntax). The solution was to render labels manually using `{{ form.field.id_for_label }}` and explicit `<label>` elements. The fix was validated by reloading the pages and confirming the error no longer occurred.

		Additional debugging example (rating submission):

		- Problem found during early testing: it was possible to submit the rating form without selecting any stars. This caused a server-side crash (HTTP 500 Internal Server Error) when the missing value was treated as a numeric rating. The issue was reproduced by a tester and confirmed locally.
		- AI-assisted fix: an AI-assisted suggestion implemented a small client-side guard that prevents submission when no star is selected and displays a modal prompting the user to choose a rating. This prevented the 500 error and improved UX.
		- AI-assisted UI fix (duplicate modals): AI suggested showing the rating 'Thanks' modal *instead* of the generic flash modal when a rating is submitted, and to add a close (X) control to the rating modal for consistent behavior. This was implemented in `templates/base.html` to avoid overlapping modals and improve UX.
		- Evidence and screenshots: to document the fix for resubmission, add two screenshots to `staticfiles/images`:
			- `rating_before.png` — the HTTP 500 error screen (before the client-side guard).
			- `rating_after.png` — the modal shown when attempting to submit without selecting a star (after the client-side guard).
			Insert them here once you have them:

			![Rating bug — before](staticfiles/images/Star_submit_error.jpg)

			![Rating bug — after](staticfiles/images/Star_submit_error_fixed.jpg)

- **3 — AI-assisted performance & UX improvements**: AI suggested pragmatic UX improvements that were implemented, such as:
	- Adding Bootstrap layout and spacing to auth and form pages for consistent, mobile-friendly UX.
	- Introducing admin-facing pending-count badges and a lightweight moderation interface to improve content moderation workflow (fewer backend-only admin steps).
	These suggestions were implemented conservatively and manually verified in the browser.

- **4 — AI-assisted test generation**: GitHub Copilot has been used to help draft unit test scaffolding and example test cases (for model helpers, view permissions, and form validation). Test code is being reviewed and adjusted to align with the project's logic; a focused test suite will be added to `recipes/tests.py` and the test report / instructions will be documented in this `README.md` (see Testing section above).

How AI was used responsibly
- All AI-generated code and suggestions were reviewed by the developer. Where generated code did not exactly match project conventions or requirements, it was edited and tested manually.
- No sensitive information, credentials, or private prompts were stored in the repository. All environment-specific secrets remain in environment variables or `env.py` (not checked into source control).


## 🙌 13. Credits & Acknowledgements

- **Developer:** [Dan Baloiu](https://github.com/DanBaloiu)  
- **Mentor / Facilitator:** Code Institute Team  
- **Icons & Images:** [Cloudinary](https://cloudinary.com/) & Generated by AI
- **Frameworks:** Django, Bootstrap 5  
- **Hosting:** Heroku
