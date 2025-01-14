from flask import render_template, Blueprint, request
from sqlalchemy import or_


from src.models import Book


search_blueprint = Blueprint("search", __name__)



@search_blueprint.route("/search/", methods=['GET'])
def search_result():
    search_term = request.args.get('search', '').lower()

    if search_term:
        # Split the search term into individual keywords
        keywords = search_term.split()

        # Construct a dynamic OR condition for each keyword for name and author
        condition_name = or_(*[Book.project_name.ilike(f'%{keyword}%') for keyword in keywords])
        condition_author = or_(*[Book.student_fullname.ilike(f'%{keyword}%') for keyword in keywords])
        condition_school = or_(*[Book.school.ilike(f'%{keyword}%') for keyword in keywords])

        # Combine the conditions using OR for name and author
        combined_condition = or_(condition_name, condition_author, condition_school)

        # Print the generated SQL query
        search_results_query = Book.query.filter(combined_condition)

        # Execute the query to get the results
        search_results = search_results_query.all()
    else:
        search_results = []

    return render_template('search/search_result.html', search_term=search_term, results=search_results)